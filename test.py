import pytest
from fastkafka.testing import Tester

from application import IrisInputData, kafka_app, IrisPrediction


msg = IrisInputData(
    sepal_length=0.1,
    sepal_width=0.2,
    petal_length=0.3,
    petal_width=0.4,
)


@pytest.mark.asyncio
async def test():
    # Start Tester app and create local Redpanda broker for testing
    async with Tester(kafka_app).using_local_redpanda(tag="v23.1.2", listener_port=9092) as tester:
        # Send IrisInputData message to input_data topic
        await tester.to_input_data(msg)

        # Assert that the kafka_app responded with IrisPrediction in predictions topic
        await tester.awaited_mocks.on_predictions.assert_awaited_with(
            IrisPrediction(species="setosa"), timeout=2
        )
