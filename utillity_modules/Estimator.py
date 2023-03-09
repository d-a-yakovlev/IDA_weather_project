import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import List

from data.Storage import Storage

PATH_TO_GRAPHS = "./static/graphs/"
class Estimator:
    def __init__(self, city : str, storage : Storage):
        self.city = city
        self.storage = storage

        self.data = self.storage.get_data_for_city(city)

    
    def forecast(self, days : int, save_graph=True) -> list:
        pass
    
    def get_stats(self) -> List[str]:
        pass

    def get_detailed_stats(self) -> List[str]:
        pass
