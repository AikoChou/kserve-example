FROM docker-registry.wikimedia.org/python3-build-buster:0.1.0

COPY transformer transformer
RUN pip3 install --no-cache-dir --upgrade pip && pip3 install --no-cache-dir -r ./transformer/requirements.txt

ENTRYPOINT ["python3", "./transformer/transformer.py"]
