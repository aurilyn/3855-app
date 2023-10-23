import mysql.connector
import yaml
with open('app_conf.yml', 'r') as f:
    db_config = yaml.safe_load(f.read())
db_conn = mysql.connector.connect(host=db_config['datastore']['hostname'], user=db_config['datastore']['user'], password=db_config['datastore']['password'], database=db_config['datastore']['db'])

db_cursor = db_conn.cursor()
db_cursor.execute('''
DROP TABLE augment, unit
''')
db_conn.commit()
db_conn.close()