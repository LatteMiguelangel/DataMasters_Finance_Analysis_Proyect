import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Samsung vs Apple",
    page_icon="📊",
    layout="centered"
)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


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

samsung_df['Date'] = samsung_df['Date'].dt.strftime('%Y/%m/%d')
apple_df['Date'] = apple_df['Date'].dt.strftime('%Y/%m/%d')
won_to_usd_00_17_df['DATE'] = won_to_usd_00_17_df['DATE'].dt.strftime('%Y/%m/%d')
won_to_usd_04_22_df['Date'] = won_to_usd_04_22_df['Date'].dt.strftime('%Y/%m/%d')


#renombrado de columnas
samsung_df.rename(columns={'Date': 'date', 'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Adj Close': 'adj_close', 'Volume': 'volume'}, inplace=True)
apple_df.rename(columns={'Date': 'date', 'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Adj Close': 'adj_close', 'Volume': 'volume'}, inplace=True)
won_to_usd_00_17_df.rename(columns={'DATE': 'date', 'DEXKOUS': 'dollar'}, inplace=True)
won_to_usd_04_22_df.rename(columns={'Date': 'date', 'KRW=X': 'dollar'}, inplace=True)

# ----- definición de índice --------
# samsung_df.set_index('date', inplace=True)
# apple_df.set_index('date', inplace=True)
# won_to_usd_00_17_df.set_index('date', inplace=True)
# won_to_usd_04_22_df.set_index('date', inplace=True)


#print(samsung_df.head())
#print('\n\n\n-----------------------------------------\n\n')
#print(apple_df.head())

#print(won_to_usd_04_22_df.sort_values('dollar'))
#print('\n\n\n-----------------------------------------\n\n')
#print(won_to_usd_00_17_df.sort_values('dollar'))


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

# crear columna de year para ambos datasets
samsung_df['year'] = pd.DatetimeIndex(samsung_df['date']).year
apple_df['year'] = pd.DatetimeIndex(apple_df['date']).year

#rangos para evaluar acciones de apple
date_start = samsung_df['date'].min()
date_end = samsung_df['date'].max()
#definicion final de acciones de apple
apple_df = apple_df[(apple_df['date'] >= date_start) & (apple_df['date'] <= date_end)]


#mostrar df
st.title("Análisis Financiero: Samsung vs Apple")
st.write("""
### Samsung Dataset
Esta tabla contiene las acciones de **Samsung** convertidas a dólares del **2000 al 2022**.
""")
st.dataframe(samsung_df.sort_values('date', ascending=True).reset_index(drop=True, inplace=False))
st.divider()
st.write("""
### Apple Dataset
Esta tabla contiene las acciones de **Apple** convertidas a dólares del **2000 al 2022**.
""")
st.dataframe(apple_df.sort_values('date', ascending=True).reset_index(drop=True, inplace=False))




# Gráfico interactivo
# company = st.selectbox("Selecciona una empresa", ["Samsung", "Apple"])
# if company == "Samsung":
#     st.line_chart(samsung_df[['year', 'volume']].set_index('year'))
# else:
#     st.line_chart(apple_df[['year', 'volume']].set_index('year'))