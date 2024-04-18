import streamlit as st
import pandas as pd
import st_pop_up_component as sp
import numpy as np
import random
from annotated_text import annotated_text

print("this is lct.py")
st.set_page_config(page_title="LCT", page_icon="./LCT/Flitto_symbol.jpg")
st.title("LCT")

# hide streamlit toolbar on top
hide_streamlit_style = """
<style>
[data-testid="stToolbar"] {visibility: hidden !important;}
footer {visibility: hidden !important;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# Base Module
class Widget:
    def __init__(self, root=None):
        self._root = root
        self.initUI()

    def initUI(self):
        pass


class Main(Widget):
    def __init__(self, root=None):
        self.__DEFAULT_STATE = {
            "uploaded_file": [],  # json -> excel
            "pair_dict": {},  # excel -> json and excel : json pair
            "need_inspect": False,
            "environment": "",
            "src_lang": "",
            "tgt_lang": "",
        }

        super().__init__(root)

    def create_pair_uploader(self, ct):

        ej_col1, arrow, ej_col2 = st.columns(3)

        with ej_col1:

            excel = st.file_uploader(
                "Upload Excel",
                accept_multiple_files=False,
                type=".xlsx",
                key=f"excel_{ct}",
            )
        with arrow:
            st.text("       ➡️")
        with ej_col2:
            json = st.file_uploader(
                "Upload Json",
                accept_multiple_files=False,
                type=".json",
                key=f"json_{ct}",
            )
        # update the pair_dict
        self.__DEFAULT_STATE["pair_dict"][excel] = json

    def initUI(self):
        tab1, tab2 = st.tabs(["json -> excel", "excel -> json"])

        with tab1:
            self.__DEFAULT_STATE["environment"] = "json -> excel"
            tab1.subheader("json -> excel")

            uploaded_file = st.file_uploader(
                "Choose a File", accept_multiple_files=True, type=".json"
            )
            self.__DEFAULT_STATE["uploaded_file"] = uploaded_file
            need_inspect = st.toggle("내부검수 추가")
            self.__DEFAULT_STATE["need_inspect"] = need_inspect
            tab1_next_button = st.button("Next", key="tab1")
            if tab1_next_button:
                st.spinner("generating files....")
                # call json to excel class
                # if need_inspect add inspect
                # else convert it and make it download in zip file

        with tab2:
            self.__DEFAULT_STATE["environment"] = "excel -> json"
            tab2.subheader("excel -> json")
            st.text("엑셀과 원문 json을 모두 짝지어서 올려주세요")
            # Create an empty placeholder for dynamic content
            placeholder = st.empty()
            ct = len(self.__DEFAULT_STATE["pair_dict"].keys())

            ej_col1, arrow, ej_col2 = st.columns([3, 2, 3])

            with ej_col1:
                excel = st.file_uploader(
                    "Upload Excel",
                    accept_multiple_files=True,
                    type=".xlsx",
                    key=f"excel_{ct}",
                )

            with arrow:
                st.text("➡️")

            with ej_col2:
                json = st.file_uploader(
                    "Upload Json",
                    accept_multiple_files=True,
                    type=".json",
                    key=f"json_{ct}",
                )

            if excel and json:

                pair_objects = [{"Excel": e, "Json": j} for e, j in zip(excel, json)]

                for i, pair_obj in enumerate(pair_objects):
                    st.write(f"Pair {i+1}:")
                    annotated_text((f"Pair {i+1}:"))
                    st.write(
                        f"**Excel**: {pair_obj['Excel'].name}, **JSON**: {pair_obj['Json'].name}"
                    )

                tab2_next_button = st.button("Next", key="tab2")

                if tab2_next_button:
                    if len(excel) != len(json):
                        st.error(
                            "Excel 파일의 수와 JSON 파일의 수가 일치하지 않습니다."
                        )
                    else:
                        pass
                        
                        # popup_output = sp.st_custom_pop_up(
                        #     message="확실히 짝이 다 맞나요?", key=random.random()
                        # )
                        # print(
                        #     "popup_output",
                        #     popup_output,
                        #     type(popup_output),
                        #     "tab2_next",
                        #     tab2_next_button,
                        # )
                        # popup_output
                        # if popup_output:
                        #     with st.spinner("generating files...."):
                        #         for e, j in zip(excel, json):
                        #             self.__DEFAULT_STATE["pair_dict"][e] = j
                        # else:
                        #     tab2_next_button = False
                    # generate excel_json using pair_dict
                    # create download button then make it download as zip file

    def get_state(self):
        return self.__DEFAULT_STATE


class json_to_excel(Widget):
    def __init__(self, root=None):
        self.state = self.__getstate__()


class excel_to_json(Widget):
    def __init__(self, root=None):
        self.state = self.__getstate__()


if __name__ == "__main__":
    Main()
