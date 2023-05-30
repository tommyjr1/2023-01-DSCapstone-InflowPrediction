import pandas as pd
import numpy as np
import os

from sklearn.preprocessing import MinMaxScaler

from utils.preprocesslib import merge, preprocessDam, preprocessWeather, merge, pca, scalenvif

if __name__ == '__main__':
    # merge('합천다목적댐_전체_일별', '종상기상관측_전체_일별', '합천_댐기상종합')
    # preprocessDam('합천다목적댐_전체_일별')
    dam_file = '합천다목적댐_전체_일별_forTrain'
    # preprocessWeather('종상기상관측_전체_일별')
    weather_file = '종상기상관측_전체_일별_forTrain'
    # merge(dam_file, weather_file, '합천_댐기상종합_forTrain4')
    scaler = MinMaxScaler()
    scalenvif('합천_댐기상종합_forTrain4', scaler, 0)
    # pca('합천_댐기상종합_forTrain4_scaled', 3)
