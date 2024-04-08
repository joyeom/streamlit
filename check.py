from datetime import datetime
from BBCompiles.Files import FilePreview, FileProcessor
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


from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import PatternFill, Border, Side, Alignment
import pandas as pd
from io import BytesIO
import zipfile

def apply_color(val, color, border_color):
    if isinstance(val,list):
        return f'background-color: {color}; border: 1px solid {border_color};'
    elif pd.notna(val):
        return f'background-color: {color}; border: 1px solid {border_color};'  # Apply specified color with border
    else:
        return ''

st.set_page_config(page_title="File Compiler", page_icon="./Inspection/Flitto_CI_Logotype_Blue_Email.png")
st.title('내부검수')

# uploaded_file = st.file_uploader("Choose a File",accept_multiple_files=True,type=".xlsx")

# option = st.selectbox(
#     label = "작업환경",
#     options = ('Select an environment', 'NAC', 'EXCEL'),
#     index=0  # 'Select an environment'가 기본값이 됩니다.
#     )

# src_lang_options = ["src_lang"] + lang.bb_language
# tgt_lang_options = ["tgt_lang"] + lang.bb_language
# src_lang = st.selectbox(label = "Source lang" , options = src_lang_options,index=0)
# tgt_lang = st.selectbox(label = "Target lang" , options = tgt_lang_options,index=0)

# st.session_state["uploaded_file"] = uploaded_file
# st.session_state["environment"] = option
# st.session_state["src_lang"] = src_lang
# st.session_state["tgt_lang"] = tgt_lang

# print(st.session_state["environment"],st.session_state["uploaded_file"],st.session_state["src_lang"],st.session_state["tgt_lang"] )





        
    # if st.session_state["uploaded_file"] is None:
    #     return False
    # if st.session_state["environment"] == "":
    #     return False
    # if st.session_state["src_lang"] == "":
    #     return False
    # if st.session_state["tgt_lang"] == "":
    #     return False
    # return True

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
            "uploaded_file" : [],
            "environment": "",
            "src_lang" : "",
            "tgt_lang" : ""
        }
        self.input_validity = False
        self.DEFAULT_SETTINGS()
        super().__init__(root)
    
    def initUI(self):
        uploaded_file = st.file_uploader("Choose a File",accept_multiple_files=True,type=".xlsx")
        environment = st.selectbox(
            label = "작업환경",
            options = ('Select an environment', 'NAC', 'EXCEL'),
            index=0  # 'Select an environment'가 기본값이 됩니다.
            )

        src_lang_options = ["src_lang"] + lang.bb_language
        tgt_lang_options = ["tgt_lang"] + lang.bb_language
        src_lang = st.selectbox(label = "Source lang" , options = src_lang_options,index=0)
        tgt_lang = st.selectbox(label = "Target lang" , options = tgt_lang_options,index=0)

        self.__DEFAULT_STATE["uploaded_file"] = uploaded_file
        self.__DEFAULT_STATE["environment"] = environment
        self.__DEFAULT_STATE["src_lang"] = src_lang
        self.__DEFAULT_STATE["tgt_lang"] = tgt_lang
        
        if self.check_input_validity():
            for s in self.__DEFAULT_STATE:
                print("after input",s,self.__DEFAULT_STATE[s])

            if st.button("Next", on_click=self.on_next_click):
                pass

    def on_next_click(self):
        processor_menu = ProcessorMenu(self)

    def DEFAULT_SETTINGS(self):
        for state in self.__DEFAULT_STATE:
            if state not in st.session_state:
                st.session_state[state] = self.__DEFAULT_STATE[state]
            print("Default setting st.session_state[state]",state,st.session_state[state],self.__DEFAULT_STATE[state])

    def check_input_validity(self):
        self.input_validity = all([
            self.__DEFAULT_STATE["uploaded_file"] != [],
            self.__DEFAULT_STATE["environment"] != "",
            self.__DEFAULT_STATE["environment"] != "Select an environment",
            self.__DEFAULT_STATE["src_lang"] != "",
            self.__DEFAULT_STATE["src_lang"] != "src_lang",
            self.__DEFAULT_STATE["tgt_lang"] != "",
            self.__DEFAULT_STATE["tgt_lang"] != "tgt_lang",
        ])

        return self.input_validity

    def get_state(self):
        return self.__DEFAULT_STATE

