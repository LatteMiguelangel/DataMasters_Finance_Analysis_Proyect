import streamlit as st
def Datasets(samsung_df, apple_df):
    #mostrar df
    st.title("Comportamiento de las Acciones de las Empresas Big Tech")
    st.write("""
    ### Samsung Dataset
    Esta tabla contiene las acciones de **Samsung** convertidas a dólares del **2000 al 2022**.
    """)
    st.dataframe(samsung_df.sort_values('date', ascending=True))
    st.divider()
    st.write("""
    ### Apple Dataset
    Esta tabla contiene las acciones de **Apple** convertidas a dólares del **2000 al 2022**.
    """)
    st.dataframe(apple_df.sort_values('date', ascending=True))
