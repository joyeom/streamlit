import streamlit as st
import pandas as pd
import st_pop_up_component as sp
from io import BytesIO
import zipfile

# json > excel
from File_Conversion.je import convert as json2excel

# excel > json
from File_Conversion.ej import convert as excel2json


st.set_page_config(page_title="LCT", page_icon="./Inspection/Flitto_symbol.jpg")
st.title("LCT File Converter")

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
            "uploaded_file": [],  # used in "json -> excel" tab
            "pair_list": [],  # used in  "excel -> json" tab and [{excel1 : json1}, {excel2 : json2}]
            "need_inspect": False,
            "environment": "",
            "src_lang": "",
            "tgt_lang": "",
        }

        super().__init__(root)

    def DEFAULT_SETTINGS(self):
        for state in self.__DEFAULT_STATE:
            if state not in st.session_state:
                st.session_state[state] = self.__DEFAULT_STATE[state]
            print(
                "Default setting st.session_state[state]",
                state,
                st.session_state[state],
                self.__DEFAULT_STATE[state],
            )

    def check_tab1_input_validity(self):
        self.input_validity = all(
            [
                self.__DEFAULT_STATE["uploaded_file"] != [],
                self.__DEFAULT_STATE["environment"] != "",
                self.__DEFAULT_STATE["environment"] == "je",
            ]
        )

        return self.input_validity

    def check_tab2_input_validity(self):
        self.input_validity = all(
            [
                self.__DEFAULT_STATE["uploaded_file"] != [],
                self.__DEFAULT_STATE["environment"] != "",
                self.__DEFAULT_STATE["environment"] == "ej",
            ]
        )

        return self.input_validity

    def initUI(self):
        tab1, tab2 = st.tabs(["JSON ▶ EXCEL", "EXCEL ▶ JSON"])

        with tab1:
            self.__DEFAULT_STATE["environment"] = "je"  # json > excel
            # tab1.subheader("json ➤ excel")
            st.info(
                """
                **파일 업로드 시 주의사항:** \n
                - 'Browse files' 버튼을 사용하여 파일을 업로드하세요. \n
                - 원하는 파일이 표시되지 않으면, ZIP 파일을 압축 해제해주세요.
                """
            )
            uploaded_file = st.file_uploader(
                "Choose a File", accept_multiple_files=True, type=".json"
            )
            self.__DEFAULT_STATE["uploaded_file"] = uploaded_file

            if self.check_tab1_input_validity():
                for s in self.__DEFAULT_STATE:
                    print("여기는 tab1 input", s, self.__DEFAULT_STATE[s])

                if st.button("Next"):
                    self.on_next_click()

        with tab2:
            self.__DEFAULT_STATE["environment"] = "ej"  # excel > json
            # tab2.subheader("excel ➤ json")

            # Displaying instructions within a callout box
            st.info(
                """
                **파일 업로드 시 주의사항:** \n
                - 'Browse files' 버튼을 사용하여 EXCEL 파일과 JSON 파일을 모두 업로드하세요. \n
                - 파일들을 매칭시키려면 :red[**이름이 동일해야 합니다**]
                """
            )

            # Create an empty placeholder for dynamic content
            placeholder = st.empty()
            ct = len(self.__DEFAULT_STATE["pair_list"])

            ej_col1, arrow, ej_col2 = st.columns([3, 2, 3])

            with ej_col1:
                uploaded_excel = st.file_uploader(
                    "Upload Excel",
                    accept_multiple_files=True,
                    type=".xlsx",
                    key=f"excel_{ct}",
                )

            with arrow:
                arrow_css = """
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 30px;
                    position: relative;
                    top:60px;
                    left:3px;
                """

                st.markdown(f"<div style='{arrow_css}'>▷</div>", unsafe_allow_html=True)
                # ➤,▷,➡️,▶,➲

            with ej_col2:
                uploaded_json = st.file_uploader(
                    "Upload Json",
                    accept_multiple_files=True,
                    type=".json",
                    key=f"json_{ct}",
                )

            if uploaded_excel and uploaded_json:
                unmatched = []  # add unmatched files
                # 이름이 같은걸로 자동 match
                for excel in uploaded_excel:
                    excel_name = excel.name[:-5]  # due to .xlsx
                    for json in uploaded_json:
                        json_name = json.name[:-5]  # due to .json
                        if excel_name == json_name:
                            self.__DEFAULT_STATE["pair_list"].append({excel: json})

                print("넣은 후", self.__DEFAULT_STATE["pair_list"])
                for i, (key, val) in enumerate(self.__DEFAULT_STATE["pair_list"]):
                    st.write(f"Pair {i+1}:")
                    st.write(f"**Excel**: {key.name}, **JSON**: {val.name}")
                    st.write(f"제외된 파일: {unmatched} ")

                tab2_next_button = st.button("Next", key="tab2")

                if self.check_tab2_input_validity():
                    for s in self.__DEFAULT_STATE:
                        print("after input", s, self.__DEFAULT_STATE[s])

                    if st.button("Next", key="tab2", on_click=self.on_next_click):
                        pass

    def on_next_click(self):
        env = self.__DEFAULT_STATE["environment"]
        if env == "je":
            je_menu = json_to_excel(self)
        elif env == "ej":
            ej_menu = excel_to_json(self)
        else:
            raise ValueError("Not expected environment")

    def get_state(self):
        return self.__DEFAULT_STATE


class json_to_excel(Widget):
    def __init__(self, instance, root=None):
        self.state = instance.get_state()
        super().__init__(root)

    def initUI(self):
        with st.spinner("파일 전환 중.."):
            for s in self.state:
                print("state in jsontoexcel calss", s, self.state[s])

            zip_buffer = self.create_zip_file(self.state["uploaded_file"])
            # Zip 파일 다운로드
            st.download_button(
                label="Download Zip",
                data=zip_buffer,
                file_name="json_to_excel.zip",
                mime="application/zip",
            )

    def create_zip_file(self, uploaded_files):
        # BytesIO 객체 생성
        zip_buffer = BytesIO()

        # Zip 파일 생성
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zf:
            for uploaded_file in uploaded_files:
                file_name = uploaded_file.name[:-5] + ".xlsx"  # to remove .json
                converted_file = self.je_convert_data(uploaded_file)  # gets .xlsx file
                zf.writestr(file_name, converted_file.getvalue())

        # BytesIO 객체의 커서 위치를 파일의 시작으로 이동
        zip_buffer.seek(0)

        return zip_buffer

    def je_convert_data(self, json_file):
        return json2excel.convert_json_to_excel(json_file.getvalue())


class excel_to_json(Widget):
    def __init__(self, instance, root=None):
        self.state = instance.get_state()
        super().__init__(root)

    def ej_convert_data(self, excel_file):
        return excel2json.update_json_with_excel_data(excel_file.getvalue())


if __name__ == "__main__":
    Main()
