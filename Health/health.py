import connexion
from connexion import NoContent
from datetime import datetime
import logging.config
import json
import time
import requests
import logging
from apscheduler.schedulers.background import BackgroundScheduler
import yaml

output = {
    "receiver": "",
    "storage": "",
    "processing": "",
    "audit": "",
    "last_update": "",
}

app_conf_file = "app_conf.yml"

with open(app_conf_file, 'r') as f:
    app_config = yaml.safe_load(f.read())

logger = logging.getLogger('basicLogger')

services = ['receiver', 'storage', 'processing', 'audit']

def health_check():
    for service in services:
        logger.info(f"Attempting to get health check from {service}")
        try:
            response = requests.get(f"http://benny-3855.eastus2.cloudapp.azure.com/{service}/health", timeout=5)
            if response.status_code == 200:
                logger.info(f"{service} is running")
                output[service] = "running"
            else:
                logger.warning(f"{service} is down")
                output[service] = "down"
        except:
            output[service] = "down"
    output["last_update"] = time.strftime("%Y-%m-%d %H:%M:%S")
    save_to_json(output, "health_check_output.json")
    return output, 200

def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(health_check,
                'interval',
                seconds=app_config['scheduler']['period_sec'])
    sched.start()

app = connexion.FlaskApp(__name__, specification_dir='')

app.add_api("api.yml", base_path="/health", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    init_scheduler()
    app.run(port=8120)