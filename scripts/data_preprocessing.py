import pandas as pd

def load_and_clean_data(filepath, date_format):
    df = pd.read_csv(filepath)
    df['Date'] = pd.to_datetime(df['Date'], format=date_format)
    df = df.sort_values(by='Date')
    return df

def normalize_data(df, columns_to_scale, scaler):
    df[columns_to_scale] = scaler.fit_transform(df[columns_to_scale])
    return df
