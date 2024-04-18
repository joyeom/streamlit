import streamlit as st


st.set_page_config(page_title="Home", page_icon="./Inspection/Flitto_symbol.jpg")
st.title("Hi Data PM")
st.subheader("This is the home page")
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
