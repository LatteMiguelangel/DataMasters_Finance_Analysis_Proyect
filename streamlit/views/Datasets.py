import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

def Datasets(datasets):
    # Título principal
    st.title("Comportamiento de las Acciones de las Empresas Big Tech")
    
    # Diccionario de enlaces
    links = {
        "IBM": "https://www.kaggle.com/datasets/zongaobian/microsoft-stock-data-and-key-affiliated-companies?select=VZ_daily_data.csv",
        "Sony": "https://www.kaggle.com/datasets/zongaobian/microsoft-stock-data-and-key-affiliated-companies?select=VZ_daily_data.csv",
        "Apple": "https://www.kaggle.com/datasets/henryshan/apple-stock-price",
        "Microsoft": "https://www.kaggle.com/datasets/prajwaldongre/microsoft-stock-price2000-2023",
        "Amazon": "https://www.kaggle.com/datasets/henryshan/amazon-com-inc-amzn",
        "Google": "https://www.kaggle.com/datasets/henryshan/google-stock-price",
        "Nvidia": "https://www.kaggle.com/datasets/programmerrdai/nvidia-stock-historical-data",
        "Samsung": "https://www.kaggle.com/datasets/ranugadisansagamage/samsung-stocks"
    }

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

    # Enlaces de conversión de USD a KRW
    usd_to_krw_links = [
        "https://www.kaggle.com/datasets/imtkaggleteam/dollar-vs-asian-currencies",
        "https://www.kaggle.com/datasets/biokpc/us-korean-exchange-rate"
    ]

    # Selector de dataset
    company_name = st.selectbox("Selecciona una empresa:", list(datasets.keys()))
    
    # Mostrar el dataset seleccionado
    selected_df = datasets[company_name]
    
    # Asegurarse de que 'date' es del tipo datetime
    selected_df['date'] = pd.to_datetime(selected_df['date'], errors='coerce')

    # Mostrar información sobre el dataset
    st.write(f"## {company_name} Dataset")
    st.write(f"Total de registros: {len(selected_df)}")
    st.write(f"Rango de fechas: {selected_df['date'].min().date()} - {selected_df['date'].max().date()}")
    
    # Mostrar enlaces
    st.markdown(f"**Link de Dataset**: {links[company_name]}")
    
    # Mostrar enlaces de conversión de USD a KRW solo si Samsung está seleccionado
    if company_name == "Samsung":
        st.markdown("###### Enlaces de Conversión USD a KRW:")
        for link in usd_to_krw_links:
            st.markdown(f"- {link}")

    # Selector de rango de fechas
    start_date, end_date = st.date_input(
        "Selecciona el rango de fechas:", 
        [selected_df['date'].min().date(), selected_df['date'].max().date()]
    )

    # Convertir start_date y end_date a datetime
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    filtered_df = selected_df[(selected_df['date'] >= start_date) & (selected_df['date'] <= end_date)]
    
    # Mostrar el dataframe filtrado
    st.dataframe(filtered_df.sort_values('date', ascending=True))
    
    st.divider()

    # Diccionario para las columnas a graficar
    columns_to_plot = {
        'open': 'Precio de Apertura',
        'high': 'Precio más Alto',
        'low': 'Precio más Bajo',
        'close': 'Precio de Cierre',
        'adj_close': 'Cierre Ajustado',
        'volume': 'Volumen'
    }
    
    # Selección de columna para graficar
    selected_column_key = st.selectbox("Selecciona el campo a visualizar:", list(columns_to_plot.keys()), format_func=lambda x: columns_to_plot[x])

    # Gráfico lineal
    linear_graphs(filtered_df, company_name, selected_column_key, colors[company_name], columns_to_plot)  # Pasar el color correspondiente

    # Calcular estadísticas descriptivas
    stats = filtered_df.drop(columns=['date']).dropna().describe()

    # Sección para estadísticas descriptivas usando pestañas
    st.markdown("### Estadísticas Descriptivas")
    tabs = st.tabs(["Resumen", "Caja Bigote", "Histograma"])

    with tabs[0]:
        st.dataframe(stats)

    with tabs[1]:
        fig_box = go.Figure()
        fig_box.add_trace(go.Box(y=filtered_df[selected_column_key], name=columns_to_plot[selected_column_key], marker_color=colors[company_name]))  # Usar el color
        fig_box.update_layout(title=f"Distribución de {columns_to_plot[selected_column_key]} de {company_name}",
                            yaxis_title=columns_to_plot[selected_column_key])
        st.plotly_chart(fig_box)

    with tabs[2]:
        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(x=filtered_df[selected_column_key], nbinsx=30, marker_color=colors[company_name]))  # Usar el color
        fig_hist.update_layout(title=f"Histograma de {columns_to_plot[selected_column_key]} de {company_name}",
                            xaxis_title=columns_to_plot[selected_column_key],
                            yaxis_title="Frecuencia")
        st.plotly_chart(fig_hist)

    # Mostrar la matriz de correlación
    st.divider()
    numeric_data = filtered_df.select_dtypes(include='number')
    display_correlation(numeric_data, company_name)

def linear_graphs(data, title, selected_column, color, columns_to_plot):
    # Gráfico de precios a lo largo del tiempo
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['date'], y=data[selected_column], mode='lines', name=columns_to_plot[selected_column], line=dict(color=color)))  # Usar el color
    fig.update_layout(title=f"{columns_to_plot[selected_column]} de {title}",  # Usar el valor en español
                    xaxis_title="Fecha",
                    yaxis_title=columns_to_plot[selected_column],
                    xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

def display_correlation(data, title):
    correlation_matrix = data.corr()
    st.markdown(f"### Matriz de Correlación")
    if correlation_matrix.empty:
        st.subheader(f"No hay datos numéricos disponibles para calcular la correlación en {title}.")
        return

    fig = px.imshow(
        correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.index,
        color_continuous_scale='magma',
        text_auto='.2f',
        labels=dict(color='Correlación'),
        title=f"Matriz de Correlación: {title}"
    )

    # Ajustar diseño
    fig.update_layout(
        width=800,
        height=600,
        xaxis_title="Variables",
        yaxis_title="Variables",
        margin=dict(l=50, r=50, t=50, b=50),
        font=dict(family="Arial", size=12),
    )
    
    st.plotly_chart(fig)