import pandas as pd
import plotly.express as px
import streamlit as st

def Hitos(datasets):
    st.title("📆 Análisis Histórico de Hitos Globales")
    st.markdown(
        """
        Este análisis permite explorar cómo los grandes hitos globales han afectado a las empresas tecnológicas. 
        Puedes seleccionar un evento histórico para ver las tendencias en los precios ajustados durante el rango de fechas correspondiente.
        """
    )
    st.divider()

    # Lista de eventos y rangos de fechas
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

    # Crear diccionario para el selectbox
    opciones_eventos = {evento[0]: (evento[1], evento[2]) for evento in eventos}

    # Selección de evento
    selected_event = st.selectbox("Selecciona un evento histórico:", opciones_eventos.keys())
    rango_fechas = opciones_eventos[selected_event]

    st.markdown(f"### Evento seleccionado: **{selected_event}**")
    st.markdown(f"- **Rango de fechas:** {rango_fechas[0]} a {rango_fechas[1]}")
    st.divider()

    # Filtrar datos en función del rango de fechas
    filtered_data = pd.DataFrame()

    for company, data in datasets.items():
        if 'adj_close' in data.columns and 'date' in data.columns:
            data['date'] = pd.to_datetime(data['date'])
            filtered = data[(data['date'] >= rango_fechas[0]) & (data['date'] <= rango_fechas[1])].copy()
            filtered['Compañía'] = company  # Añadir nombre de compañía para diferenciarlas
            filtered_data = pd.concat([filtered_data, filtered])

    # Verificar que hay datos después del filtro
    if filtered_data.empty:
        st.warning(f"No hay datos disponibles para el evento seleccionado: {selected_event}.")
        return

    st.subheader("📈 Comportamiento durante el Evento (Gráfico Lineal)")

    fig = px.line(
        filtered_data,
        x="date",
        y="adj_close",
        color="Compañía",
        title=f"Tendencias de Precios Ajustados: {selected_event}",
        labels={
            "adj_close": "Precio Ajustado (USD)",
            "date": "Fecha",
            "Compañía": "Empresas"
        },
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

    # Personalización del diseño
    fig.update_traces(mode="lines")  # Líneas con puntos en cada valor
    fig.update_layout(
        template="plotly_white",
        font=dict(family='Arial', size=16, color='#023047'),
        xaxis_title="Fecha",
        yaxis_title="Precio Ajustado (USD)",
        legend_title="Empresas",
    )
    st.plotly_chart(fig)


