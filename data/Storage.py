import errno
import os
import sys
import sqlite3

DB_NAME = "weather_db"
class Storage:
    def __init__(self):
        if not os.path.exists(DB_NAME):
            raise FileNotFoundError(
                errno.ENOENT, 
                os.strerror(errno.ENOENT), 
                DB_NAME
            )
        
        self.conn = sqlite3.connect(DB_NAME) 
        self.cur = self.conn.cursor()

    def __del__(self):
        if os.path.exists(DB_NAME):
            self.conn.close()

    def get_cities(self):
        query = '''
            SELECT city_name
            FROM cities
        '''

        cities = [t[0] for t in self.cur.execute(query).fetchall()]
        return cities


