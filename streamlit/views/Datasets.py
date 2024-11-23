import streamlit as st
def Datasets(samsung_df, apple_df, amazon_df, microsoft_df, nvidia_df, google_df, sony_df, ibm_df):
    #mostrar df
    st.title("Comportamiento de las Acciones de las Empresas Big Tech")
    st.write("""
    ### Samsung Dataset
    """)
    st.dataframe(samsung_df.sort_values('date', ascending=True))
    st.divider()
    st.write("""
    ### Apple Dataset
    """)
    st.dataframe(apple_df.sort_values('date', ascending=True))
    st.divider()
    st.write("""
    ### Amazon Dataset
    """)
    st.dataframe(amazon_df.sort_values('date', ascending=True))
    st.divider()
    st.write("""
    ### Microsoft Dataset
    """)
    st.dataframe(microsoft_df.sort_values('date', ascending=True))
    st.divider()
    st.write("""
    ### Nvidia Dataset
    """)
    st.dataframe(nvidia_df.sort_values('date', ascending=True))
    st.divider()
    st.write("""
    ### Google Dataset
    """)
    st.dataframe(google_df.sort_values('date', ascending=True))
    st.divider()
    st.write("""
    ### Sony Dataset
    """)
    st.dataframe(sony_df.sort_values('date', ascending=True))
    st.divider()
    st.write("""
    ### IBM Dataset
    """)
    st.dataframe(ibm_df.sort_values('date', ascending=True))    
