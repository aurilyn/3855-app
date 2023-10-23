import sqlite3

conn = sqlite3.connect('tft.sqlite')

c = conn.cursor()
c.execute('''
          DROP TABLE augment
          ''')

conn.commit()
conn.close()
