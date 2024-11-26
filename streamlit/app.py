import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from views.Datasets import Datasets
from views.Comparativa import Comparativa
from views.Avanzado import Avanzado
from views.Hitos import Hitos
from config import config
import openpyxl

config() #configuracion streamlit

#lectura de datasets
samsung_df = pd.read_csv('data/raw/SSNG.csv', delimiter=',')
apple_df = pd.read_csv('data/raw/AAPL.csv', delimiter=',')
amazon_df = pd.read_csv('data/raw/AMZN.csv', delimiter=',')
microsoft_df = pd.read_csv('data/raw/MSFT.csv', delimiter=',')
nvidia_df = pd.read_csv('data/raw/NVDA.csv', delimiter=',')
google_df = pd.read_csv('data/raw/GOOG.csv', delimiter=',')
sony_df = pd.read_csv('data/raw/SONY.csv', delimiter=',')
ibm_df = pd.read_csv('data/raw/IBM.csv', delimiter=',')
won_to_usd_00_17_df = pd.read_csv('data/raw/KRW_TO_USD_2000-2017.csv', delimiter=',')
won_to_usd_04_22_df = pd.read_csv('data/raw/KRW_TO_USD_2004-2022.csv', delimiter=',')
won_to_usd_04_22_df = won_to_usd_04_22_df[['Date', 'KRW=X']]

#eliminar filas con valores nulos
samsung_df = samsung_df.dropna()
apple_df = apple_df.dropna()
amazon_df = amazon_df.dropna()
microsoft_df = microsoft_df.dropna()
nvidia_df = nvidia_df.dropna()
google_df = google_df.dropna()
sony_df = sony_df.dropna()
ibm_df = ibm_df.dropna()
won_to_usd_00_17_df = won_to_usd_00_17_df.dropna()
won_to_usd_04_22_df = won_to_usd_04_22_df.dropna()

won_to_usd_00_17_df = won_to_usd_00_17_df[won_to_usd_00_17_df['DEXKOUS'] != '.']
won_to_usd_04_22_df = won_to_usd_04_22_df[won_to_usd_04_22_df['KRW=X'] != '.']

#formateando las columnas de fechas
samsung_df['Date'] = pd.to_datetime(samsung_df['Date'])
apple_df['Date'] = pd.to_datetime(apple_df['Date'])
amazon_df['Date'] = pd.to_datetime(amazon_df['Date'])
microsoft_df['Date'] = pd.to_datetime(microsoft_df['Date'], format='%m/%d/%Y')
nvidia_df['Date'] = pd.to_datetime(nvidia_df['Date'])
google_df['Date'] = pd.to_datetime(google_df['Date'])
sony_df['Date'] = pd.to_datetime(sony_df['Date'])
ibm_df['Date'] = pd.to_datetime(ibm_df['Date'])
won_to_usd_00_17_df['DATE'] = pd.to_datetime(won_to_usd_00_17_df['DATE'])
won_to_usd_04_22_df['Date'] = pd.to_datetime(won_to_usd_04_22_df['Date'])

samsung_df['Date'] = samsung_df['Date'].dt.strftime('%Y/%m/%d')
apple_df['Date'] = apple_df['Date'].dt.strftime('%Y/%m/%d')
won_to_usd_00_17_df['DATE'] = won_to_usd_00_17_df['DATE'].dt.strftime('%Y/%m/%d')
won_to_usd_04_22_df['Date'] = won_to_usd_04_22_df['Date'].dt.strftime('%Y/%m/%d')

#renombrado de columnas
samsung_df.rename(columns={'Date': 'date', 'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Adj Close': 'adj_close', 'Volume': 'volume'}, inplace=True)
apple_df.rename(columns={'Date': 'date', 'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Adj Close': 'adj_close', 'Volume': 'volume'}, inplace=True)
amazon_df.rename(columns={'Date': 'date', 'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Adj Close': 'adj_close', 'Volume': 'volume'}, inplace=True)
microsoft_df.rename(columns={'Date': 'date', 'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Adj Close': 'adj_close', 'Volume': 'volume'}, inplace=True)
nvidia_df.rename(columns={'Date': 'date', 'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Adj Close': 'adj_close', 'Volume': 'volume'}, inplace=True)
google_df.rename(columns={'Date': 'date', 'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Adj Close': 'adj_close', 'Volume': 'volume'}, inplace=True)
sony_df.rename(columns={'Date': 'date', 'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Adj Close': 'adj_close', 'Volume': 'volume'}, inplace=True)
ibm_df.rename(columns={'Date': 'date', 'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Adj Close': 'adj_close', 'Volume': 'volume'}, inplace=True)
won_to_usd_00_17_df.rename(columns={'DATE': 'date', 'DEXKOUS': 'dollar'}, inplace=True)
won_to_usd_04_22_df.rename(columns={'Date': 'date', 'KRW=X': 'dollar'}, inplace=True)

