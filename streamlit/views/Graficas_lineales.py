import plotly.graph_objects as go
import pandas as pd
import streamlit as st
def Graficas_lineales(datasets):
    
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
                name=f'{company} Precio más alto',
                line=dict(color=base_color, width=3),  # Línea sólida
                marker=dict(size=8)
            ))

            # Añadir traza para los precios mínimos (color con opacidad moderada)
            fig.add_trace(go.Scatter(
                x=yearly_low.index,
                y=yearly_low,
                mode='lines+markers',
                name=f'{company} Precio más bajo',
                line=dict(color=hex_to_rgba(base_color, 0.6), width=2),  # Línea más transparente
                marker=dict(size=8)
            ))

    # Configuración del layout
    fig.update_layout(
        title="Precios Máximos y Mínimos Anuales de las Grandes Compañías Tecnológicas",
        xaxis_title='Año',
        yaxis_title='Precio (USD)',
        legend_title='Acciones',
        template='plotly_white',
        font=dict(family='Arial', size=16, color='#023047')
    )

    # Mostrar la gráfica en Streamlit
    st.title("Análisis de Precios Anuales Máximos y Mínimos de Empresas Tecnológicas")
    st.plotly_chart(fig)
    fig = go.Figure()

    st.divider()
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
                name=f'{company} Precio de Apertura',
                line=dict(color=hex_to_rgba(base_color, 0.6), width=2),  # Menos opacidad
                marker=dict(size=8)
            ))
            
            # Añadir traza para los precios de cierre (color original)
            fig.add_trace(go.Scatter(
                x=yearly_close.index,
                y=yearly_close,
                mode='lines+markers',
                name=f'{company} Precio de Cierre',
                line=dict(color=base_color, width=3),  # Color sólido
                marker=dict(size=8)
            ))

    # Configuración del layout
    fig.update_layout(
        title="Precios Anuales de Apertura y Cierre de las Grandes Compañías Tecnológicas",
        xaxis_title='Año',
        yaxis_title='Precio (USD)',
        legend_title='Acciones',
        template='plotly_white',
        font=dict(family='Arial', size=16, color='#023047')
    )

    # Mostrar la gráfica en Streamlit
    st.title("Análisis de Precios Anuales de Apertura y Cierre de Empresas Tecnológicas")
    st.plotly_chart(fig)

    st.divider()

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
                name=f'{company}',
                increasing_line_color=colors.get(company, '#000000'),
                decreasing_line_color=hex_to_rgba(colors.get(company, '#000000'), 0.6),
                increasing_fillcolor=colors.get(company, '#000000'),
                decreasing_fillcolor=hex_to_rgba(colors.get(company, '#000000'), 0.6)
            ))

    # Configuración del layout
    fig.update_layout(
        title="Precios Máximos y Mínimos Anuales de las Grandes Compañías Tecnológicas",
        xaxis_title='Año',
        yaxis_title='Precio (USD)',
        legend_title='Acciones',
        template='plotly_white',
        font=dict(family='Arial', size=16, color='#023047'),
        xaxis_rangeslider_visible=False 
    )

    # Mostrar la gráfica en Streamlit
    st.title("Gráfico de Velas Japonesas de Apertura y Cierre de Empresas Tecnológicas")
    st.plotly_chart(fig)

    st.divider()

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
        title='Volumen Anual de Acciones de las Grandes Compañías Tecnológicas',
        xaxis_title='Año',
        yaxis_title='Volumen de las Acciones',
        legend_title='Companías',
        template='plotly_white',
        font=dict(family='Arial', size=16, color='#023047')
    )

    # Mostrar el gráfico en Streamlit
    st.title("Volumen Anual de Acciones de las Grandes Compañías Tecnológicas")
    st.plotly_chart(fig)

    st.divider()

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
        title='Ganancias Acumulativas entre las Grandes Compañías Tecnológicas',
        xaxis_title='Fecha',
        yaxis_title='Ganancias Acumulativas',
        template='plotly_white',
        font=dict(family='Arial', size=16, color='#023047'),
        legend_title='Companies'
    )

    # Mostrar el gráfico en Streamlit
    st.title("Ganancias Acumulativas de las Grandes Compañías Tecnológicas")
    st.plotly_chart(fig)

    st.divider()

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
                name=f'{company}',
                line=dict(color=colors.get(company, '#636EFA'))  # Asignar color único o predeterminado
            ))

    # Configuración del layout
    fig.update_layout(
        title='Volatibilidad Mensual de las Grandes Compañias Tecnológicas',
        xaxis_title='Mes',
        yaxis_title='Desviación Estándar (Volatibilidad)',
        template='plotly_white',
        font=dict(family='Arial', size=16, color='#023047')
    )
    # Mostrar el gráfico en Streamlit
    st.title("Volatibilidad Mensual de las Grandes Compañias Tecnológicas")
    st.plotly_chart(fig)