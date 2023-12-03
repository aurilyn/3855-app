import logging.config
import datetime
import os
import json
import connexion
import yaml
from pykafka import KafkaClient
from flask_cors import CORS

if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
    print("In Test Environment")
    APP_CONF_FILE = "/config/app_conf.yml"
    LOG_CONF_FILE = "/config/log_conf.yml"
else:
    print("In Dev Environment")
    APP_CONF_FILE = "app_conf.yml"
    LOG_CONF_FILE = "log_conf.yml"

with open(APP_CONF_FILE, 'r') as f:
    app_config = yaml.safe_load(f.read())

# External Logging Configuration
with open(LOG_CONF_FILE, 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

logger.info("App Conf File: %s", APP_CONF_FILE)
logger.info("Log Conf File: %s", LOG_CONF_FILE)

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
                message_count += 1
    except:
        logger.error("No more messages found")
    logger.error("Could not find unit at index %d" % index)
    return { "message": "Not found" }, 404
def health():
    return 200
app = connexion.FlaskApp(__name__, specification_dir='')

if "TARGET_ENV" not in os.environ or os.environ["TARGET_ENV"] != "test":
    CORS(app.app)
    app.app.config['CORS_HEADER'] = 'Content-Type'
app.add_api("api.yml", base_path="/audit", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    app.run(port=8110, use_reloader=False)
