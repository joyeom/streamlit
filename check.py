from datetime import datetime
import streamlit as st
import tracemalloc
import pandas as pd
import re
import numpy as np
import Inspection.language as lang

# NAC
from Inspection.NAC import chars_error as nac_chars_error
from Inspection.NAC import emcha_error as nac_emcha_error
from Inspection.NAC import red_error as nac_red_error
from Inspection.NAC import emoji_error as nac_emoji_error

# EXCEL
from Inspection.EXCEL import chars_error as excel_chars_error
from Inspection.EXCEL import emcha_error as excel_emcha_error
from Inspection.EXCEL import red_error as excel_red_error
from Inspection.EXCEL import emoji_error as excel_emoji_error

import openpyxl
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import PatternFill, Border, Side, Alignment
import pandas as pd
import io
from io import BytesIO
import zipfile
from openpyxl.styles import Font
from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows
import pandas as pd
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment

st.set_page_config(page_title="Inspection", page_icon="./Inspection/Flitto_symbol.jpg")
st.title("내부검수")


# Base Module
class Widget:
    def __init__(self, root=None):
        self._root = root
        self.initUI()

    def initUI(self):
        pass


# Main Programs
class Main(Widget):
    def __init__(self, root=None):
        self.__DEFAULT_STATE = {
            "uploaded_file": [],
            "environment": "",
            "src_lang": "",
            "tgt_lang": "",
        }
        self.input_validity = False
        self.DEFAULT_SETTINGS()
        super().__init__(root)

    def initUI(self):
        uploaded_file = st.file_uploader(
            "Choose a File", accept_multiple_files=True, type=".xlsx"
        )
        environment = st.selectbox(
            label="작업환경",
            options=("Select an environment", "NAC", "EXCEL"),
            index=0,  # 'Select an environment'가 기본값이 됩니다.
        )

        src_lang_options = ["src_lang"] + lang.bb_language
        tgt_lang_options = ["tgt_lang"] + lang.bb_language
        src_lang = st.selectbox(label="Source lang", options=src_lang_options, index=0)
        tgt_lang = st.selectbox(label="Target lang", options=tgt_lang_options, index=0)

        self.__DEFAULT_STATE["uploaded_file"] = uploaded_file
        self.__DEFAULT_STATE["environment"] = environment
        self.__DEFAULT_STATE["src_lang"] = src_lang
        self.__DEFAULT_STATE["tgt_lang"] = tgt_lang

        if self.check_input_validity():
            for s in self.__DEFAULT_STATE:
                print("after input", s, self.__DEFAULT_STATE[s])

            if st.button("Next", on_click=self.on_next_click):
                pass

    def on_next_click(self):
        processor_menu = ProcessorMenu(self)

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

    def check_input_validity(self):
        self.input_validity = all(
            [
                self.__DEFAULT_STATE["uploaded_file"] != [],
                self.__DEFAULT_STATE["environment"] != "",
                self.__DEFAULT_STATE["environment"] != "Select an environment",
                self.__DEFAULT_STATE["src_lang"] != "",
                self.__DEFAULT_STATE["src_lang"] != "src_lang",
                self.__DEFAULT_STATE["tgt_lang"] != "",
                self.__DEFAULT_STATE["tgt_lang"] != "tgt_lang",
            ]
        )

        return self.input_validity

    def get_state(self):
        return self.__DEFAULT_STATE


