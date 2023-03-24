FROM python:3.9-slim-bullseye

SHELL ["/bin/bash", "-c"]
WORKDIR /project

COPY application.py requirements.txt /project/

RUN pip install --no-cache-dir -r /project/requirements.txt

CMD ["fastkafka", "run", "--num-workers", "2", "--kafka-broker", "production", "application:kafka_app"]
