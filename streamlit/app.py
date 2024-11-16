import streamlit as st
import pandas as pd

# Cargar datos
@st.cache
def load_data(filepath):
    return pd.read_csv(filepath)

st.title("Análisis Financiero: Samsung vs Apple")

# Cargar datasets procesados
samsung_df = load_data('./data/processed/samsung_cleaned.csv')
apple_df = load_data('./data/processed/apple_cleaned.csv')

# Mostrar datos
st.write("Previsualización de Samsung:")
st.dataframe(samsung_df.head())

st.write("Previsualización de Apple:")
st.dataframe(apple_df.head())

# Gráfico interactivo
company = st.selectbox("Selecciona una empresa", ["Samsung", "Apple"])
if company == "Samsung":
    st.line_chart(samsung_df[['Date', 'Close']].set_index('Date'))
else:
    st.line_chart(apple_df[['Date', 'Close']].set_index('Date'))
