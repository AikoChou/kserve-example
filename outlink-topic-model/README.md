# Deploying Outlink-Topic model with transformer and predictor on a local Docker instance of KServe

## Setup

1. Install [Docker](https://www.docker.com/products/docker-desktop/)
2. Clone this repository to your local
3. Download the outlink-topic [model binary](https://analytics.wikimedia.org/published/datasets/one-off/isaacj/articletopic/model_alloutlinks_202012.bin) to `models/`

## Build the Docker images

Change your directory to `outlink-topic-model`
```
cd kserve-example/outlink-topic-model
```

Build the transformer's Docker image
```
docker build -t outlink-transformer -f transformer.Dockerfile .
```

Build the predictor's Docker image
```
docker build -t outlink-predictor -f model.Dockerfile .
```

## Deploy locally via Docker

Start a predictor docker container
```
docker run --rm -v `pwd`/models:/mnt/models outlink-predictor
```

If everything goes fine, you should see logs reporting from kserve
```
[I 220724 18:34:20 kfserver:150] Registering model: outlink-topic-model
[I 220724 18:34:20 kfserver:120] Setting asyncio max_workers as 8
[I 220724 18:34:20 kfserver:127] Listening on port 8080
[I 220724 18:34:20 kfserver:129] Will fork 1 workers
```

Next, we are going to connect the transformer and predicator together using Docker's default network called `bridge`.

First, open a new terminal, get the predictor container ID
```
docker ps
```

Then check the predictor container's IP address
```
docker inspect <container-id> | grep IPAddress
```

Start a transformer container using the following command, replace `<predictor-ip-address>` with what you found in the last step
```
docker run -p 8080:8080 --rm outlink-transformer --predictor_host <predictor-ip-address>:8080 --model_name outlink-topic-model
```

If everything goes fine, you should see logs reporting from kserve
```
[I 220724 18:49:53 kfserver:150] Registering model: outlink-topic-model
[I 220724 18:49:53 kfserver:120] Setting asyncio max_workers as 8
[I 220724 18:49:53 kfserver:127] Listening on port 8080
[I 220724 18:49:54 kfserver:129] Will fork 1 workers
```

## Test the model 

Open a new terminal, change dir to `kserve-example/outlink-topic-model` and run the following command to send a test inference request
```
curl localhost:8080/v1/models/outlink-topic-model:predict -d @input.json --http1.1
```

If everything goes fine, you should see the predicted topics and scores for the test article in the HTTP response.
```
{"prediction": {"article": "https://en.wikipedia.org/wiki/Toni Morrison", "results": [{"topic": "Culture.Biography.Biography*", "score": 0.9626831412315369}, {"topic": "Culture.Biography.Women", "score": 0.8933194279670715}, {"topic": "Geography.Regions.Americas.North_America", "score": 0.7186043858528137}, {"topic": "Culture.Literature", "score": 0.5775054097175598}, {"topic": "History_and_Society.History", "score": 0.4843900501728058}]}}
```
