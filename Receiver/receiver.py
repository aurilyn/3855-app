import connexion
from connexion import NoContent
import requests
import yaml
import logging
import logging.config
import uuid
import datetime
import json
import time
from pykafka import KafkaClient
import os

if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
    print("In Test Environment")
    app_conf_file = "/config/app_conf.yml"
    log_conf_file = "/config/log_conf.yml"
else:
    print("In Dev Environment")
    app_conf_file = "app_conf.yml"
    log_conf_file = "log_conf.yml"

with open(app_conf_file, 'r') as f:
    app_config = yaml.safe_load(f.read())

# External Logging Configuration
with open(log_conf_file, 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

logger.info("App Conf File: %s" % app_conf_file)
logger.info("Log Conf File: %s" % log_conf_file)

headers = {"Content-Type": 'application/json; charset=utf-8'}
hostname = "%s:%d" % (app_config['events']['hostname'], app_config['events']['port'])    

max_retries = 100
current_retries = 0
while current_retries < max_retries:
    logger.info(f"Attempting to connect to Kafka, current retry count is {current_retries}")
    try:
        client = KafkaClient(hosts=hostname)
        topic = client.topics[str.encode(app_config['events']['topic'])]
        producer = topic.get_sync_producer()
        logger.info("Connected to Kafka")
        break
    except Exception as e:
        logger.error(f"Connection to Kafka failed: {e}")
        current_retries += 1
        time.sleep(app_config['scheduler']['period_sec'])

def post_augment_stats(body):
    body["trace_id"] = str(uuid.uuid4())
    
    logger.info(f"Created with the following trace id: {body['trace_id']}")
    
    msg = { "type": "augment",
            "datetime":
                datetime.datetime.now().strftime(
                    "%Y-%m-%dT%H:%M:%S"),
            "payload": body }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    logger.info(f"{body['trace_id']} received")


    return NoContent, 201

def post_units(body):

    body['trace_id'] = str(uuid.uuid4())

    logger.info(f"Created with the following trace id: {body['trace_id']}")

    msg = { "type": "unit",
            "datetime":
                datetime.datetime.now().strftime(
                    "%Y-%m-%dT%H:%M:%S"),
            "payload": body }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    logger.info(f"{body['trace_id']} received")

    return NoContent, 201
 

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("api.yml", base_path="/receiver", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    app.run(port=8080)