# Processor Menu
class ProcessorMenu(Widget):
    def __init__(self, main_instance,root=None):
        self.state = main_instance.get_state()
        super().__init__(root)
    
    def initUI(self):
        with st.spinner("내부검수 파일 만드는 중.."):
            print("state",self.state)
            
            
            uploaded_files = self.state["uploaded_file"]
            environment = self.state["environment"]
            src_lang = self.state["src_lang"]
            tgt_lang = self.state["tgt_lang"]
            
            zip_buffer = self.create_zip_file(uploaded_files, src_lang, tgt_lang, environment)
        
            # Zip 파일 다운로드
            st.download_button(label="Download Zip", data=zip_buffer, file_name='Inspection_files.zip', mime='application/zip')

    def create_zip_file(self, uploaded_files, src_lang, tgt_lang, environment):
        # BytesIO 객체 생성
        zip_buffer = BytesIO()

        # Zip 파일 생성
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zf:
            for uploaded_file in uploaded_files:
                if environment == "EXCEL":
                    file_name, df = self.process_excel_data(uploaded_file, src_lang, tgt_lang)
                elif environment == "NAC":
                    file_name, df = self.process_nac_data(uploaded_file, src_lang, tgt_lang)

                # DataFrame을 Excel 파일로 변환하여 BytesIO에 쓰기
                excel_buffer = BytesIO()
                df.to_excel(excel_buffer, index=False)
                excel_buffer.seek(0)
                
                # Zip 파일에 추가
                zf.writestr(file_name, excel_buffer.getvalue())

        # BytesIO 객체의 커서 위치를 파일의 시작으로 이동
        zip_buffer.seek(0)

        return zip_buffer

    def process_excel_data(self, f, src_lang, tgt_lang):
        # 파일명 설정
        file_name = f.name
        
        # DataFrame으로 변환
        df = pd.read_excel(f, engine='openpyxl')
        only_data = df.iloc[2:,] 
        only_data["Duplicated"] = only_data["f_id"].duplicated(keep = False)  #check if origin has same content -> excel에서는 origin으로 정렬
        only_data = excel_red_error.check_redacted(only_data)
        only_data = excel_emoji_error.get_emojis(only_data)
        only_data = excel_chars_error.get_chars_error(only_data)
        only_data = excel_emcha_error.get_emcha(only_data,src_lang,tgt_lang)
        return file_name, only_data

    def process_nac_data(self, f, src_lang, tgt_lang):
        # 파일명 설정
        file_name = f.name
        
        # DataFrame으로 변환
        df = pd.read_excel(f, engine='openpyxl')
        df["Duplicated"] = df["SID"].duplicated(keep=False)  # check if origin has same content -> excel에서는 origin으로 정렬
        df = nac_red_error.check_redacted(df)
        df = nac_emoji_error.get_emojis(df)
        df = nac_chars_error.get_chars_error(df)
        df = nac_emcha_error.get_emcha(df, src_lang, tgt_lang)

        return file_name, df
                

            
if __name__ == "__main__":
    Main()




































# def check_input_validity(): #나중에 좀 예쁘게 쓰기
#     if st.session_state["uploaded_file"] is None:
#         return False
#     if st.session_state["environment"] == "Select an environment":
#         return False
#     if st.session_state["src_lang"] == "src_lang":
#         return False
#     if st.session_state["tgt_lang"] == "tgt_lang":
#         return False
#     return True



# with st.spinner("내부검수 파일 만드는 중.."):
#     if check_input_validity():
#         if st.session_state["environment"] == "EXCEL":
#         #print("type(uploaded_file)",type(uploaded_file)) #<class 'list'>
#         # BytesIO 객체 생성
#             zip_buffer = BytesIO()

#         # Zip 파일 생성
#             with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zf:
#                 for f in uploaded_file:
#                     # 파일명 설정
#                     file_name = f.name
                    
#                     # DataFrame으로 변환
#                     df = pd.read_excel(f, engine='openpyxl')
#                     only_data = df.iloc[2:,] 
#                     only_data["Duplicated"] = only_data["f_id"].duplicated(keep = False)  #check if origin has same content -> excel에서는 origin으로 정렬
#                     only_data = excel_red_error.check_redacted(only_data)
#                     only_data = excel_emoji_error.get_emojis(only_data)
#                     only_data = excel_chars_error.get_chars_error(only_data)
#                     only_data = excel_emcha_error.get_emcha(only_data,src_lang,tgt_lang)
                    
#                 # DataFrame을 Excel 파일로 변환하여 BytesIO에 쓰기
#                 excel_buffer = BytesIO()
#                 only_data.to_excel(excel_buffer, index=False)
#                 excel_buffer.seek(0)
                
#                 # Zip 파일에 추가
#                 zf.writestr(file_name, excel_buffer.getvalue())

        
#             # BytesIO 객체의 커서 위치를 파일의 시작으로 이동
#             zip_buffer.seek(0)

#             # Zip 파일 다운로드
#             st.download_button(label="Download Zip", data=zip_buffer, file_name='Inspection_files.zip', mime='application/zip')

#         elif st.session_state["environment"] == "NAC":
#             # BytesIO 객체 생성
#             zip_buffer = BytesIO()

#         # Zip 파일 생성
#             with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zf:
#                 for f in uploaded_file:
#                     # 파일명 설정
#                     file_name = f.name
                    
