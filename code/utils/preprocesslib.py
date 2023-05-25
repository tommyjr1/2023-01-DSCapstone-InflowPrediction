import pandas as pd
import numpy as np
import os


def merge(dam_file, weather_file, output_name):
    dam = pd.read_csv(f'../data/{dam_file}.csv', index_col='시간')
    dam.index = pd.to_datetime(dam.index)

    weather = pd.read_csv(f'../data/{weather_file}.csv', index_col='일시')
    weather.index = pd.to_datetime(weather.index)
    df = pd.concat([dam, weather], axis=1)
    df.dropna(inplace=True)
    df.to_csv(f'../data/{output_name}.csv')


def generate_cyclical_features(df, col_name, period, start_num=0):
    kwargs = {
        f'sin_{col_name}': lambda x: np.sin(2*np.pi*(df[col_name]-start_num)/period),
        f'cos_{col_name}': lambda x: np.cos(2*np.pi*(df[col_name]-start_num)/period)
    }
    return df.assign(**kwargs).drop(columns=[col_name])


def preprocessDam(file_name):
    data = pd.read_csv(f'../data/{file_name}.csv')
    data['1일후유입량'] = data['당일유입량'][1:].reset_index()['당일유입량']
    data['2일후유입량'] = data['당일유입량'][2:].reset_index()['당일유입량']

    data = data[['시간', '저수량(현재)', '전일방류량(본댐)',
                 '당일유입량', '전일유입량', '1일후유입량', '2일후유입량', '홍수기']]
    data = data.iloc[:-2,]

    data.set_index('시간')
    data.index = pd.to_datetime(data.index)

    df_date = data.assign(month=data.index.month).assign(
        day_of_week=data.index.dayofweek).assign(week_of_year=data.index.isocalendar().week)
    df_date = generate_cyclical_features(df_date, 'day_of_week', 7, 0)
    df_date = generate_cyclical_features(df_date, 'month', 12, 1)
    df_date = generate_cyclical_features(df_date, 'week_of_year', 52, 0)

    df_date.to_csv(f'../data/{file_name}_forTrain.csv', index=False)


def preprocessWeather(file_name):
    data = pd.read_csv(f'../data/{file_name}.csv')
    data = data[['일시', '기온(°C)', '강수량(mm)', '지면온도(°C)', '습도(%)']]
    data.to_csv(f'../data/{file_name}_forTrain.csv', index=False)