# Processor Menu
class ProcessorMenu(Widget):
    def __init__(self, main_instance, root=None):
        self.state = main_instance.get_state()
        super().__init__(root)

    def initUI(self):
        with st.spinner("내부검수 파일 만드는 중.."):
            print("state", self.state)

            uploaded_files = self.state["uploaded_file"]
            environment = self.state["environment"]
            src_lang = self.state["src_lang"]
            tgt_lang = self.state["tgt_lang"]

            zip_buffer = self.create_zip_file(
                uploaded_files, src_lang, tgt_lang, environment
            )

            # Zip 파일 다운로드
            st.download_button(
                label="Download Zip",
                data=zip_buffer,
                file_name="Inspection_files.zip",
                mime="application/zip",
            )

    def create_zip_file(self, uploaded_files, src_lang, tgt_lang, environment):
        # BytesIO 객체 생성
        zip_buffer = BytesIO()

        # Zip 파일 생성
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zf:

            for uploaded_file in uploaded_files:
                if environment == "EXCEL":
                    file_name, df = self.process_excel_data(
                        uploaded_file, src_lang, tgt_lang
                    )
                elif environment == "NAC":
                    file_name, df = self.process_nac_data(
                        uploaded_file, src_lang, tgt_lang
                    )

                # DataFrame을 Excel 파일로 변환하여 BytesIO에 쓰기
                excel_buffer = BytesIO()

                # original file
                file_object = io.BytesIO(uploaded_file.getvalue())
                wb = load_workbook(file_object)
                sheet = wb.active  # 첫번째 sheet

                max_col = sheet.max_column
                add_columns = df.columns
                redacted_columns = [col for col in add_columns if "red" in col.lower()]
                emoji_columns = [col for col in add_columns if "emoji" in col.lower()]
                chars_columns = [col for col in add_columns if "chars" in col.lower()]
                emcha_columns = [col for col in add_columns if "emcha" in col.lower()]

                thin_border = Border(
                    left=Side(style="thin"),
                    right=Side(style="thin"),
                    top=Side(style="thin"),
                    bottom=Side(style="thin"),
                )
                # Create an Alignment object with horizontal and vertical alignment set to 'center'
                alignment = Alignment(horizontal="center", vertical="center")

                if environment == "EXCEL":
                    for i in range(len(add_columns)):
                        # make column
                        add_start = get_column_letter(
                            max_col + i + 1
                        )  # A-Z,AA,AB...AZ.BA..
                        sheet.merge_cells(f"{add_start}1:{add_start}3")  # merge row 1-3
                        sheet[f"{add_start}1"].alignment = alignment
                        sheet[f"{add_start}1"].border = thin_border
                        sheet[f"{add_start}1"] = add_columns[i]
                        sheet.column_dimensions[f"{add_start}"].width = 20
                        for idx, value in enumerate(df[add_columns[i]], start=4):
                            if add_columns[i] == "Duplicated":
                                sheet[f"{add_start}1"].fill = PatternFill(
                                    start_color="FFC0CB",
                                    end_color="FFC0CB",
                                    fill_type="solid",
                                )  # pink
                                sheet[f"{add_start}{idx}"].fill = PatternFill(
                                    start_color="FFC0CB",
                                    end_color="FFC0CB",
                                    fill_type="solid",
                                )  # pink
                            elif add_columns[i] in redacted_columns:
                                sheet[f"{add_start}1"].fill = PatternFill(
                                    start_color="FFFF00",
                                    end_color="FFFF00",
                                    fill_type="solid",
                                )  # yellow fil
                                sheet[f"{add_start}{idx}"].fill = PatternFill(
                                    start_color="FFFF00",
                                    end_color="FFFF00",
                                    fill_type="solid",
                                )  # yellow fill
                            elif add_columns[i] in emoji_columns:
                                sheet[f"{add_start}1"].fill = PatternFill(
                                    start_color="90EE90",
                                    end_color="90EE90",
                                    fill_type="solid",
                                )  # light green fill
                                sheet[f"{add_start}{idx}"].fill = PatternFill(
                                    start_color="90EE90",
                                    end_color="90EE90",
                                    fill_type="solid",
                                )  # light green fill
                            elif add_columns[i] in chars_columns:
                                sheet[f"{add_start}1"].fill = PatternFill(
                                    start_color="ADD8E6",
                                    end_color="ADD8E6",
                                    fill_type="solid",
                                )  # light blue fill
                                sheet[f"{add_start}{idx}"].fill = PatternFill(
                                    start_color="ADD8E6",
                                    end_color="ADD8E6",
                                    fill_type="solid",
                                )  # light blue fill
                            elif add_columns[i] in emcha_columns:
                                sheet[f"{add_start}1"].fill = PatternFill(
                                    start_color="00FFFF",
                                    end_color="00FFFF",
                                    fill_type="solid",
                                )  # cyan fill
                                sheet[f"{add_start}{idx}"].fill = PatternFill(
                                    start_color="00FFFF",
                                    end_color="00FFFF",
                                    fill_type="solid",
                                )  # cyan fill
                            sheet[f"{add_start}{idx}"] = str(value)
                            sheet[f"{add_start}{idx}"].border = thin_border

                elif environment == "NAC":
                    for i in range(len(add_columns)):
                        # make column
                        add_start = get_column_letter(
                            max_col + i + 1
                        )  # A-Z,AA,AB...AZ.BA..

                        sheet[f"{add_start}1"].alignment = alignment
                        sheet[f"{add_start}1"].border = thin_border
                        sheet[f"{add_start}1"] = add_columns[i]
                        sheet.column_dimensions[f"{add_start}"].width = 20
                        for idx, value in enumerate(df[add_columns[i]], start=2):
                            if add_columns[i] == "Duplicated":
                                sheet[f"{add_start}1"].fill = PatternFill(
                                    start_color="FFC0CB",
                                    end_color="FFC0CB",
                                    fill_type="solid",
                                )  # pink
                                sheet[f"{add_start}{idx}"].fill = PatternFill(
                                    start_color="FFC0CB",
                                    end_color="FFC0CB",
                                    fill_type="solid",
                                )  # pink
                            elif add_columns[i] in redacted_columns:
                                sheet[f"{add_start}1"].fill = PatternFill(
                                    start_color="FFFF00",
                                    end_color="FFFF00",
                                    fill_type="solid",
                                )  # yellow fil
                                sheet[f"{add_start}{idx}"].fill = PatternFill(
                                    start_color="FFFF00",
                                    end_color="FFFF00",
                                    fill_type="solid",
                                )  # yellow fill
                            elif add_columns[i] in emoji_columns:
                                sheet[f"{add_start}1"].fill = PatternFill(
                                    start_color="90EE90",
                                    end_color="90EE90",
                                    fill_type="solid",
                                )  # light green fill
                                sheet[f"{add_start}{idx}"].fill = PatternFill(
                                    start_color="90EE90",
                                    end_color="90EE90",
                                    fill_type="solid",
                                )  # light green fill
                            elif add_columns[i] in chars_columns:
                                sheet[f"{add_start}1"].fill = PatternFill(
                                    start_color="ADD8E6",
                                    end_color="ADD8E6",
                                    fill_type="solid",
                                )  # light blue fill
                                sheet[f"{add_start}{idx}"].fill = PatternFill(
                                    start_color="ADD8E6",
                                    end_color="ADD8E6",
                                    fill_type="solid",
                                )  # light blue fill
                            elif add_columns[i] in emcha_columns:
                                sheet[f"{add_start}1"].fill = PatternFill(
                                    start_color="00FFFF",
                                    end_color="00FFFF",
                                    fill_type="solid",
                                )  # cyan fill
                                sheet[f"{add_start}{idx}"].fill = PatternFill(
                                    start_color="00FFFF",
                                    end_color="00FFFF",
                                    fill_type="solid",
                                )  # cyan fill

                            sheet[f"{add_start}{idx}"] = str(
                                value
                            )  # datatype상관없이 그냥 string으로
                            sheet[f"{add_start}{idx}"].border = thin_border

                # BytesIO 객체에 엑셀 데이터를 쓰기
                wb.save(excel_buffer)
                excel_buffer.seek(0)
                zf.writestr(file_name, excel_buffer.getvalue())

        # BytesIO 객체의 커서 위치를 파일의 시작으로 이동
        zip_buffer.seek(0)

        return zip_buffer

    def process_excel_data(self, f, src_lang, tgt_lang):
        # 파일명 설정
        file_name = f.name
        # DataFrame으로 변환
        df = pd.read_excel(f, engine="openpyxl")
        only_data = df.iloc[2:,]
        only_data["Duplicated"] = only_data["f_id"].duplicated(
            keep=False
        )  # check if origin has same content -> excel에서는 origin으로 정렬
        only_data = excel_red_error.check_redacted(only_data)
        only_data = excel_emoji_error.get_emojis(only_data)
        only_data = excel_chars_error.get_chars_error(only_data)
        only_data = excel_emcha_error.get_emcha(only_data, src_lang, tgt_lang)

        added_col_loc = only_data.columns.get_loc("Duplicated")
        added_df = only_data.iloc[:, added_col_loc:]

        return file_name, added_df

    def process_nac_data(self, f, src_lang, tgt_lang):

        # 파일명 설정
        file_name = f.name

        # DataFrame으로 변환
        df = pd.read_excel(f, engine="openpyxl")
        df["Duplicated"] = df["SID"].duplicated(
            keep=False
        )  # check if origin has same content -> excel에서는 origin으로 정렬
        df = nac_red_error.check_redacted(df)
        df = nac_emoji_error.get_emojis(df)
        df = nac_chars_error.get_chars_error(df)
        df = nac_emcha_error.get_emcha(df, src_lang, tgt_lang)

        added_col_loc = df.columns.get_loc("Duplicated")
        added_df = df.iloc[:, added_col_loc:]

        return file_name, added_df


if __name__ == "__main__":
    Main()
