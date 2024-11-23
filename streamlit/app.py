import pandas as pd
import streamlit as st
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import seaborn as sns
import plotly.express as px

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
    
st.write("""#### Análisis de Correlación de Variables por Compañía""")

for company, data in datasets.items():
    # Filtrar solo las columnas numéricas
    numeric_data = data.select_dtypes(include='number')
    
    if numeric_data.empty:
        st.subheader(f"{company}: No hay datos numéricos disponibles para calcular la correlación.")
        continue

    # Calcular la matriz de correlación
    correlation_matrix = numeric_data.corr()

    # Convertir la matriz en un formato largo para Plotly
    correlation_long = correlation_matrix.reset_index().melt(id_vars='index')
    correlation_long.columns = ['Variable 1', 'Variable 2', 'Correlación']

    # Crear el heatmap con Plotly
    fig = px.imshow(
        correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.index,
        color_continuous_scale='magma',
        text_auto='.2f',
        labels=dict(color='Correlación'),
        title=f'Matriz de Correlación: {company}',
    )
    
    # Ajustar el diseño
    fig.update_layout(
        width=600,
        height=500,
        xaxis_title="Variables",
        yaxis_title="Variables",
        margin=dict(l=50, r=50, t=50, b=50),
        font=dict(family="Arial", size=12),
    )
    
    # Mostrar el gráfico en Streamlit
    st.subheader(f"Matriz de Correlación: {company}")
    st.plotly_chart(fig)


# Encabezado de la aplicación
st.title("Análisis de Correlación Global entre Empresas")

# Combinar los volúmenes en un solo DataFrame
st.header("Generando Datos Combinados")
combined_data = pd.DataFrame()
combined_data = combined_data.dropna()
for company, data in datasets.items():
    data['date'] = pd.to_datetime(data['date'])
    data = data.set_index('date')  # Asegurar que las fechas sean el índice
    combined_data[company] = data['volume']  # Agregar la columna 'volume' por empresa

# Mostrar datos combinados si el usuario lo desea
if st.checkbox("Mostrar datos combinados"):
    st.write(combined_data)

# Eliminar fechas donde falten datos para alguna empresa
combined_data.dropna(inplace=True)

# Calcular la matriz de correlación
correlation_matrix = combined_data.corr()

# Visualizar la matriz de correlación con Plotly
st.header("Matriz de Correlación entre el Volumen de las Compañías")

fig = px.imshow(
    correlation_matrix.values,
    x=correlation_matrix.columns,
    y=correlation_matrix.index,
    color_continuous_scale='magma',
    text_auto='.2f',
    labels=dict(color='Correlación'),
    title="Matriz de Correlación entre el Volumen de las Compañías",
)

# Personalizar el diseño del gráfico
fig.update_layout(
    width=800,
    height=600,
    xaxis_title="Compañías",
    yaxis_title="Compañías",
    margin=dict(l=50, r=50, t=50, b=50),
    font=dict(family="Arial", size=12),
)

# Mostrar la gráfica en Streamlit
st.plotly_chart(fig)


# Función para convertir colores HEX a RGBA con opacidad
def hex_to_rgba(hex_color, alpha=1.0):
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return f'rgba({r}, {g}, {b}, {alpha})'



# Inicialización de la figura
fig = go.Figure()

# Iterar sobre cada empresa en datasets
for company, data in datasets.items():
    if 'high' in data.columns and 'low' in data.columns and 'date' in data.columns:
        # Convertir la columna de fechas
        data['date'] = pd.to_datetime(data['date'])
        
        # Cálculo de máximos y mínimos anuales
        yearly_high = data.groupby(data['date'].dt.year)['high'].max()
        yearly_low = data.groupby(data['date'].dt.year)['low'].min()

        # Obtener color base
        base_color = colors.get(company, '#000000')  # Negro como valor predeterminado

        # Añadir traza para los precios máximos (color sólido)
        fig.add_trace(go.Scatter(
            x=yearly_high.index,
            y=yearly_high,
            mode='lines+markers',
            name=f'{company} Highest Price',
            line=dict(color=base_color, width=3),  # Línea sólida
            marker=dict(size=8)
        ))

        # Añadir traza para los precios mínimos (color con opacidad moderada)
        fig.add_trace(go.Scatter(
            x=yearly_low.index,
            y=yearly_low,
            mode='lines+markers',
            name=f'{company} Lowest Price',
            line=dict(color=hex_to_rgba(base_color, 0.6), width=2),  # Línea más transparente
            marker=dict(size=8)
        ))

