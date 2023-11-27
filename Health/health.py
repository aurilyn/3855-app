import connexion
from connexion import NoContent
from datetime import datetime
import logging.config
import json
from sqlalchemy import and_
import time
import requests
from logging import logger

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
                logger.info(f"Attempting to get health check from {service}")
                response = requests.get(f"http://benny-3855.eastus2.cloudapp.azure.com/{service}/health", timeout=5)
                if response.status_code == 200:
                    output[service] = "running"
                    logger.info(f"{service} is running")
                else:
                    logger.warning(f"{service} is down")
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