import mysql.connector
import yaml
with open('app_conf.yml', 'r') as f:
    db_config = yaml.safe_load(f.read())
db_conn = mysql.connector.connect(host=db_config['datastore']['hostname'], user=db_config['datastore']['user'], password=db_config['datastore']['password'], database=db_config['datastore']['db'])

db_cursor = db_conn.cursor()

db_cursor.execute('''
        CREATE TABLE augment (
            id INT NOT NULL AUTO_INCREMENT,
            augment_id VARCHAR(250) NOT NULL,
            name VARCHAR(250) NOT NULL,
            rarity VARCHAR(100) NOT NULL,
            placement INTEGER NOT NULL,
            stage_picked VARCHAR(100) NOT NULL,
            winrate INTEGER NOT NULL,   
            trace_id VARCHAR(100) NOT NULL,
            date_created VARCHAR(100) NOT NULL,
            CONSTRAINT augment_pk PRIMARY KEY (id))
        ''')

db_cursor.execute('''
        CREATE TABLE unit (
            id INT NOT NULL AUTO_INCREMENT,
            unit_id VARCHAR(250) NOT NULL,
            name VARCHAR(250) NOT NULL,
            buy_cost INTEGER NOT NULL,
            sell_cost INTEGER NOT NULL,
            rarity VARCHAR(100) NOT NULL,
            ability_name VARCHAR(100) NOT NULL,
            stars INTEGER NOT NULL,
            trace_id VARCHAR(100) NOT NULL,
            date_created VARCHAR(100) NOT NULL,
            CONSTRAINT unit_pk PRIMARY KEY (id))
        ''')

db_conn.commit()
db_conn.close()