# Configuración del layout
fig.update_layout(
    title="Yearly High and Low Prices of Big Tech Companies",
    xaxis_title='Year',
    yaxis_title='Price (USD)',
    legend_title='Stocks',
    template='plotly_white',
    font=dict(family='Arial', size=16, color='#023047')
)

# Mostrar la gráfica en Streamlit
st.title("Análisis de Precios Anuales Máximos y Mínimos de Empresas Tecnológicas")
st.plotly_chart(fig)



fig = go.Figure()

# Iterar sobre cada empresa en datasets
for company, data in datasets.items():
    if 'open' in data.columns and 'close' in data.columns and 'date' in data.columns:
        # Convertir la columna de fechas
        data['date'] = pd.to_datetime(data['date'])
        
        # Cálculo de precios anuales de apertura y cierre
        yearly_open = data.groupby(data['date'].dt.year)['open'].first()
        yearly_close = data.groupby(data['date'].dt.year)['close'].last()

        # Obtener color base
        base_color = colors.get(company, '#000000')  # Negro como valor predeterminado
        
        # Añadir traza para los precios de apertura (color con opacidad moderada)
        fig.add_trace(go.Scatter(
            x=yearly_open.index,
            y=yearly_open,
            mode='lines+markers',
            name=f'{company} Open Price',
            line=dict(color=hex_to_rgba(base_color, 0.6), width=2),  # Menos opacidad
            marker=dict(size=8)
        ))
        
        # Añadir traza para los precios de cierre (color original)
        fig.add_trace(go.Scatter(
            x=yearly_close.index,
            y=yearly_close,
            mode='lines+markers',
            name=f'{company} Close Price',
            line=dict(color=base_color, width=3),  # Color sólido
            marker=dict(size=8)
        ))

# Configuración del layout
fig.update_layout(
    title="Yearly Open and Close Prices of Big Tech Companies",
    xaxis_title='Year',
    yaxis_title='Price (USD)',
    legend_title='Stocks',
    template='plotly_white',
    font=dict(family='Arial', size=16, color='#023047')
)

# Mostrar la gráfica en Streamlit
st.title("Análisis de Precios Anuales de Apertura y Cierre de Empresas Tecnológicas")
st.plotly_chart(fig)


fig = go.Figure()

# Iterar sobre cada empresa en datasets
for company, data in datasets.items():
    if 'high' in data.columns and 'low' in data.columns and 'date' in data.columns:
        # Convertir la columna de fechas
        data['date'] = pd.to_datetime(data['date'])
        
        # Cálculo de los máximos y mínimos anuales
        yearly_high = data.groupby(data['date'].dt.year)['high'].max()
        yearly_low = data.groupby(data['date'].dt.year)['low'].min()

        # Crear el gráfico de velas usando solo high y low
        fig.add_trace(go.Candlestick(
            x=yearly_high.index,
            open=yearly_high,  # Usamos 'high' como valor de apertura
            high=yearly_high,  # También como valor más alto
            low=yearly_low,    # Usamos 'low' como valor mínimo
            close=yearly_low,  # Y como valor de cierre
            name=f'{company} High-Low Candlestick',
            increasing_line_color=colors.get(company, '#000000'),
            decreasing_line_color=hex_to_rgba(colors.get(company, '#000000'), 0.6),
            increasing_fillcolor=colors.get(company, '#000000'),
            decreasing_fillcolor=hex_to_rgba(colors.get(company, '#000000'), 0.6)
        ))

