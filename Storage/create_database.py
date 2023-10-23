import sqlite3

conn = sqlite3.connect('tft.sqlite')

c = conn.cursor()

c.execute('''
          CREATE TABLE augment
          (id INTEGER PRIMARY KEY ASC,
           augment_id VARCHAR(250) NOT NULL,
           name VARCHAR(250) NOT NULL,
           rarity INTEGER NOT NULL,
           placement INTEGER NOT NULL,
           stage_picked VARCHAR(100) NOT NULL,
           winrate INTEGER NOT NULL,
           trace_id VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
        ''')

c.execute('''
            CREATE TABLE unit
            (id INTEGER PRIMARY KEY ASC, 
            unit_id VARCHAR(250) NOT NULL,
            name VARCHAR(250) NOT NULL,
            buy_cost INTEGER NOT NULL,
            sell_cost INTEGER NOT NULL,
            rarity VARCHAR(100) NOT NULL,
            ability_name VARCHAR(100) NOT NULL,
            stars INTEGER NOT NULL,
            trace_id VARCHAR(100) NOT NULL,
            date_created VARCHAR(100) NOT NULL)
        ''')

conn.commit()
conn.close()