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

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')


def get_augment_stats(index):
    hostname = "%s:%d" % (app_config['events']['hostname'],
                          app_config['events']['port'])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config['events']['topic'])]
    
    consumer = topic.get_simple_consumer(reset_offset_on_start=True,
                                         consumer_timeout_ms=1000)
    
    logger.info("Retrieving augment at index %d" % index)

    message_count = 0

    try:
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)

            if msg['type'] == 'augment':
                if message_count == index:
                    return { "message": msg }, 200
                else:
                    message_count += 1
    
    except:
        logger.error("No more messages found")

    logger.error("Could not find augment at index %d" % index)
    return { "message": "Not found" }, 404

def get_units(index):
    hostname = "%s:%d" % (app_config['events']['hostname'],
                          app_config['events']['port'])
    client = KafkaClient(hosts=hostname)

    topic = client.topics[str.encode(app_config['events']['topic'])]
    
    consumer = topic.get_simple_consumer(reset_offset_on_start=True,
                                         consumer_timeout_ms=1000)
    
    logger.info("Retrieving unit at index %d" % index)

    message_count = 0

    try:
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
            
            if msg['type'] == 'unit':
                if message_count == index:
                    return { "message": msg }, 200
                else:
                    message_count += 1
  
    except:
        logger.error("No more messages found")

    logger.error("Could not find unit at index %d" % index)
    return { "message": "Not found" }, 404

app = connexion.FlaskApp(__name__, specification_dir='')

app.add_api("api.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    app.run(port=8110, use_reloader=False)