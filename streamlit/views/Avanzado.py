import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import streamlit as st

def Avanzado(datasets):
    st.title("📊 Análisis Avanzado de las Empresas Big Tech")
    st.markdown(
        """
        Este análisis incluye visualizaciones interactivas avanzadas para explorar:
        
        - **Comparación de volúmenes anuales**: Gráfico de Barras Apiladas.
        - **Distribución de precios ajustados**: Diagrama de Violín.
        - **Identificación de outliers**: Bandas de Bollinger.
        """
    )
    st.divider()

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

    ### GRÁFICO 1: Volúmenes Anuales (Barras Apiladas) ###
    st.subheader("📊 Volúmenes Anuales de Todas las Compañías")
    st.markdown(
        """
        Este gráfico muestra el volumen anual total de transacciones para cada compañía, apilado para observar la contribución relativa de cada empresa.
        """
    )

    # Crear un DataFrame combinado para los volúmenes anuales
    volume_data = pd.DataFrame()

    for company, data in datasets.items():
        if 'volume' in data.columns and 'date' in data.columns:
            data['date'] = pd.to_datetime(data['date'])
            yearly_volume = data.groupby(data['date'].dt.year)['volume'].sum()
            volume_data[company] = yearly_volume

    volume_data.index.name = "Año"
    volume_data.reset_index(inplace=True)

    # Crear el gráfico de barras apiladas
    fig_volume = px.bar(
        volume_data,
        x="Año",
        y=volume_data.columns[1:],  # Excluir la columna de años
        title="Volúmenes Anuales de Transacciones (Barras Apiladas)",
        labels={"value": "Volumen", "variable": "Compañías"},
        color_discrete_map=colors
    )

    fig_volume.update_layout(
        barmode='stack',
        template='plotly_white',
        font=dict(family='Arial', size=16, color='#023047'),
        xaxis_title="Año",
        yaxis_title="Volumen Total (en unidades)"
    )
    st.plotly_chart(fig_volume)
    st.markdown(
    """
    **¿Cómo leer el Gráfico?**
    - **Barras más altas:** Indican años con mayor volumen de transacciones en general.
    - **Segmentos de color:** Representan la proporción del volumen total que corresponde a cada compañía en un año determinado.
    """
    )
    st.divider()

    ### GRÁFICO 2: Distribución de Precios Ajustados (Diagrama de Violín) ###
    st.subheader("🎻 Distribución de Precios Ajustados de Cada Compañía")
    st.markdown(
        """
        Este diagrama de violín muestra la distribución de los precios ajustados de las acciones para una compañía seleccionada, indicando su rango y densidad.
        """
    )

    # Selección de compañía para el diagrama de violín
    selected_company_violin = st.selectbox(
        "Selecciona una compañía para analizar la distribución de precios ajustados:",
        datasets.keys()
    )

    if selected_company_violin:
        data = datasets[selected_company_violin]
        if 'adj_close' in data.columns and 'date' in data.columns:
            data['date'] = pd.to_datetime(data['date'])

            # Crear el DataFrame para la compañía seleccionada
            violin_data = pd.DataFrame({
                "Precio Ajustado": data['adj_close'],
                "Compañía": selected_company_violin
            })

            # Crear el gráfico de violín
            fig_violin = px.violin(
                violin_data,
                x="Compañía",
                y="Precio Ajustado",
                color="Compañía",
                box=True,  # Mostrar caja dentro del violín
                points="all",  # Mostrar todos los puntos
                title=f"Distribución de Precios Ajustados: {selected_company_violin}",
                color_discrete_map={selected_company_violin: colors.get(selected_company_violin, '#636EFA')}
            )

            fig_violin.update_layout(
                template="plotly_white",
                font=dict(family='Arial', size=16, color='#023047'),
                xaxis_title="Compañía",
                yaxis_title="Precio Ajustado (USD)"
            )
            
            st.plotly_chart(fig_violin)
            st.markdown(
            """
                **¿Cómo leer el Diagrama de Violín?**
                - **Forma del violín:** La forma más ancha indica donde se concentran más datos (precios más frecuentes).
                - **Caja dentro del violín:** Representa el rango intercuartil (IQR), es decir, el  50% de los datos.
                - **Línea dentro de la caja:** Indica la mediana (valor central).
                """
            )
    st.divider()

    ### GRÁFICO 3: Identificación de Outliers (Bandas de Bollinger) ###
    st.subheader("🎯 Identificación de Outliers")
    st.markdown(
        """
        Este gráfico utiliza Bandas de Bollinger para identificar posibles outliers en el precio ajustado de las acciones de cada compañía.
        """
    )

    # Selección de compañía para el análisis de Bandas de Bollinger
    selected_company_bollinger = st.selectbox(
        "Selecciona una compañía para visualizar las Bandas de Bollinger:",
        datasets.keys()
    )

    if selected_company_bollinger:
        data = datasets[selected_company_bollinger]
        if 'adj_close' in data.columns and 'date' in data.columns:
            data['date'] = pd.to_datetime(data['date'])

            # Calcular media móvil y desviación estándar
            window = 20  # Ventana de 20 días
            data['SMA'] = data['adj_close'].rolling(window=window).mean()
            data['STD'] = data['adj_close'].rolling(window=window).std()

            # Calcular las bandas superior e inferior
            data['Upper Band'] = data['SMA'] + (data['STD'] * 2)
            data['Lower Band'] = data['SMA'] - (data['STD'] * 2)

            # Crear el gráfico de Bandas de Bollinger
            fig_bollinger = go.Figure()

            # Precio Ajustado
            fig_bollinger.add_trace(go.Scatter(
                x=data['date'],
                y=data['adj_close'],
                mode='lines',
                name='Precio Ajustado',
                line=dict(color=colors.get(selected_company_bollinger, '#636EFA'))
            ))

            # SMA
            fig_bollinger.add_trace(go.Scatter(
                x=data['date'],
                y=data['SMA'],
                mode='lines',
                name='Media Móvil (SMA)',
                line=dict(color='#FFA500', dash='dot')
            ))

            # Banda Superior
            fig_bollinger.add_trace(go.Scatter(
                x=data['date'],
                y=data['Upper Band'],
                mode='lines',
                name='Banda Superior',
                line=dict(color='green', dash='dot')
            ))

            # Banda Inferior
            fig_bollinger.add_trace(go.Scatter(
                x=data['date'],
                y=data['Lower Band'],
                mode='lines',
                name='Banda Inferior',
                line=dict(color='red', dash='dot')
            ))

            fig_bollinger.update_layout(
                title=f"Bandas de Bollinger para {selected_company_bollinger}",
                xaxis_title="Fecha",
                yaxis_title="Precio Ajustado (USD)",
                template="plotly_white",
                font=dict(family='Arial', size=16, color='#023047')
            )

            st.plotly_chart(fig_bollinger)
            st.markdown(
                """
                **¿Cómo leer las Bandas de Bollinger?**
                - **Banda superior e inferior:** Representan los límites superior e inferior de un rango de precios considerado "normal".
                - **Precio ajustado:** La línea que representa el precio real de las acciones.

                **Notas**
                - **Outliers:** Los precios que se encuentran fuera de las bandas suelen considerarse valores atípicos.
                - **Tendencias:** La dirección general del precio y si está volátil o estable.

                Son un indicador técnico que utiliza una media móvil y desviaciones estándar para crear bandas alrededor del precio de un activo. Estas bandas pueden ayudar a identificar sobrecompra o sobreventa, así como a detectar posibles puntos de entrada        o salida.
                """
            )