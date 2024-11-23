import pandas as pd
import streamlit as st
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import seaborn as sns

st.set_page_config(
    page_title="Data Analysis",
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

colors = {
    'Sony': '#4285F4', 
    'IBM': '#6c3483', 
    'Google': '#EA4335', 
    'Microsoft': '#F14F21', 
    'Amazon': '#d68910', 
    'Nvidia': '#34A853', 
    'Samsung': '#1428A0',
    'Apple': '#B5B5B5'
}

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

#mostrar df
st.title("Comportamiento de las Acciones de las Empresas Big Tech")
st.write("""
### Samsung Dataset
Esta tabla contiene las acciones de **Samsung** convertidas a dólares del **2000 al 2022**.
""")
st.dataframe(samsung_df.sort_values('date', ascending=True))
st.divider()
st.write("""
### Apple Dataset
Esta tabla contiene las acciones de **Apple** convertidas a dólares del **2000 al 2022**.
""")
st.dataframe(apple_df.sort_values('date', ascending=True))

st.header("""
Modulo de Estadísticas Descriptivas
""")
st.write("""
        #### Distribución de Datos
""")
datasets = {'Samsung': samsung_df, 'Apple': apple_df, 'Amazon': amazon_df, 'Microsotf':microsoft_df, 'Nvidia': nvidia_df, 'Google': google_df, 'Sony': sony_df, 'IBM': ibm_df}
for company, data in datasets.items():
    # Excluir la columna 'date' y calcular las estadísticas descriptivas
    st.write(f"Estadísticas para {company}:")
    st.write(data.drop(columns=['date']).describe())

st.divider()

st.write("""
        #### Análisis de Volatilidad
""")

for company, data in datasets.items():
    data['daily_range'] = data['high'] - data['low']
    data['daily_pct_change'] = (data['close'] - data['open']) / data['open'] * 100
    st.write(f"Resumen de volatilidad para {company}:\n")
    st.write(data[['daily_range', 'daily_pct_change']].describe())
    
st.write("""
        #### Análisis de Correlación de Variables por Compañía
""")
for company, data in datasets.items():
    # Filtrar solo las columnas numéricas
    numeric_data = data.select_dtypes(include='number')
    
    if numeric_data.empty:
        st.subheader(f"{company}: No hay datos numéricos disponibles para calcular la correlación.")
        continue

    # Calcular la matriz de correlación
    correlation_matrix = numeric_data.corr()

    # Crear el heatmap con Seaborn
    fig, ax = plt.subplots(figsize=(8, 6))  # Tamaño ajustable para cada gráfico
    sns.set_style('whitegrid')
    sns.heatmap(correlation_matrix, annot=True, cmap='magma', ax=ax)
    ax.set_title(f'Correlación de variables para {company}')

    # Mostrar el gráfico en Streamlit
    st.subheader(f"Matriz de Correlación: {company}")
    st.pyplot(fig)
    
    combined_data = pd.DataFrame()
###################################
# Encabezado de la aplicación
st.title("Análisis de Correlación Global entre Empresas")

# Combinar los precios ajustados de cierre en un solo DataFrame
st.header("Generando Datos Combinados")
combined_data = pd.DataFrame()
combined_data = combined_data.dropna()

for company, data in datasets.items():
    data['date'] = pd.to_datetime(data['date'])
    data = data.set_index('date')  # Asegurar que las fechas sean el índice
    combined_data[company] = data['volume']  # Agregar la columna adj_close por empresa

# Mostrar datos combinados si el usuario lo desea
if st.checkbox("Mostrar datos combinados"):
    st.write(combined_data)

# Eliminar fechas donde falten datos para alguna empresa
combined_data.dropna(inplace=True)

# Calcular la matriz de correlación
correlation_matrix = combined_data.corr()

# Visualizar la matriz de correlación
st.header("Matriz de Correlación entre el Volumen de las Compañías")
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='magma', fmt=".2f", linewidths=0.5, ax=ax)
ax.set_title("Matriz de Correlación entre el Volumen de las Compañías", fontsize=16)

# Renderizar la gráfica en Streamlit
st.pyplot(fig)


