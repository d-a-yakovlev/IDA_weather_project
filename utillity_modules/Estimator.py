import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import sklearn
from typing import List

from data.Storage import Storage

PATH_TO_GRAPHS = "./static/graphs/"
PATH_TO_MODEL = "./model/pipe.pkl"
class Estimator:
    def __init__(self, storage : Storage):
        self.storage = storage
        self.pipe = pickle.load(open(PATH_TO_MODEL, 'rb'))
    
    def forecast(self, city : int, days : int) -> list:
        weather = np.array(self.storage.get_data_for_city(city))
        #weather = np.nan_to_num(last_date, nan=np.mean(weather))

        #last_date = self.storage.get_last_date()
        #last_date_dt = self.storage.db_str_to_datetime(last_date)
        #today_dt

        pred_w = []
        for _ in range(days):
            pred = self.pipe.predict(weather.reshape(1,-1))
            weather = np.append(weather, round(pred[0],2))
            weather = np.delete(weather, 0)
            pred_w.append( round(pred[0],2) )
        
        return pred_w
        
    
    def get_stats(self) -> List[str]:
        pass

    def get_detailed_stats(self) -> List[str]:
        pass
