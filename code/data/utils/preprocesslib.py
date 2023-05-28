import pandas as pd
import numpy as np
import os


def merge(dam_file, weather_file, output_name):
    dam = pd.read_csv(f'./data/{dam_file}.csv',
                      index_col='시간', encoding="utf-8-sig")
    dam.index = pd.to_datetime(dam.index)

    weather = pd.read_csv(
        f'./data/{weather_file}.csv', index_col='일시', encoding="utf-8-sig")
    weather.index = pd.to_datetime(weather.index)
    df = pd.concat([dam, weather], axis=1)
    df.dropna(inplace=True)
    df.to_csv(f'./data/{output_name}.csv', encoding="utf-8-sig")


def generate_cyclical_features(df, col_name, period, start_num=0):
    kwargs = {
        f'sin_{col_name}': lambda x: np.sin(2*np.pi*(df[col_name]-start_num)/period),
        f'cos_{col_name}': lambda x: np.cos(2*np.pi*(df[col_name]-start_num)/period)
    }
    return df.assign(**kwargs).drop(columns=[col_name])


def preprocessDam(file_name):
    data = pd.read_csv(f'./data/{file_name}.csv',
                       encoding="utf-8-sig", index_col='시간')
    data.index = pd.to_datetime(data.index)

    # data['1일후유입량'] = data['당일유입량'][1:].reset_index()['당일유입량']
    # data['2일후유입량'] = data['당일유입량'][2:].reset_index()['당일유입량']
    # 저수위(현재),저수량(현재),저수위(예년),저수량(예년), 예년누계강우량,강우량전일,금년누계강우량
    data['저수위변화'] = data['저수위(현재)'] - data['저수위(예년)']
    data['저수량변화'] = data['저수량(현재)'] - data['저수량(예년)']
    data['강우변화'] = data['금년누계강우량'] - data['예년누계강우량']

    mask = data.columns.str.contains('발전') | data.columns.str.contains('전년') | data.columns.str.contains(
        '방류') | data.columns.str.contains('연간') | data.columns.str.contains('강우량')
    data = data[[x for x in data.columns if x not in data.columns[mask]]]

    df_date = data.assign(month=data.index.month).assign(
        day_of_week=data.index.dayofweek).assign(week_of_year=data.index.isocalendar().week)
    df_date = generate_cyclical_features(df_date, 'day_of_week', 7, 0)
    df_date = generate_cyclical_features(df_date, 'month', 12, 1)
    df_date = generate_cyclical_features(df_date, 'week_of_year', 52, 0)

    df_date.to_csv(f'./data/{file_name}_forTrain.csv', encoding="utf-8-sig")


def preprocessWeather(file_name):
    data = pd.read_csv(f'./data/{file_name}.csv', encoding="utf-8-sig")
    data['1일후강수량'] = data['강수량(mm)'][1:].reset_index()['강수량(mm)']
    data['2일후강수량'] = data['강수량(mm)'][2:].reset_index()['강수량(mm)']
    data = data.iloc[:-2,]

    data.to_csv(f'./data/{file_name}_forTrain.csv',
                index=False, encoding="utf-8-sig")
