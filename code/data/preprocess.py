import pandas as pd
import numpy as np
import os

from sklearn.preprocessing import MinMaxScaler

from utils.preprocesslib import merge, preprocessDam, preprocessWeather, merge, pca, scalenvif

if __name__ == '__main__':
    merge('합천다목적댐_전체_일별', '종상기상관측_전체_일별', '합천_댐기상종합_원본')
    preprocessDam('합천다목적댐_전체_일별')
    dam_file = '합천다목적댐_전체_일별_전처리'
    preprocessWeather('종상기상관측_전체_일별')
    weather_file = '종상기상관측_전체_일별_전처리'
    merge(dam_file, weather_file, '합천_댐기상종합_전처리')
    scaler = MinMaxScaler()
    scalenvif('합천_댐기상종합_전처리', scaler, 0)
    scalenvif('합천_댐기상종합_전처리', scaler, 1)

    # pca('합천_댐기상종합_forTrain4_scaled', 3)
