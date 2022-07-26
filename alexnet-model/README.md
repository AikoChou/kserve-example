# Deploying Alexnet model on a local Docker instance of KServe


## Setup

1. Install [Docker](https://www.docker.com/products/docker-desktop/)
2. Clone this repository to your local
3. Download the Alexnet model [weights](https://download.pytorch.org/models/alexnet-owt-7be5be79.pth) to `models/`

## Build the Docker image

Change your directory to `alexnet-model`
```
cd kserve-example/alexnet-model
```

Make sure your Docker is running locally!

Run the following command to build the Docker image
```
docker build -t SOME-DOCKER-TAG-THAT-YOU-LIKE -f Dockerfile .
```

After the building is finished, you may want to check if the image is in your local environment
```
docker image ls
``` 

## Deploy Locally and Test

Launch the docker image built from last step
```
docker run --rm -p 8080:8080 -v `pwd`/models:/mnt/models SOME-DOCKER-TAG-THAT-YOU-LIKE
```
* `-p 8080:8080` exposes port 8080 of the container to port 8080 of the host
* `-v "$(pwd)"/models:/mnt/models` mounts `models` directory to `/mnt/models`, so kserve can access the models in the container.

If everything goes fine, you should see logs reporting from kserve
```
[I 220725 09:06:00 kfserver:150] Registering model: alexnet-model
[I 220725 09:06:00 kfserver:120] Setting asyncio max_workers as 8
[I 220725 09:06:00 kfserver:127] Listening on port 8080
[I 220725 09:06:00 kfserver:129] Will fork 1 workers
```

Now we are ready to test the model server!

Open a new terminal, change dir to `kserve-example/alexnet-model` and run the following command to send a test inference request
```
curl localhost:8080/v1/models/alexnet-model:predict -d @input.json
```
The `input.json` follows the [Tensorflow V1 HTTP API](https://www.tensorflow.org/tfx/serving/api_rest#encoding_binary_values) for encoding image bytes. We encoded a test image `dog.jpeg` to a base64 string and encapsulated it in `input.json`.

If everything goes fine, you should see the top 5 predicted classes and probabilities for the test image in the HTTP response.
```
{"Samoyed": 0.7244765758514404, "wallaby": 0.1393786072731018, "Pomeranian": 0.05874988064169884, "Angora": 0.022829724475741386, "Arctic fox": 0.012450194917619228}
```
