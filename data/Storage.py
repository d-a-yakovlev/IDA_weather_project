import errno
import os
import sys
import sqlite3
import pandas
import datetime

DB_NAME = "data/weather.db"
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
            SELECT id, name
            FROM cities
        '''

        cities_tup = self.cur.execute(query).fetchall()
        id_cities = [t[0] for t in cities_tup]
        cities = [t[1].split(',')[0] for t in cities_tup]
        return id_cities, cities
    
    def get_data_for_city(self, city):
        query = f'''
            SELECT day
            FROM temperature
            WHERE INTEGER = {city}
            ORDER BY date DESC
            LIMIT 7
        '''

        temps_day_tup = self.cur.execute(query).fetchall()
        temps = [t[0] for t in temps_day_tup]
        return list(reversed(temps))
    
    def get_last_date(self):
        query = '''
            SELECT date
            FROM temperature
            ORDER BY date DESC
            LIMIT 1
        '''

        return [t[0] for t in self.cur.execute(query).fetchall()][0]
    
    
    def db_str_to_datetime_str(self, str_date : str):
        splitted_str = str_date.split('/')
        for i in range(len(splitted_str)):
            splitted_str[i] = f"{int(splitted_str[i]):02}"
            
        return '/'.join(splitted_str)
        
    def db_str_to_datetime(self, str_date : str):
        datetime_str = self.db_str_to_datetime_str(str_date)
        return datetime.datetime.strptime(datetime_str, '%Y/%m/%d')


