import geopandas as gpd
from datetime import datetime, timedelta
import shapely
import numpy as np
import pandas as pd
import shapefile as shp
import matplotlib.pyplot as plt
#import seaborn as sns
from geopandas.tools import geocode
import folium

from data.Storage import Storage

PATH_TO_TEMPLATES = "./templates/"
class GeoPainter:
    def __init__(self, storage : Storage):
        self.storage = storage

        self.last_date = self.storage.get_last_date()
        self.pre_last_date = self.storage.datetime_to_str(
            self.storage.db_str_to_datetime(self.storage.get_last_date()) - timedelta(days=1)
        )
        self.cities = pd.read_sql('SELECT * FROM cities', con=storage.conn ,index_col = 'id')
        self.tempC = pd.read_sql(f"""SELECT * FROM temperature""", con=storage.conn, index_col = 'id')

    def paint(self) -> None:
        def city_name(str):
            str = str[:str.find(', ')]
            k = str.find('(')
            if k != -1:
                str = str[:k]
            return str

        for x in self.cities.index:
            self.cities.iat[x, 0] = city_name(self.cities.iat[x, 0])

        def index_by_name(str):
            return self.cities[self.cities['name'] == str].index.to_list()[0]

        def temp_by_day(cit):
            cityid = index_by_name(cit)

            ret = self.tempC.loc[(self.tempC['INTEGER'] == cityid)
                                  & (self.tempC['date'] == self.tempC[self.tempC['INTEGER'] == cityid].date.max()),
                                  ['day','evening']]
            #print(ret)
            return ret
        
        tmp = self.cities.values.tolist()
        df = pd.DataFrame({'cityname' : tmp})

        def color_by_temp(val):
            colors = ['darkblue', 'blue', 'lightblue', 'pink', 'lightred', 'red',  'darkred']
            t_min = -30.0
            t_max = 30.0
            if val < t_min:
                val = t_min
            elif val > t_max:
                val = t_max
            i = int((val + t_max)/8.57)
            return colors[i]

        def custom_geocoder(address):
            dataframe = geocode(address , provider="nominatim", user_agent = 'my_request')
            point = dataframe.geometry.iloc[0]
            return pd.Series({'Latitude': point.y, 'Longitude': point.x})
        
        df[['latitude', 'longitude']] =  df.cityname.apply(lambda x: custom_geocoder(x))
        mapit = folium.Map(location=[53.198627, 50.113987], zoom_start = 2)
        
        mydate = self.last_date
        mydate_m1 = self.pre_last_date
        #print(mydate)
        for index, row in df.iterrows():
            vcity, lat, lon = row['cityname'][0], row['latitude'], row['longitude']

            t1 = temp_by_day(vcity).iat[0,0]
            t2 = temp_by_day(vcity).iat[0,1]
            hcol = 'pink'
            if t1 is None:
                st1 = "—"
            else:
                t1 = float(t1)
                st1 = str(t1) + '°C'
                hcol = color_by_temp(t1)
                #print(hcol)
            if t2 is None:
                st2 = "—"
            else:
                st2 = str(t2) + '°C'
            html = '''{city}<br>Днём: {t1}<br>Вечером: {t2}'''.format(city = vcity, t1 = st1, t2 = st2)
            iframe = folium.IFrame(html, width = 200, height = 80)
            popup = folium.Popup(iframe,  max_width = 200)
            folium.Marker( location=[ lat,lon ], icon = folium.Icon(color=hcol, icon_color='white', icon = 'cloud'), radius = 8, popup = popup ).add_to( mapit )

        mapit.save(PATH_TO_TEMPLATES + "weather_data_color.html")
