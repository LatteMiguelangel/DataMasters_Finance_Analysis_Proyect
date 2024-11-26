import pandas as pd
import plotly.express as px
import streamlit as st

def Hitos(datasets):
    st.title("📈 Análisis Histórico de Hitos Globales")
    st.markdown(
        """
        Explora cómo los grandes hitos globales han afectado a las empresas tecnológicas en términos de precios ajustados y volumen de transacciones.
        Selecciona un evento para analizar las tendencias.
        """
    )
    st.divider()

    # Lista de eventos y sus rangos de fechas
    eventos = [
        ("Invasión de Rusia a Ucrania", "2022-02-24", "2023-05-23"),
        ("COVID 2019", "2020-01-30", "2023-01-30"),
        ("Gripe H1N1", "2009-06-11", "2010-09-18"),
        ("La Gran Recesión (Crisis burbuja inmobiliaria)", "2007-12-01", "2009-06-30"),
        ("1° Iphone", "2007-01-09", "2008-12-31"),
        ("Huracán Katrina", "2005-08-23", "2005-12-31"),
        ("Guerra de Irak", "2003-03-20", "2004-03-20"),
        ("Ataques del 11 de septiembre", "2001-08-30", "2002-09-30"),
        ("Ataque del virus ILOVEYOU/LoveLetter", "2000-05-05", "2001-05-05"),
        ("Crisis de las puntocom", "2000-01-01", "2002-12-31"),
    ]

    # Crear diccionario de eventos
    opciones_eventos = {evento[0]: (evento[1], evento[2]) for evento in eventos}

    # Selección de evento
    selected_event = st.selectbox("Selecciona un evento histórico:", opciones_eventos.keys(), key="select_event")
    rango_fechas = opciones_eventos[selected_event]

    st.markdown(f"### Evento seleccionado: **{selected_event}**")
    st.markdown(f"- **Rango de fechas:** {rango_fechas[0]} a {rango_fechas[1]}")
    st.divider()

    # Filtrar datos para un rango de fechas dado
    def filtrar_datos(datasets, columna, rango_fechas):
        filtered_data = pd.DataFrame()
        for company, data in datasets.items():
            if columna in data.columns and 'date' in data.columns:
                data['date'] = pd.to_datetime(data['date'])
                filtered = data[(data['date'] >= rango_fechas[0]) & (data['date'] <= rango_fechas[1])].copy()
                filtered['Compañía'] = company  # Añadir nombre de la compañía
                filtered_data = pd.concat([filtered_data, filtered])
        return filtered_data

    # Gráfico genérico para evitar duplicación
    def mostrar_grafico(filtered_data, columna, titulo, eje_y):
        if filtered_data.empty:
            st.warning(f"No hay datos disponibles para el evento seleccionado: {selected_event}.")
            return
        fig = px.line(
            filtered_data,
            x="date",
            y=columna,
            color="Compañía",
            title=titulo,
            labels={"date": "Fecha", "Compañía": "Empresas", columna: eje_y},
            color_discrete_map={
                'Sony': '#1428A0',
                'IBM': '#F180E6',
                'Google': '#FBBC05',
                'Microsoft': '#A51C30',
                'Amazon': '#F44611',
                'Nvidia': '#76B900',
                'Samsung': '#4285F4',
                'Apple': '#B5B5B5'
            }
        )
        fig.update_traces(mode="lines")
        fig.update_layout(
            template="plotly_white",
            font=dict(family='Arial', size=16, color='#023047'),
            xaxis_title="Fecha",
            yaxis_title=eje_y,
            legend_title="Empresas"
        )
        st.plotly_chart(fig)

    # Generar y mostrar gráficos
    datos_precio = filtrar_datos(datasets, "adj_close", rango_fechas)
    st.subheader("📈 Comportamiento durante el Evento: Precio Ajustado")
    mostrar_grafico(datos_precio, "adj_close", f"Tendencias de Precios Ajustados: {selected_event}", "Precio Ajustado (USD)")

    datos_volumen = filtrar_datos(datasets, "volume", rango_fechas)
    st.subheader("📊 Comportamiento durante el Evento: Volumen de Transacciones")
    mostrar_grafico(datos_volumen, "volume", f"Tendencias de Volumen: {selected_event}", "Volumen")

