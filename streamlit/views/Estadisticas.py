import streamlit as st
def Estadisticas(datasets):
    st.header("""
Modulo de Estadísticas Descriptivas
""")
    st.write("""
        #### Distribución de Datos
""")
    for company, data in datasets.items():
        # Excluir la columna 'date' y calcular las estadísticas descriptivas
        st.write(f"Estadísticas para {company}:")
        st.write(data.drop(columns=['date']).describe())
    
    st.divider()
    st.write("""
            #### Análisis de Volatilidad
    """)

    for company, data in datasets.items():
        data['daily_range'] = data['high'] - data['low']
        data['daily_pct_change'] = (data['close'] - data['open']) / data['open'] * 100
        st.write(f"Resumen de volatilidad para {company}:\n")
        st.write(data[['daily_range', 'daily_pct_change']].describe())