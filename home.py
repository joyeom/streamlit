import streamlit as st
from streamlit_extras.app_logo import add_logo
from st_pages import show_pages_from_config, add_page_title
from st_pages import Page, Section, add_page_title, show_pages
# def logo():
#     add_logo("https://brunch.co.kr/@brodipage/20", height=300)


# Either this or add_indentation() MUST be called on each page in your
# app to add indendation in the sidebar


st.set_page_config(page_title="Home", page_icon="./Inspection/Flitto_symbol.jpg",layout = 'wide')

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
#https://github.com/blackary/st_pages => 이걸로 나중에 페이지 수정하기 