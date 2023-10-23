FROM ubuntu:22.04

LABEL maintainer="rcao6@bcit.ca"

RUN apt-get update -y && apt-get install -y python3 python3-pip

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY ./Storage

ENTRYPOINT ["python3"]

CMD["storage.py"]