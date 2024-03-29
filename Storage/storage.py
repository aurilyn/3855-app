import connexion
from connexion import NoContent
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from augment import Augment
from unit import Unit
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


DB_ENGINE = create_engine(f"mysql+pymysql://{app_config['datastore']['user']}:{app_config['datastore']['password']}@"
    f"{app_config['datastore']['hostname']}:{app_config['datastore']['port']}/"
    f"{app_config['datastore']['db']}")

Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)


def post_augment_stats(body):

    logger.info(f"Connecting to DB. Hostname:{app_config['datastore']['hostname']}, port: {app_config['datastore']['port']}")

    session = DB_SESSION()

    aug = Augment(body['augment_id'],
                  body['name'],
                  body['rarity'],
                  body['placement'],
                  body['stage_picked'],
                  body['winrate'],
                  body['trace_id'])
    
    session.add(aug)

    session.commit()
    session.close()

    logger.debug(f"Stored event Augment request with a trace id of {body['trace_id']}")

    return NoContent, 201

def post_units(body):

    logger.info(f"Connecting to DB. Hostname:{app_config['datastore']['hostname']}, port: {app_config['datastore']['port']}")

    session = DB_SESSION()

    unit = Unit(body['unit_id'],
                  body['name'],
                  body['buy_cost'],
                  body['sell_cost'],
                  body['rarity'],
                  body['ability_name'],
                  body['stars'],
                  body['trace_id'])
    
    session.add(unit)

    session.commit()
    session.close()
    
    logger.debug(f"Stored Event Unit request with trace id of {body['trace_id']}")

    return NoContent, 201
 
def get_augment_stats(start_timestamp, end_timestamp):
    session = DB_SESSION()

    start_timestamp_datetime = datetime.datetime.strptime(start_timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')

    end_timestamp_datetime = datetime.datetime.strptime(end_timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
    
    augment_list = session.query(Augment).filter(and_(Augment.date_created >= start_timestamp_datetime,
                                                 Augment.date_created <= end_timestamp_datetime))

    result = []

    for augment in augment_list:
        result.append(augment.to_dict())

    session.close()

    logger.info("Query for Augments after %s returns %d results" % (start_timestamp, len(result)))

    return result, 200

def get_units(start_timestamp, end_timestamp):
    session = DB_SESSION()

    start_timestamp_datetime = datetime.datetime.strptime(start_timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')

    end_timestamp_datetime = datetime.datetime.strptime(end_timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')

    unit_list = session.query(Unit).filter(and_(Unit.date_created >= start_timestamp_datetime,
                                           Unit.date_created <= end_timestamp_datetime))

    result = []

    for unit in unit_list:
        result.append(unit.to_dict())

    session.close()

    logger.info("Query for Units after %s returns %d results" % (start_timestamp, len(result)))

    return result, 200

def process_messages():
    hostname = "%s:%d" % (app_config['events']['hostname'],
                          app_config['events']['port'])
    max_retries = 100
    current_retries = 0
    while current_retries < max_retries:
        logger.info(f"Attempting to connect to Kafka, current retry count is {current_retries}")
        try:
            client = KafkaClient(hosts=hostname)
            topic = client.topics[str.encode(app_config['events']['topic'])]
            logger.info("Connected to Kafka")
            break
        except Exception as e:
            logger.error(f"Connection to Kafka failed: {e}")
            current_retries += 1
            time.sleep(app_config['scheduler']['period_sec'])
    consumer = topic.get_simple_consumer(consumer_group=b'event_group',
                                         reset_offset_on_start=False,
                                         auto_offset_reset=OffsetType.LATEST)

    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        logger.info("Message: %s" % msg)
        
        payload = msg['payload']

        session = DB_SESSION()

        if msg['type'] == "augment":
            logger.info(f"Received the following augment payload: {payload}")
            aug = Augment(payload['augment_id'],
                    payload['name'],
                    payload['rarity'],
                    payload['placement'],
                    payload['stage_picked'],
                    payload['winrate'],
                    payload['trace_id'])
        
            session.add(aug)

            session.commit()
            session.close()

        elif msg['type'] == "unit":
            logger.info(f"Received the following unit payload: {payload}")
            unit = Unit(payload['unit_id'],
                  payload['name'],
                  payload['buy_cost'],
                  payload['sell_cost'],
                  payload['rarity'],
                  payload['ability_name'],
                  payload['stars'],
                  payload['trace_id'])
    
            session.add(unit)

            session.commit()
            session.close()
        consumer.commit_offsets()

def health():
    return 200

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("api.yml", base_path="/storage", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090)