# Configuración del layout
fig.update_layout(
    title="Yearly High and Low Prices of Big Tech Companies",
    xaxis_title='Year',
    yaxis_title='Price (USD)',
    legend_title='Stocks',
    template='plotly_white',
    font=dict(family='Arial', size=16, color='#023047'),
    xaxis_rangeslider_visible=False 
)

# Mostrar la gráfica en Streamlit
st.title("Gráfico de Velas Japonesas de Apertura y Cierre de Empresas Tecnológicas")
st.plotly_chart(fig)



fig = go.Figure()

# Iterar sobre cada empresa en datasets
for company, data in datasets.items():
    if 'volume' in data.columns and 'date' in data.columns:
        # Convertir la columna 'date' a formato datetime si no lo está
        data['date'] = pd.to_datetime(data['date'])
        
        # Cálculo del volumen anual
        yearly_volume = data.groupby(data['date'].dt.year)['volume'].sum()
        
        # Añadir traza al gráfico
        fig.add_trace(go.Scatter(
            x=yearly_volume.index,
            y=yearly_volume,
            mode='lines+markers',
            name=company,
            line=dict(color=colors.get(company, None)),  # Color único para cada empresa
            marker=dict(size=4)
        ))

# Configuración del layout
fig.update_layout(
    title='Annual Stock Volume Across Big Tech Companies',
    xaxis_title='Year',
    yaxis_title='Stock Volume',
    legend_title='Companies',
    template='plotly_white',
    font=dict(family='Arial', size=16, color='#023047')
)

# Mostrar el gráfico en Streamlit
st.title("Annual Stock Volume of Big Tech Companies")
st.plotly_chart(fig)



fig = go.Figure()

# Iterar sobre cada empresa en datasets
for company, data in datasets.items():
    if 'adj_close' in data.columns and 'date' in data.columns:
        # Convertir la columna 'date' a formato datetime si no lo está
        data['date'] = pd.to_datetime(data['date'])
        
        # Calcular el rendimiento acumulativo de 'adj_close'
        cumulative_return = data['adj_close'].pct_change().fillna(0).add(1).cumprod()
        
        # Añadir traza para el rendimiento acumulado de cada empresa
        fig.add_trace(go.Scatter(
            x=data['date'],
            y=cumulative_return,
            mode='lines',
            name=company,
            line=dict(color=colors.get(company, None))  # Color único para cada empresa
        ))

# Configuración del layout
fig.update_layout(
    title='Cumulative Returns Across Big Tech Companies',
    xaxis_title='Date',
    yaxis_title='Cumulative Return',
    template='plotly_white',
    font=dict(family='Arial', size=16, color='#023047'),
    legend_title='Companies'
)

# Mostrar el gráfico en Streamlit
st.title("Cumulative Returns of Big Tech Companies")
st.plotly_chart(fig)


fig = go.Figure()

# Iterar sobre las empresas en los datasets
for company, data in datasets.items():
    if 'adj_close' in data.columns and 'date' in data.columns:
        # Calcular la volatilidad mensual (desviación estándar de los precios ajustados de cierre)
        volatility = data.groupby(data['date'].dt.to_period('M'))['adj_close'].std()

        # Añadir traza al gráfico para cada empresa
        fig.add_trace(go.Scatter(
            x=volatility.index.to_timestamp(),  # Convertir el índice de periodo a timestamp
            y=volatility,
            mode='lines',
            name=f'{company} Volatility',
            line=dict(color=colors.get(company, '#636EFA'))  # Asignar color único o predeterminado
        ))

# Configuración del layout
fig.update_layout(
    title='Monthly Volatility of Big Tech Companies',
    xaxis_title='Month',
    yaxis_title='Standard Deviation (Volatility)',
    template='plotly_white',
    font=dict(family='Arial', size=16, color='#023047')
)

# Mostrar el gráfico en Streamlit
st.title("Monthly Volatility of Big Tech Companies")
st.plotly_chart(fig)