#combinar datasets de valores de conversion entre dolar y won coreano
combined_dollar_values = pd.concat([won_to_usd_00_17_df, won_to_usd_04_22_df])
combined_dollar_values = combined_dollar_values.drop_duplicates(subset='date')

#agregar columna de conversion de won a dolar
samsung_df['usd_to_won'] = samsung_df['date'].map(combined_dollar_values.set_index('date')['dollar'])

#filtrar filas con volumen 0 y eliminar filas con valores nulos
samsung_df = samsung_df[samsung_df['volume'] != 0]
samsung_df = samsung_df.dropna()

#convertir valores de won a dolar en la tabla de samsung
samsung_df['open'] = samsung_df.apply(lambda x: float(x['open']) / float(x['usd_to_won']), axis=1)
samsung_df['high'] = samsung_df.apply(lambda x: float(x['high']) / float(x['usd_to_won']), axis=1)
samsung_df['low'] = samsung_df.apply(lambda x: float(x['low']) / float(x['usd_to_won']), axis=1)
samsung_df['close'] = samsung_df.apply(lambda x: float(x['close']) / float(x['usd_to_won']), axis=1)
samsung_df['adj_close'] = samsung_df.apply(lambda x: float(x['adj_close']) / float(x['usd_to_won']), axis=1)


#2022-05-23 -> 23 de Mayo del 2022
#2000-02-01 -> 2 de Febrero del 2000
START = samsung_df['date'].min() 
END = samsung_df['date'].max() 
apple_df = apple_df[(apple_df['date'] >= START) & (apple_df['date'] <= END)]
amazon_df = amazon_df[(amazon_df['date'] >= START) & (amazon_df['date'] <= END)]
microsoft_df = microsoft_df[(microsoft_df['date'] >= START) & (microsoft_df['date'] <= END)]
nvidia_df = nvidia_df[(nvidia_df['date'] >= START) & (nvidia_df['date'] <= END)]
google_df = google_df[(google_df['date'] >= START) & (google_df['date'] <= END)]
sony_df = sony_df[(sony_df['date'] >= START) & (sony_df['date'] <= END)]
ibm_df = ibm_df[(ibm_df['date'] >= START) & (ibm_df['date'] <= END)]

#Reseteo de indices
samsung_df.reset_index(drop=True, inplace=True)
apple_df.reset_index(drop=True, inplace=True)
amazon_df.reset_index(drop=True, inplace=True)
microsoft_df.reset_index(drop=True, inplace=True)
nvidia_df.reset_index(drop=True, inplace=True)
google_df.reset_index(drop=True, inplace=True)
sony_df.reset_index(drop=True, inplace=True)
ibm_df.reset_index(drop=True, inplace=True)

datasets = {'Samsung': samsung_df, 'Apple': apple_df, 'Amazon': amazon_df, 'Microsoft':microsoft_df, 'Nvidia': nvidia_df, 'Google': google_df, 'Sony': sony_df, 'IBM': ibm_df}
datasets = dict(sorted(datasets.items(), key=lambda item: item[0]))
with st.sidebar:
    selected = option_menu(
        menu_title='Menu',
        options=['Datasets', 'Comparativa Global', 'Comparativa Avanzada', 'Hitos Relevantes'],
        menu_icon='cast',
        default_index=0     
    )

if selected == 'Datasets':
    Datasets(datasets)
if selected == 'Comparativa Global':
    Comparativa(datasets)
if selected == 'Comparativa Avanzada':
    Avanzado(datasets)
if selected == 'Hitos Relevantes':
    Hitos(datasets)