import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import datetime
from typing import List

from data.Storage import Storage

PATH_TO_GRAPHS = "./static/graphs/"
PATH_TO_MODEL = "./model/pipe.pkl"
class Estimator:
    def __init__(self, storage : Storage):
        self.storage = storage
        self.pipe = pickle.load(open(PATH_TO_MODEL, 'rb'))
    
    def forecast(self, city : int, days : int) -> tuple:
        temp_day = np.array(self.storage.get_data_for_city(city)).astype(np.float64)
        temp_evening = np.array(self.storage.get_data_evening_for_city(city)).astype(np.float64)

        last_date_in_db = self.storage.get_last_date()
        last_date_dt_in_db = self.storage.db_str_to_datetime(last_date_in_db)

        first_pred_dt = last_date_dt_in_db + datetime.timedelta(days=1)
        pred_dates = [
            self.storage.datetime_to_str(first_pred_dt + datetime.timedelta(days=day))
            for day in range(days)]

        pred_w_day = []
        for _ in range(days):
            pred = self.pipe.predict(temp_day.reshape(1,-1))
            temp_day = np.append(temp_day, round(pred[0],2))
            temp_day = np.delete(temp_day, 0)
            pred_w_day.append( round(pred[0],2) )

        pred_w_evening = []
        for _ in range(days):
            pred = self.pipe.predict(temp_evening.reshape(1,-1))
            temp_evening = np.append(temp_evening, round(pred[0],2))
            temp_evening = np.delete(temp_evening, 0)
            pred_w_evening.append( round(pred[0],2) )

        # plotting
        true_dates = list(reversed([
            last_date_dt_in_db - datetime.timedelta(days=day)
            for day in range(7)]))
        temp_day = np.array(self.storage.get_data_for_city(city)).astype(np.float64)
        temp_evening = np.array(self.storage.get_data_evening_for_city(city)).astype(np.float64)

        self.plot_weather(true_dates , temp_day, pred_w_day, temp_evening, pred_w_evening, city)
        
        return pred_dates, pred_w_day, pred_w_evening
        

    def get_detailed_stats(self, city) -> List[str]:
        day_temp_for_last_7_days = np.array(self.storage.get_measures_for_city_k_days("day", city, 7)).astype(np.float64)
        day_temp_for_last_30_days = np.array(self.storage.get_measures_for_city_k_days("day", city, 30)).astype(np.float64)

        evening_temp_for_last_7_days = np.array(self.storage.get_measures_for_city_k_days("evening", city, 7)).astype(np.float64)
        evening_temp_for_last_30_days = np.array(self.storage.get_measures_for_city_k_days("evening", city, 30)).astype(np.float64)

        stats = [
            f"Средняя температура днём за последние 7 дней : {round(day_temp_for_last_7_days.mean(), ndigits=1)} °C",
            f"Стандартное отклонение днём за последние 7 дней : {round(day_temp_for_last_7_days.std(), ndigits=1)} °C",
            f"Средняя температура вечером за последние 7 дней : {round(evening_temp_for_last_7_days.mean(), ndigits=1)} °C",
            f"Стандартное отклонение вечером за последние 7 дней : {round(evening_temp_for_last_7_days.std(), ndigits=1)} °C",
            f"Средняя температура днём за последние 30 дней : {round(day_temp_for_last_30_days.mean(), ndigits=1)} °C",
            f"Стандартное отклонение днём за последние 30 дней : {round(day_temp_for_last_30_days.std(), ndigits=1)} °C",
            f"Средняя температура вечером за последние 30 дней : {round(evening_temp_for_last_30_days.mean(), ndigits=1)} °C",
            f"Стандартное отклонение вечером за последние 30 дней : {round(evening_temp_for_last_30_days.std(), ndigits=1)} °C",
        ]

        return stats


    def plot_weather(self, days_true, weather_true_day, weather_pred_day,
                     weather_true_evening, weather_pred_evening, city_id):

        last = days_true[-1] # последняя дата для непрерывного графика
        days_pred = [last] #  
        weather_pred_day.insert(0, weather_true_day[-1]) # добавить в прогнозы последнее значение для непрерывного графика
        for i in range(len(weather_pred_day)-1):
            days_pred.append(last + datetime.timedelta(1))
            last = days_pred[-1]

        weather_pred_evening.insert(0, weather_true_evening[-1])
        
        city_name = self.storage.get_city_by_id(city_id)
        sns.set_context("poster")
        plt.figure(figsize = (16, 9))
        plt.title(f'{city_name}')
        
        sns.lineplot(x = days_true, y = weather_true_day, label = 'Дневная температура')
        sns.lineplot(x = days_pred, y = weather_pred_day, color = 'red', label = 'Дневной прогноз')

        sns.lineplot(x = days_true, y = weather_true_evening, color= 'magenta', label = 'Вечерняя температура')
        sns.lineplot(x = days_pred, y = weather_pred_evening, color = 'orange', label = 'Вечерний прогноз')
        plt.xlabel('Дата')
        plt.ylabel('Температруа в °C')
        plt.tick_params(axis = 'x' , labelrotation = 45)
        plt.savefig(PATH_TO_GRAPHS + "estimator_graph.png")
