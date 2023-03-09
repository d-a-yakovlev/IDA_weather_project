import geopandas

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from data.Storage import Storage

PATH_TO_GRAPHS = "./static/graphs/"
class GeoPainter:
    def __init__(self, predictions : list, city : str, days : int, storage : Storage):
        self.predictions = predictions
        self.city = city
        self.days = days
        self.storage = storage

    def draw() -> None:
        pass
