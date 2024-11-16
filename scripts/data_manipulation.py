import pandas as pd
#leer datasets
samsung_df = pd.read_csv('./data/raw/SSNG.csv', delimiter=';')
apple_df = pd.read_csv('./data/raw/AAPL.csv', delimiter=',')

#mostrar datasets
print(samsung_df.head())
print(apple_df.head())