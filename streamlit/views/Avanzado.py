import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.express as px
import pandas as pd
import streamlit as st

def Avanzado(datasets):
    st.title("📊 Análisis Avanzado de las Empresas Big Tech")
    st.markdown(
        """
        Este análisis incluye visualizaciones interactivas avanzadas para explorar:
        
        - **Distribución de precios ajustados**: Diagrama de Violín.
        - **Identificación de outliers**: Bandas de Bollinger.
        - **Análisis temporal avanzado**: Heatmaps de Volumen y Precio Ajustado.
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
    st.divider()
    ### HEATMAPS: Análisis Temporal Avanzado ###
    st.subheader("📆 Heatmaps de Análisis Temporal")
    st.markdown(
        """
        Los heatmaps permiten visualizar tendencias temporales:
        
        - **Volumen (%)**: Identifica periodos con mayor actividad de volumen.
        - **Precio Ajustado (%)**: Observa periodos con cambios significativos en el precio ajustado.
        """
    )

    # Selección de compañía para el heatmap
    selected_company_heatmap = st.selectbox(
        "Selecciona una compañía para los heatmaps:",
        datasets.keys()
    )

    if selected_company_heatmap:
        data = datasets[selected_company_heatmap]
        if 'adj_close' in data.columns and 'volume' in data.columns and 'date' in data.columns:
            data['date'] = pd.to_datetime(data['date'])
            data['year'] = data['date'].dt.year
            data['month'] = data['date'].dt.month

            # Filtrar datos entre 2000 y 2022
            data = data[(data['year'] >= 2000) & (data['year'] <= 2022)]

            # Calcular % volumen mensual
            volume_by_month = (
                data.groupby(['year', 'month'])['volume']
                .sum()
                .unstack(fill_value=0)
                .reset_index()
            )
            volume_normalized = volume_by_month.set_index('year')
            volume_normalized = volume_normalized.div(volume_normalized.sum().sum()) * 100

            # Calcular % cambio del precio ajustado
            data['price_change'] = data['adj_close'].pct_change() * 100
            price_by_month = (
                data.groupby(['year', 'month'])['price_change']
                .mean()
                .unstack(fill_value=0)
                .reset_index()
            )
            price_by_month = price_by_month.set_index('year')

            # Función para crear heatmaps anotados
            def crear_heatmap(datos, titulo, esquema_colores):
                datos_annot = datos.fillna(0).round(2)
                z = datos_annot.values
                x = [f"{i:02d}" for i in datos.columns]  # Meses
                y = datos.index.astype(str).tolist()  # Convertir el índice en una lista de strings
            
                # Crear heatmap con anotaciones
                fig = ff.create_annotated_heatmap(
                    z=z,
                    x=x,
                    y=y,
                    colorscale=esquema_colores,
                    annotation_text=datos_annot.values.astype(str),
                    showscale=True
                )
                fig.update_layout(
                    title=titulo,
                    xaxis=dict(title="Mes"),
                    yaxis=dict(title="Año"),
                    width=800,
                    height=600,
                )
                return fig

            # Selección del tipo de heatmap
            heatmap_option = st.radio(
                "Selecciona el tipo de heatmap:",
                ["Volumen (%)", "Precio Ajustado (%)"]
            )

            if heatmap_option == "Volumen (%)":
                st.subheader(f"📊 Heatmap de Volumen (%) para {selected_company_heatmap}")
                heatmap_volumen = crear_heatmap(volume_normalized, "Porcentaje de Volumen (%)", "Blues")
                st.plotly_chart(heatmap_volumen)
            else:
                st.subheader(f"📈 Heatmap de Precio Ajustado (%) para {selected_company_heatmap}")
                heatmap_precio = crear_heatmap(price_by_month, "Cambio del Precio Ajustado (%)", "Oranges")
                st.plotly_chart(heatmap_precio)
                
                
        st.divider()
        # Preparación de los datos para el Heatmap Global (Porcentual)
        st.subheader("📈 Heatmap Global Porcentual de Volúmenes de Big Tech")
        st.markdown(
            """
            Este heatmap muestra los momentos del año con mayor actividad en las acciones de las compañías analizadas,
            en términos **porcentuales**.
            """
        )
        
        # Preparamos los datos para el heatmap global
        # Combinar los datos de todas las compañías
        global_volume_data = pd.DataFrame()
        
        for company, data in datasets.items():
            if 'volume' in data.columns and 'date' in data.columns:
                data['date'] = pd.to_datetime(data['date'])
                data['Año'] = data['date'].dt.year
                data['Mes'] = data['date'].dt.month
                company_volume = data.groupby(['Año', 'Mes'])['volume'].sum().reset_index()
                company_volume['Compañía'] = company
                global_volume_data = pd.concat([global_volume_data, company_volume], ignore_index=True)
        
        # Agregar los volúmenes globales por año y mes
        volume_by_month = global_volume_data.groupby(['Año', 'Mes'])['volume'].sum().unstack(fill_value=0)
        
        # Convertir los volúmenes a valores porcentuales por año
        volume_by_month_percentage = volume_by_month.div(volume_by_month.sum(axis=1), axis=0) * 100
        
        # Crear el heatmap porcentual
        heatmap_volumen = crear_heatmap(
            volume_by_month_percentage,
            "Heatmap Global Porcentual de Volúmenes",
            "Blues"
        )
        st.plotly_chart(heatmap_volumen)
        
        st.markdown(
            """
            **¿Cómo leer el Heatmap?**
            - **Colores oscuros**: Indican períodos con un mayor porcentaje del volumen total anual.
            - **Colores claros**: Indican períodos con un menor porcentaje del volumen total anual.
            """
        )
    st.divider()
        ### SCATTERPLOT MATRIX: Relaciones Cruzadas ###
    st.subheader("📈 Scatterplot Matrix: Relaciones Cruzadas entre Variables")
    st.markdown(
        """
        Esta matriz de dispersión muestra las relaciones cruzadas entre diferentes variables financieras, como:
        - **Precio Ajustado (adj_close)**.
        - **Volumen (volume)**.
        - **Precio de Apertura (open)**.
        
        Permite identificar correlaciones y patrones entre estas variables.
        """
    )

    # Selección de compañía para el Scatterplot Matrix
    selected_company_scatter = st.selectbox(
        "Selecciona una compañía para analizar las relaciones cruzadas:",
        datasets.keys(),
        key="scatter_company_select"
    )

    if selected_company_scatter:
        data = datasets[selected_company_scatter]
        if all(col in data.columns for col in ['adj_close', 'volume', 'open']):
            # Normalización de las fechas
            data['date'] = pd.to_datetime(data['date'])

            # Filtrar columnas relevantes
            scatter_data = data[['adj_close', 'volume', 'open']].copy()

            # Crear la matriz de dispersión
            scatter_matrix = px.scatter_matrix(
                scatter_data,
                dimensions=['adj_close', 'volume', 'open'],
                labels={
                    "adj_close": "Precio Ajustado",
                    "volume": "Volumen",
                    "open": "Precio de Apertura"
                },
                title=f"Scatterplot Matrix para {selected_company_scatter}",
                color_discrete_sequence=[colors.get(selected_company_scatter, '#636EFA')],
                template="plotly_white"
            )

            scatter_matrix.update_layout(
                font=dict(family='Arial', size=14, color='#023047'),
                title_font_size=16,
                width=800,
                height=800
            )

            # Mostrar la gráfica en Streamlit
            st.plotly_chart(scatter_matrix)

            st.markdown(
                """
                **¿Cómo leer el Scatterplot Matrix?**
                - Cada celda representa una relación entre dos variables.
                - **Tendencias lineales o curvas:** Indican correlaciones positivas o negativas.
                - **Distribución diagonal:** Muestra la distribución de cada variable.
                """
            )
