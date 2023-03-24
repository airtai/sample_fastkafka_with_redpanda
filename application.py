from typing import *

from os import environ

from fastkafka import FastKafka
from pydantic import BaseModel, NonNegativeFloat, Field


class Model:
    
    def predict(*args, **kwargs) -> List[int]:
        return [0, 1, 2]
    
model = Model()


class IrisInputData(BaseModel):
    sepal_length: NonNegativeFloat = Field(
        ..., example=0.5, description="Sepal length in cm"
    )
    sepal_width: NonNegativeFloat = Field(
        ..., example=0.5, description="Sepal width in cm"
    )
    petal_length: NonNegativeFloat = Field(
        ..., example=0.5, description="Petal length in cm"
    )
    petal_width: NonNegativeFloat = Field(
        ..., example=0.5, description="Petal width in cm"
    )


class IrisPrediction(BaseModel):
    species: str = Field(..., example="setosa", description="Predicted species")


kafka_server_url = environ.get("KAFKA_HOSTNAME", "localhost")
kafka_server_port = environ.get("KAFKA_PORT", 9092)

kafka_brokers = {
    "localhost": {
        "url": kafka_server_url,
        "description": "local development kafka broker",
        "port": kafka_server_port,
    },
    "production": {
        "url": "kafka.airt.ai",
        "description": "production kafka broker",
        "port": 9092,
        "protocol": "kafka-secure",
        "security": {"type": "plain"},
    },
}

kafka_app = FastKafka(
    title="Iris predictions",
    kafka_brokers=kafka_brokers,
)


@kafka_app.consumes(topic="input_data", auto_offset_reset="latest")
async def on_input_data(msg: IrisInputData):
    global model
    species_class = model.predict(
        [[msg.sepal_length, msg.sepal_width, msg.petal_length, msg.petal_width]]
    )[0]

    to_predictions(species_class)


@kafka_app.produces(topic="predictions")
def to_predictions(species_class: int) -> IrisPrediction:
    iris_species = ["setosa", "versicolor", "virginica"]

    prediction = IrisPrediction(species=iris_species[species_class])
    return prediction
