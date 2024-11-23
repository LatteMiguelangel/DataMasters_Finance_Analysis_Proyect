import pandas as pd
import streamlit as st
import plotly.express as px
def Correlacion(datasets):
    st.title(""" Análisis de Correlación de Variables por Compañía""")
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
            #title=f'Matriz de Correlación: {company}',
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
        st.divider()




    combined_data = pd.DataFrame()
    for company, data in datasets.items():
        data['date'] = pd.to_datetime(data['date'])
        data = data.set_index('date') 
        combined_data[company] = data['adj_close'] 

    combined_data.dropna(inplace=True)

    correlation_matrix = combined_data.corr()

    st.header("Matriz de Correlación entre el Cierre Ajustado de las Compañías")

    fig = px.imshow(
        correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.index,
        color_continuous_scale='magma',
        text_auto='.2f',
        labels=dict(color='Correlación'),
        #title="Matriz de Correlación entre el Volumen de las Compañías",
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
    
    if st.checkbox("Mostrar precio de cierre ajustado de las compañías"):
        st.write(combined_data)
    
    st.divider()
    combined_volume_data = pd.DataFrame()
    for company, data in datasets.items():
        data['date'] = pd.to_datetime(data['date'])
        data = data.set_index('date') 
        combined_data[company] = data['volume'] 

    combined_volume_data.dropna(inplace=True)

    correlation_matrix = combined_data.corr()

    st.header("Matriz de Correlación entre el Volumen de las Compañías")

    fig = px.imshow(
        correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.index,
        color_continuous_scale='magma',
        text_auto='.2f',
        labels=dict(color='Correlación'),
        #title="Matriz de Correlación entre el Volumen de las Compañías",
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