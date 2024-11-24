import pandas as pd
import streamlit as st
import plotly.express as px

def Correlacion(datasets):
    st.title("Análisis de Correlación de Variables por Compañía")
    
    # Selector para elegir la compañía
    company_name = st.selectbox("Selecciona una compañía:", list(datasets.keys()))
    
    # Filtrar los datos de la compañía seleccionada
    data = datasets[company_name]
    numeric_data = data.select_dtypes(include='number')

    # Mostrar la matriz de correlación solo para la compañía seleccionada
    display_correlation(numeric_data, company_name)

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