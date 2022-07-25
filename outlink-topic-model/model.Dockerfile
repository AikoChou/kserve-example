FROM docker-registry.wikimedia.org/python3-build-buster:0.1.0

RUN apt-get update && apt-get install -y \
        g++ \
        && rm -rf /var/lib/apt/lists/*

COPY model-server model-server
RUN pip3 install --no-cache-dir --upgrade pip && pip3 install --no-cache-dir -r ./model-server/requirements.txt

ENTRYPOINT ["python3", "./model-server/model.py"]
