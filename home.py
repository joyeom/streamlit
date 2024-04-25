import streamlit as st
from st_pages import show_pages_from_config


st.set_page_config(
    page_title="Home", page_icon="./Inspection/Flitto_symbol.jpg", layout="wide"
)

show_pages_from_config(".streamlit/pages.toml")

st.title("Greetings, Data PM")
st.subheader("Prepare to Embark on a Data Odyssey 🌌")
st.image("./pages/Flitto_pretty.jpg")
st.balloons()


# hide streamlit toolbar on top
hide_streamlit_style = """
<style>
[data-testid="stToolbar"] {visibility: hidden !important;}
footer {visibility: hidden !important;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)