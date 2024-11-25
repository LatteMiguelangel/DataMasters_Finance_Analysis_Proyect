import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import streamlit as st

def Avanzado(datasets):
    st.title("📊 Análisis Avanzado de Big Tech")
    st.markdown(
        """
        Este análisis incluye visualizaciones interactivas avanzadas para explorar:
        
        1. **Comparación de volúmenes anuales**: Gráfico de Barras Apiladas.
        2. **Distribución de precios ajustados**: Diagrama de Violín.
        3. **Identificación de outliers**: Bandas de Bollinger.
        4. **Eventos clave**: Anotaciones en series temporales.
        """
    )