#                     # DataFrame으로 변환
#                     df = pd.read_excel(f, engine='openpyxl')
#                     df["Duplicated"] = df["SID"].duplicated(keep=False)  # check if origin has same content -> excel에서는 origin으로 정렬
#                     df = nac_red_error.check_redacted(df)
#                     df = nac_emoji_error.get_emojis(df)
#                     df = nac_chars_error.get_chars_error(df)
#                     df = nac_emcha_error.get_emcha(df, src_lang, tgt_lang)


#                 # DataFrame을 Excel 파일로 변환하여 BytesIO에 쓰기
#                 excel_buffer = BytesIO()
#                 df.to_excel(excel_buffer, index=False)
#                 excel_buffer.seek(0)
                
#                 # Zip 파일에 추가
#                 zf.writestr(file_name, excel_buffer.getvalue())

        
#             # BytesIO 객체의 커서 위치를 파일의 시작으로 이동
#             zip_buffer.seek(0)

#             # Zip 파일 다운로드
#             st.download_button(label="Download Zip", data=zip_buffer, file_name='Inspection_files.zip', mime='application/zip')



  
















#   for f in uploaded_file:
#     # Read file content into bytes
#     file_content = f.read()
#     df = pd.read_excel(f, engine='openpyxl')
#     only_data = df.iloc[2:,] 
#     only_data["Duplicated"] = only_data["f_id"].duplicated(keep = False)  #check if origin has same content -> excel에서는 origin으로 정렬
#     only_data = excel_red_error.check_redacted(only_data)
#     only_data = excel_emoji_error.get_emojis(only_data)
#     only_data = excel_chars_error.get_chars_error(only_data)
#     only_data = excel_emcha_error.get_emcha(only_data,src_lang,tgt_lang)

    
#     # BytesIO 객체 생성
#     bridge = BytesIO()
#     only_data.to_excel(bridge, index=False, header=True)
#     # BytesIO 객체의 커서 위치를 파일의 시작으로 이동
#     bridge.seek(0)


#     st.download_button(label="Download Excel", data=bridge, file_name=f"added_{f.name}+.xlsx", mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    
#     #@st.cache_data(ttl=36000) #36000seconds = 10 hours cache 저장
#     if st.session_state["environment"] == "NAC":
#         # NAC processor 하나 만들기
#         df["Duplicated"] = df["SID"].duplicated(keep=False)  # check if origin has same content -> excel에서는 origin으로 정렬
#         df = nac_red_error.check_redacted(df)
#         df = nac_emoji_error.get_emojis(df)
#         df = nac_chars_error.get_chars_error(df)
#         df = nac_emcha_error.get_emcha(df, src_lang, tgt_lang)

#         # Apply different colors to each category of columns
#         redacted_columns = [col for col in df.columns if 'redacted' in col.lower()]
#         emoji_columns = [col for col in df.columns if 'emoji' in col.lower()]
#         chars_columns = [col for col in df.columns if 'chars' in col.lower()]
#         emcha_columns = [col for col in df.columns if 'emcha' in col.lower()]

#         data_styled = df.style

#         data_styled = data_styled.applymap(lambda x: apply_color(x, 'pink', 'black'), subset='Duplicated')

#         for col in redacted_columns:
#             data_styled = data_styled.applymap(lambda x: apply_color(x, 'yellow', 'black'), subset=col)
#         for col in emoji_columns:
#             data_styled = data_styled.applymap(lambda x: apply_color(x, 'lightgreen', 'black'), subset=col)
#         for col in chars_columns:
#             data_styled = data_styled.applymap(lambda x: apply_color(x, 'lightblue', 'black'), subset=col)
#         for col in emcha_columns:
#             data_styled = data_styled.applymap(lambda x: apply_color(x, 'cyan', 'black'), subset=col)

#         # # Display the DataFrame with applied styling
#         # st.subheader("Changed DataFrame:")
#         # st.dataframe(data_styled, hide_index=True)

#         # Export the styled DataFrame to Excel
#         st.markdown("### Download Changed DataFrame as Excel")
#         #excel_file = data_styled.to_excel(index=False, header=True)
#         st.download_button(label="Download Excel", data=data_styled, file_name='styled_data.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


#     elif st.session_state["environment"] == "EXCEL":
#         only_data = df.iloc[2:,] 
#         only_data["Duplicated"] = only_data["f_id"].duplicated(keep = False)  #check if origin has same content -> excel에서는 origin으로 정렬
#         only_data = excel_red_error.check_redacted(only_data)
#         only_data = excel_emoji_error.get_emojis(only_data)
#         only_data = excel_chars_error.get_chars_error(only_data)
#         only_data = excel_emcha_error.get_emcha(only_data,src_lang,tgt_lang)

#         # Export the styled DataFrame to Excel
#         st.markdown("### Download Changed DataFrame as Excel")
#         #excel_file = data_styled.to_excel(index=False, header=True)
#         st.download_button(label="Download Excel", data=only_data, file_name='styled_data.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')



#          # Load the existing workbook
#         wb = load_workbook(filename=f)
#         ws = wb.active

        
#     else:
#         st.info("작업환경을 선택해주세요")
# else:
#   st.info('파일을 업로드하세요')
