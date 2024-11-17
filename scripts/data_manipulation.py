import pandas as pd
import streamlit as st

#lectura de datasets
samsung_df = pd.read_csv('data/raw/SSNG.csv', delimiter=',')
apple_df = pd.read_csv('data/raw/AAPL.csv', delimiter=',')
won_to_usd_00_17_df = pd.read_csv('data/raw/KRW_TO_USD_2000-2017.csv', delimiter=',')
won_to_usd_04_22_df = pd.read_csv('data/raw/KRW_TO_USD_2004-2022.csv', delimiter=',')
won_to_usd_04_22_df = won_to_usd_04_22_df[['Date', 'KRW=X']]

#eliminar filas con valores nulos
samsung_df = samsung_df.dropna()
apple_df = apple_df.dropna()
won_to_usd_00_17_df = won_to_usd_00_17_df.dropna()
won_to_usd_04_22_df = won_to_usd_04_22_df.dropna()

won_to_usd_00_17_df = won_to_usd_00_17_df[won_to_usd_00_17_df['DEXKOUS'] != '.']
won_to_usd_04_22_df = won_to_usd_04_22_df[won_to_usd_04_22_df['KRW=X'] != '.']


#formateando las columnas de fechas
samsung_df['Date'] = pd.to_datetime(samsung_df['Date'])
apple_df['Date'] = pd.to_datetime(apple_df['Date'])
won_to_usd_00_17_df['DATE'] = pd.to_datetime(won_to_usd_00_17_df['DATE'])
won_to_usd_04_22_df['Date'] = pd.to_datetime(won_to_usd_04_22_df['Date'])

samsung_df['Date'] = samsung_df['Date'].dt.strftime('%d-%m-%Y')
apple_df['Date'] = apple_df['Date'].dt.strftime('%d-%m-%Y')
won_to_usd_00_17_df['DATE'] = won_to_usd_00_17_df['DATE'].dt.strftime('%d-%m-%Y')
won_to_usd_04_22_df['Date'] = won_to_usd_04_22_df['Date'].dt.strftime('%d-%m-%Y')


#renombrado de columnas
samsung_df.rename(columns={'Date': 'date', 'Open': 'samsung_open', 'High': 'samsung_high', 'Low': 'samsung_low', 'Close': 'samsung_close', 'Adj Close': 'samsung_adj_close', 'Volume': 'samsung_volume'}, inplace=True)
apple_df.rename(columns={'Date': 'date', 'Open': 'apple_open', 'High': 'apple_high', 'Low': 'apple_low', 'Close': 'apple_close', 'Adj Close': 'apple_adj_close', 'Volume': 'apple_volume'}, inplace=True)
won_to_usd_00_17_df.rename(columns={'DATE': 'date', 'DEXKOUS': 'dollar'}, inplace=True)
won_to_usd_04_22_df.rename(columns={'Date': 'date', 'KRW=X': 'dollar'}, inplace=True)

# ----- definición de índice --------
# samsung_df.set_index('date', inplace=True)
# apple_df.set_index('date', inplace=True)
# won_to_usd_00_17_df.set_index('date', inplace=True)
# won_to_usd_04_22_df.set_index('date', inplace=True)

#mostrar datasets
#print(samsung_df.head())
#print('\n\n\n-----------------------------------------\n\n')
#print(apple_df.head())

#print(won_to_usd_04_22_df.sort_values('dollar'))
#print('\n\n\n-----------------------------------------\n\n')
#print(won_to_usd_00_17_df.sort_values('dollar'))


#combinar datasets de valores de conversion entre dolar y won coreano
combined_dollar_values = pd.concat([won_to_usd_00_17_df, won_to_usd_04_22_df])
combined_dollar_values = combined_dollar_values.drop_duplicates(subset='date')
#print(combined_dollar_values)
st.dataframe(combined_dollar_values)