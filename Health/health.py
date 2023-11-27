import connexion
from connexion import NoContent
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import logging.config
import yaml
import datetime
import json
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread
from sqlalchemy import and_
import time
import os
import requests

output = {
    "receiver": "",
    "storage": "",
    "processing": "",
    "audit": "",
    "last_update": "",
}

services = ['receiver', 'storage', 'processing', 'audit']

def health_check():
    while True:
        for service in services:
            try:
                response = requests.get(f"http://benny-3855.eastus2.cloudapp.azure.com/{service}/health", timeout=5)
                if response.status_code == 200:
                    output[service] = "running"
                else:
                    output[service] = "down"
            except:
                output[service] = "down"
        output["last_update"] = time.strftime("%Y-%m-%d %H:%M:%S")
        save_to_json(output, "health_check_output.json")
        time.sleep(20)

def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)    

app = connexion.FlaskApp(__name__, specification_dir='')

if __name__ == "__main__":
    app.run(port=8120)