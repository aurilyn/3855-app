import connexion
from connexion import NoContent
from flask import jsonify
from datetime import datetime
import logging.config
import yaml
import datetime
import requests
from apscheduler.schedulers.background import BackgroundScheduler
import json
from flask_cors import CORS, cross_origin
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

def populate_stats():
    current_time = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    logger.info("Periodic processing has started")

    try:
        with open(app_config['datastore']['filename'], 'r') as f:
            data = json.load(f)
    except:
        data = {
            "highest_augment_placement": 0,
            "lowest_augment_placement": 0,
            "highest_champion_cost": 0,
            "lowest_champion_cost": 0,
            "total_augment": 0,
            "total_unit": 0,
            "total_amount_of_data": 0,
            "last_updated": "2023-10-10T09:30:15.448Z"
        }
        with open(app_config['datastore']['filename'], 'w') as f:
            json.dump(data, f, indent=4) 

    params = {
        'timestamp': data['last_updated']
    }

    augment_query = requests.get(app_config['eventstore1']['url'] + "?start_timestamp=" + data['last_updated'] + "&end_timestamp=" + current_time)
    unit_query = requests.get(app_config['eventstore2']['url'] + "?start_timestamp=" + data['last_updated'] + "&end_timestamp=" + current_time)
    if augment_query.status_code == 200:
        max_aug_placement = 0
        min_aug_placement = 0
        content_string = augment_query.content.decode('utf-8')
        content_json = json.loads(content_string)
        total_augment = len(content_json)
        for each in content_json:
            if each['placement'] > max_aug_placement:
                max_aug_placement = each['placement']
            if each['placement'] < min_aug_placement:
                min_aug_placement = each['placement']
        logger.info(f"Amount of augment data: {len(content_json)}")
    else:
        logger.error("Did not get a 200 response code")
    if unit_query.status_code == 200:
        max_unit_cost = 0
        min_unit_cost = 0
        content_string = unit_query.content.decode('utf-8')
        content_json = json.loads(content_string)
        total_unit = len(content_json)
        for each in content_json:
            if each['buy_cost'] > max_unit_cost:
                max_unit_cost = each['buy_cost']
            if each['buy_cost'] < min_unit_cost:
                min_unit_cost = each['buy_cost']
        logger.info(f"Amount of unit data: {len(content_json)}")
    else:
        logger.error("Did not get a 200 response code")
    data["highest_augment_placement"] = max_aug_placement
    data["lowest_augment_placement"] = min_aug_placement
    data["highest_champion_cost"] = max_unit_cost
    data["lowest_champion_cost"] = min_unit_cost
    data['total_augment'] += total_augment
    data['total_unit'] += total_unit
    data["total_amount_of_data"] += total_unit + total_augment
    data["last_updated"] = current_time
    logger.debug(data)
    with open(app_config['datastore']['filename'], 'w') as f:
        json.dump(data, f, indent=4)

    logger.info("Processing period has ended")

def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats,
                'interval',
                seconds=app_config['scheduler']['period_sec'])
    sched.start()

def get_stats():
    logger.info("Get request for stats has started")
    try:
        with open(app_config['datastore']['filename'], 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        logging.error("Statistic File is missing")
        return "Statistic do not exist", 404

    logging.debug(dict(data))
    logging.info("Get request completed")
    return dict(data), 200

app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADER'] = 'Content-Type'

app.add_api("api.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    init_scheduler()
    app.run(port=8100, use_reloader=False)
