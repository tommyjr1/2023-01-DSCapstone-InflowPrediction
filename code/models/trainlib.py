import pandas as pd


def lagndelay(num_lags, delay, df, y):
    df.sort_index(ascending=False, inplace=True)

    for column in df:
        for lag in range(1, num_lags+1):
            df[column + '_lag' + str(lag)] = df[column].shift(lag*-1-(delay-1))
            df[column + '_avg_window_length' + str(lag+1)] = df[column].shift(-1-(
                delay-1)).rolling(window=lag+1, center=False).mean().shift(1-(lag+1))

    df.dropna(inplace=True)
    df.sort_index(inplace=True)

    mask = (df.columns.str.contains(y) | df.columns.str.contains(
        'lag') | df.columns.str.contains('window'))
    df_processed = df[df.columns[mask]]
    return df_processed


def scale(scaler, df):
    scaled_data = scaler.fit_transform(df)
    df_scaled = pd.DataFrame(
        data=scaled_data, columns=df.columns, index=df.index.values)
    df_scaled.reset_index(drop=True, inplace=True)
    return df_scaled


def split(ratio, df):
    df_train = df.iloc[:int(df.shape[0]*ratio), :]
    df_test = df.iloc[int(df.shape[0]*ratio):, :]
    return df_train, df_test
