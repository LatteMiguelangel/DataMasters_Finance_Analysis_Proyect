import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

def Datasets(datasets):
    # Título principal con descripción inicial
    st.title("📊 Análisis de los Datasets de Empresas Big Tech")
    st.markdown(
        """
        Explora los datasets de las principales empresas tecnológicas (*Big Tech*). Aquí podrás:
        - Visualizar datos históricos de precios y volúmenes.
        - Seleccionar rangos de fechas específicos.
        - Analizar estadísticas descriptivas, distribuciones y correlaciones.

        Usa las herramientas interactivas para ajustar los gráficos y explorar los datos en detalle.
        """
    )
    st.divider()

    # Diccionario de enlaces a los datasets
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

    # Selector de empresa
    st.subheader("🔍 Selección de Dataset")
    company_name = st.selectbox("Selecciona una empresa para analizar:", list(datasets.keys()))
    selected_df = datasets[company_name]

    # Enlaces adicionales
    st.markdown(f"**🔗 Enlace al Dataset:** {links[company_name]}")
    if company_name == "Samsung":
        st.markdown("###### Enlaces de Conversión USD a KRW:")
        st.markdown("- https://www.kaggle.com/datasets/imtkaggleteam/dollar-vs-asian-currencies")
        st.markdown("- https://www.kaggle.com/datasets/biokpc/us-korean-exchange-rate")

    # Mostrar información del dataset
    st.markdown(f"### 📋 Información del Dataset de {company_name}")
    selected_df['date'] = pd.to_datetime(selected_df['date'], errors='coerce')
    st.write(f"Total de registros: **{len(selected_df)}**")
    st.write(f"Rango de fechas: **{selected_df['date'].min().date()}** a **{selected_df['date'].max().date()}**")

    # Selector de rango de fechas
    st.markdown("### 📅 Selección de Rango de Fechas")
    start_date, end_date = st.date_input(
        "Selecciona el rango de fechas:",
        [selected_df['date'].min().date(), selected_df['date'].max().date()]
    )
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = selected_df[(selected_df['date'] >= start_date) & (selected_df['date'] <= end_date)]
    st.dataframe(filtered_df.sort_values('date', ascending=True))
    st.divider()

    # Selección de columna para graficar
    st.markdown("### 📊 Visualización de Datos")
    columns_to_plot = {
        'open': 'Precio de Apertura',
        'high': 'Precio más Alto',
        'low': 'Precio más Bajo',
        'close': 'Precio de Cierre',
        'adj_close': 'Cierre Ajustado',
        'volume': 'Volumen'
    }
    selected_column_key = st.selectbox("Selecciona el campo a visualizar:", list(columns_to_plot.keys()), format_func=lambda x: columns_to_plot[x])

    # Gráfico lineal
    st.markdown(f"#### 📈 Gráfico de {columns_to_plot[selected_column_key]}")
    linear_graphs(filtered_df, company_name, selected_column_key, colors[company_name], columns_to_plot)
    st.divider()

    # Estadísticas descriptivas
    st.markdown("### 📊 Estadísticas Descriptivas")
    stats = filtered_df.drop(columns=['date']).dropna().describe()
    tabs = st.tabs(["📋 Resumen", "📦 Caja y Bigotes", "📊 Histograma"])

    with tabs[0]:
        st.markdown("#### 📋 Resumen Estadístico")
        st.dataframe(stats)
        st.markdown(
            """
            **¿Qué Siginifica esta Tabla?**:
            - Es un resumen estadístico que muestra métricas clave como:
              - **Media**: El valor promedio.
              - **Desviación estándar**: Cómo varían los datos respecto a la media.
              - **Mínimo y máximo**: Los valores extremos del conjunto de datos.
            - Útil para obtener una visión general de los datos seleccionados.
            """
        )

    with tabs[1]:
        st.markdown(f"#### 📦 Distribución de {columns_to_plot[selected_column_key]}")
        fig_box = go.Figure()
        fig_box.add_trace(go.Box(y=filtered_df[selected_column_key], name=columns_to_plot[selected_column_key], marker_color=colors[company_name]))
        fig_box.update_layout(
            title=f"Distribución de {columns_to_plot[selected_column_key]} de {company_name}",
            yaxis_title=columns_to_plot[selected_column_key]
        )
        st.plotly_chart(fig_box)
        st.markdown(
            """
            **¿Cómo leer el Boxplot? (Diagrama de Caja y Bigote)**:
            - El gráfico de caja y bigote muestra la **distribución de un conjunto de datos**:
                - La caja representa el rango intercuartil (IQR), es decir, del 25% al 75% de los datos.
                - La línea dentro de la caja es la mediana.
                - Los "bigotes" muestran el rango de datos que no son considerados outliers.
            - Útil para detectar **outliers** y entender la dispersión de los datos.
            """
        )

    with tabs[2]:
        st.markdown(f"#### 📊 Histograma de {columns_to_plot[selected_column_key]}")
        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(x=filtered_df[selected_column_key], nbinsx=30, marker_color=colors[company_name]))
        fig_hist.update_layout(
            title=f"Histograma de {columns_to_plot[selected_column_key]} de {company_name}",
            xaxis_title=columns_to_plot[selected_column_key],
            yaxis_title="Frecuencia"
        )
        st.plotly_chart(fig_hist)
        st.markdown(
            """
            **¿Cómo leer el Histograma?**:
            - Un histograma muestra la **frecuencia** con la que ocurren ciertos valores en un conjunto de datos.
                - El eje X representa los valores.
                - El eje Y representa la cantidad de veces que esos valores ocurren.
            - Útil para visualizar la **distribución de los datos** y detectar tendencias como sesgos o agrupaciones.
            """
        )
    st.divider()

    # Matriz de correlación
    st.markdown("### 📈 Matriz de Correlación")
    numeric_data = filtered_df.select_dtypes(include='number')
    display_correlation(numeric_data, company_name)

def linear_graphs(data, title, selected_column, color, columns_to_plot):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['date'], y=data[selected_column], mode='lines', name=columns_to_plot[selected_column], line=dict(color=color)))
    fig.update_layout(
        title=f"{columns_to_plot[selected_column]} de {title}",
        xaxis_title="Fecha",
        yaxis_title=columns_to_plot[selected_column],
        xaxis_rangeslider_visible=True
    )
    st.plotly_chart(fig)

def display_correlation(data, title):
    correlation_matrix = data.corr()
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
    fig.update_layout(
        width=800,
        height=600,
        xaxis_title="Variables",
        yaxis_title="Variables",
        margin=dict(l=50, r=50, t=50, b=50),
        font=dict(family="Arial", size=12)
    )
    st.plotly_chart(fig)
    st.markdown(
        """
        **¿Cómo leer la Matriz de Correlación?**:
        - La **matriz de correlación** muestra la relación entre las variables numéricas del dataset.
        - Los valores van de **-1** a **1**:
            - **1**: Correlación positiva perfecta (cuando una variable sube, la otra también sube).
            - **-1**: Correlación negativa perfecta (cuando una variable sube, la otra baja).
            - **0**: No hay relación entre las variables.
        - Útil para identificar relaciones lineales entre variables (por ejemplo, entre precio y volumen).
        """
    )