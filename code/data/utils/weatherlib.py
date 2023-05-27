import pandas as pd
import numpy as np
import os


def concat(startY, endY):
    data_files = os.listdir("./data/합천군_종상기상관측")
    data_files.sort()
    year = range(startY, endY+1)
    data = pd.DataFrame()
    for name in year:
        df = pd.read_csv(
            f"./data/합천군_종상기상관측/기상청데이터_{str(name)}.csv", encoding="cp949")
        data = pd.concat([data, df])
    data.drop(["지면상태(지면상태코드)", "현상번호(국내식)", "운형(운형약어)", "일사(MJ/m2)", "3시간신적설(cm)",
              "5cm 지중온도(°C)", "10cm 지중온도(°C)", "20cm 지중온도(°C)", "30cm 지중온도(°C)", '전운량(10분위)', '중하층운량(10분위)', '풍향(16방위)', '지점', '지점명'], axis=1, inplace=True)
    data.drop(
        list(data.columns[data.columns.str.contains("QC플래그")]), axis=1, inplace=True)

    data['일시'] = pd.to_datetime(data["일시"])
    data = data.set_index(keys='일시')
    data.sort_index(inplace=True)

    for feature in data.columns[1:]:
        data[feature] = data[feature].astype(float)

    data = data.resample(rule='H').mean()
    data.interpolate(method='linear', inplace=True)
    data.ffill(inplace=True)
    data.bfill(inplace=True)
    data.to_csv(f"./data/종상기상관측_전체.csv", encoding="utf-8-sig")

    data_daily = data.resample(rule='D').mean()
    data_daily.to_csv(f"./data/종상기상관측_전체_일별.csv", encoding="utf-8-sig")
