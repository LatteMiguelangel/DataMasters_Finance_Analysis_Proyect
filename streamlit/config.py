import streamlit as st

def config():
    st.set_page_config(
        page_title="Big Tech Stocks Analysis",
        page_icon="🖥",
        layout="centered",
        initial_sidebar_state="expanded"
    )

    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)