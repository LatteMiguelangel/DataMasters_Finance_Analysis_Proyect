def calculate_rolling_mean(df, column, window):
    df[f'{column}_rolling_mean_{window}'] = df[column].rolling(window=window).mean()
    return df
