import geopandas

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

PATH_TO_GRAPHS = "./static/graphs/"
class GeoPainter:
    def __init__(self, predictions, city, days):
        self.predictions = predictions
        self.city = city
        self.days = days

    def draw() -> None:
        pass
