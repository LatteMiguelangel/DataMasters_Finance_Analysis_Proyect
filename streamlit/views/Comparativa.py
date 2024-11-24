import plotly.graph_objects as go
import pandas as pd
import streamlit as st

def Comparativa(datasets):
    # Colores para cada empresa
    colors = {
        'Sony': '#1428A0',  
        'IBM': '#F180E6', 
        'Google': '#FBBC05', 
        'Microsoft': '#A51C30', 
        'Amazon': '#F44611', 
        'Nvidia': '#76B900', 
        'Samsung': '#4285F4',
        'Apple': '#B5B5B5'
    }

    # Función para convertir colores HEX a RGBA con opacidad
    def hex_to_rgba(hex_color, alpha=1.0):
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return f'rgba({r}, {g}, {b}, {alpha})'

    # Títulos y descripción inicial de la vista
    st.title("📊 Comparativa General entre las Empresas Big Tech")
    st.markdown(
        """
        Bienvenido al panel de análisis interactivo. Aquí encontrarás un análisis visual detallado de las principales métricas de las grandes empresas tecnológicas:
        
        - **Gráfico de Velas Japonesas**: Visualización de máximos y mínimos anuales.
        - **Ganancias Acumulativas**: Seguimiento del rendimiento de las acciones a lo largo del tiempo.
        - **Volatilidad Mensual**: Medida de la estabilidad de las acciones.
        """
    )
    st.divider()

    ### GRÁFICO 1: Velas Japonesas ###
    st.subheader("📈 Gráfico de Velas Japonesas")
    st.markdown(
        """
        El gráfico de velas japonesas muestra las fluctuaciones de precios máximos y mínimos anuales de las acciones de las empresas cargadas.
        """
    )

    fig = go.Figure()

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
                name=f'{company}',
                increasing_line_color=colors.get(company, '#000000'),
                decreasing_line_color=hex_to_rgba(colors.get(company, '#000000'), 0.6),
                increasing_fillcolor=colors.get(company, '#000000'),
                decreasing_fillcolor=hex_to_rgba(colors.get(company, '#000000'), 0.6)
            ))

    fig.update_layout(
        title="Precios Máximos y Mínimos Anuales de las Grandes Compañías Tecnológicas",
        xaxis_title='Año',
        yaxis_title='Precio (USD)',
        legend_title='Acciones',
        template='plotly_white',
        font=dict(family='Arial', size=16, color='#023047'),
        xaxis_rangeslider_visible=False
    )

    st.plotly_chart(fig)
    st.divider()

    ### GRÁFICO 2: Ganancias Acumulativas ###
    st.subheader("📈 Ganancias Acumulativas")
    st.markdown(
        """
        Este gráfico muestra las ganancias acumulativas de las acciones, indicando el rendimiento relativo desde el inicio del período de análisis.
        """
    )

    fig = go.Figure()

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

    fig.update_layout(
        title='Ganancias Acumulativas entre las Grandes Compañías Tecnológicas',
        xaxis_title='Fecha',
        yaxis_title='Ganancias Acumulativas',
        template='plotly_white',
        font=dict(family='Arial', size=16, color='#023047'),
        legend_title='Compañías'
    )

    st.plotly_chart(fig)
    st.divider()

    ### GRÁFICO 3: Volatilidad Mensual ###
    st.subheader("📉 Volatilidad Mensual")
    st.markdown(
        """
        La volatilidad mensual mide la variación o inestabilidad de los precios de las acciones. Una alta volatilidad puede indicar mayor riesgo y oportunidad en el mercado.
        """
    )

    fig = go.Figure()

    for company, data in datasets.items():
        if 'adj_close' in data.columns and 'date' in data.columns:
            # Calcular la volatilidad mensual (desviación estándar de los precios ajustados de cierre)
            volatility = data.groupby(data['date'].dt.to_period('M'))['adj_close'].std()

            # Añadir traza al gráfico para cada empresa
            fig.add_trace(go.Scatter(
                x=volatility.index.to_timestamp(),  # Convertir el índice de periodo a timestamp
                y=volatility,
                mode='lines',
                name=f'{company}',
                line=dict(color=colors.get(company, '#636EFA'))  # Asignar color único o predeterminado
            ))

    fig.update_layout(
        title='Volatilidad Mensual de las Grandes Compañías Tecnológicas',
        xaxis_title='Mes',
        yaxis_title='Desviación Estándar (Volatilidad)',
        template='plotly_white',
        font=dict(family='Arial', size=16, color='#023047')
    )

    st.plotly_chart(fig)