import connexion
from connexion import NoContent
import requests
import yaml
import logging
import logging.config
import uuid
import datetime
import json
from pykafka import KafkaClient

headers = {"Content-Type": 'application/json; charset=utf-8'}
    
with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

def post_augment_stats(body):
    body["trace_id"] = str(uuid.uuid4())
    
    logger.info(f"Created with the following trace id: {body['trace_id']}")

    client = KafkaClient(hosts=f"{app_config['events']['hostname']}:{app_config['events']['port']}")
    topic = client.topics[str.encode(app_config['events']['topic'])]
    producer = topic.get_sync_producer()

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

    client = KafkaClient(hosts=f"{app_config['events']['hostname']}:{app_config['events']['port']}")
    topic = client.topics[str.encode(app_config['events']['topic'])]
    producer = topic.get_sync_producer()

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
app.add_api("api.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    app.run(port=8080)