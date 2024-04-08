from datetime import datetime
from BBCompiles.Files import FilePreview, FileProcessor
import streamlit as st
import tracemalloc


st.set_page_config(page_title="File Compiler", page_icon=":pancakes:")


# Base Module
class Widget:
    def __init__(self, root=None):
        self._root = root
        self.initUI()

    def initUI(self):
        pass


# Main Program
class Main(Widget):
    def __init__(self, root=None):
        self.__DEFAULT_STATE = {
            "SHEET-NAME": "",
            "SHEETS": [],
            "UPLOAD-FILES": [],
            "PROCESSOR": None,
            "DOWNLOAD-FILE": None,
            "FILE-TYPE-SETTINGS": dict(),
            "FUNCTION-SETTINGS-1": ("", "", "", None),
            "FUNCTION-SETTINGS-2": None,
            "FILENAME-SETTINGS": "Master",
        }
        self.DEFAULT_SETTINGS()
        print("root",root) #None
        super().__init__(root)

    def initUI(self):
        st.title("File Compiler written by JIHO")
        FILE_LOADER = FileUploader(root=self)
        print("FileUploader root",self._root) #None

        if st.session_state["UPLOAD-FILES"] != []:
            PROCESSOR_MENU = ProcessorMenu(root=self)
            print("ProcessorMenu root",self._root)#None
        else:
            self.FLUSH("PROCESSOR")

    def DEFAULT_SETTINGS(self):
        for state in self.__DEFAULT_STATE:
            if state not in st.session_state:
                st.session_state[state] = self.__DEFAULT_STATE[state]

            print("Default setting st.session_state[state]",st.session_state[state],state)

    def FLUSH(self, key):
        try:
            st.session_state[key] = self.__DEFAULT_STATE[key]
        except KeyError:
            st.session_state[key] = None


class FileUploader(Widget):
    def __init__(self, root=None):
        super().__init__(root)

    def initUI(self):
        self._files = st.file_uploader(
            label="취합할 파일을 업로드해주세요.여긴 지호가 씀",
            type=".xlsx",
            accept_multiple_files=True,
            on_change=self._root.FLUSH,
            kwargs={"key": "DOWNLOAD-FILE"},
        )

        st.session_state["UPLOAD-FILES"] = self._files


class ProcessorMenu(Widget): #파일 넣고 나서 뒤에 나오는 페이지 전부 
    def __init__(self, root=None):
        super().__init__(root)

    def initUI(self):
        try:
            print('파일 넣어진 후 st.session_state["UPLOAD-FILES"]:',st.session_state["UPLOAD-FILES"]) #파일이 넣어진 후
            st.session_state["PROCESSOR"] = self.CACHE_PROCESSOR(
                files=st.session_state["UPLOAD-FILES"] #실제 excel 파일들 
            ) #FilePreview 객체 return 

            print('파일 넣어진 후 st.session_state["Processor"]',st.session_state["PROCESSOR"])  #<BBCompiles.Files.FilePreview object at 0x000001B19393B750>
            # 함수 채우기
            self.functions = FunctionMenu(root=self)

            # 함수 추가 설정
            with st.expander("추가 함수"):
                self.use_second_function = st.checkbox(label="함수 추가")

                if self.use_second_function:
                    self.second_function = FunctionMenu(root=self, key=2)
                else:
                    self._root.FLUSH("FUNCTION-SETTINGS-2")
                    st.empty()

            with st.expander("파일 이름 설정"):
                self.filename = st.text_input(
                    label="파일 중간에 들어갈 텍스트를 입력해주세요.", value="Master"
                )
                st.session_state["FILENAME-SETTINGS"] = self.filename

            # 특수 Type 설정
            self.file_type = FileType_OptionMenu(root=self)

            # 취합 실행
            self.run_compile = st.button("취합!", on_click=self.COMPILE, type="primary") #on_click 눌렀으때 def COMPILE 소환 

            # 출력 파일 다운로드
            if st.session_state["DOWNLOAD-FILE"] != None: #DOWNLOAD-FILE 은 내가 이제 취합해서 다운받아야할 파일
                self.download_button = st.download_button(
                    label="다운로드",
                    data=st.session_state["DOWNLOAD-FILE"],
                    file_name=f'MASTER_{st.session_state["PROCESSOR"]._LangSet}.zip',
                    mime="application/zip", #다운로드 형식 
                )
        except Exception as e:
            st.empty()

    @st.cache_data(ttl=36000) #36000seconds = 10 hours cache 저장 
    def CACHE_PROCESSOR(_self, files):
        try:
            PROCESSOR = FilePreview(files)
            _self.ERROR_CHECK(PROCESSOR)
            return PROCESSOR

        except Exception as e:
            st.error(e)
            _self._root.FLUSH("UPLOAD-FILES")
            return None

    def ERROR_CHECK(self, processor):
        hasError = False

        for errorType in processor._ErrorFiles:
            if processor._ErrorFiles[errorType] != []:
                hasError = True
                for error in processor._ErrorFiles[errorType]:
                    st.error(f"{errorType}: {error}")

        if hasError == True:
            for file in processor._CompletedFiles:
                st.success(f"Completed Files: {file}")
            raise ValueError("업로드 파일을 확인해주세요.")

    def COMPILE(self):
        print(datetime.today().time())

        for s in st.session_state: #이거 나중에 지우기 
            print(f"state:{s}:{st.session_state[s]}")

        FINAL_PROCESSOR = FileProcessor()

        tracemalloc.start()
        FINAL_PROCESSOR.GetTags(st.session_state["UPLOAD-FILES"])

        with st.spinner("Getting header data..."): #빙글뱅글 
            for file in st.session_state["UPLOAD-FILES"]:
                if file.name == st.session_state["PROCESSOR"]._Headers["FILENAME"]:
                    print("Getting data...")
                    # FINAL_PROCESSOR.SetHeaderData(file)
                    FINAL_PROCESSOR.SetHeaderData(
                        file, st.session_state["PROCESSOR"]._Headers["COLUMNS"]
                    )
                    # print("Getting styles...")
                    # FINAL_PROCESSOR.GetBaseStyle(file)

        print("Load header: ", tracemalloc.get_traced_memory()) #(3836281, 15037713) = (curr memory usage, peak memory usage (bytes))
        tracemalloc.stop()
        with st.spinner("Applying custom types..."):
            for file_type in st.session_state["FILE-TYPE-SETTINGS"]:
                FINAL_PROCESSOR.SetFileType(
                    st.session_state["FILE-TYPE-SETTINGS"][file_type][0],
                    st.session_state["FILE-TYPE-SETTINGS"][file_type][1],
                )

        with st.spinner("Applying parameters..."):
            FINAL_PROCESSOR.SetFilenameSettings(st.session_state["FILENAME-SETTINGS"]) #Master
            FINAL_PROCESSOR.SetEditCheckParams() #안중요
            FINAL_PROCESSOR.SetMtParams()
            FINAL_PROCESSOR.SetMasterCheckParams(
                st.session_state["FUNCTION-SETTINGS-1"], 1 #('Tr1 = Tr2', 'f_id', 'f_id', None)
            )
            FINAL_PROCESSOR.SetMasterCheckParams(
                st.session_state["FUNCTION-SETTINGS-2"], 2
            )

        tracemalloc.start()
        with st.spinner("Compiling raw data..."):
            print("Compiling raw...")
            print(datetime.today().today())
            FINAL_PROCESSOR.CompileRaw(st.session_state["UPLOAD-FILES"])
        with st.spinner("Compiling master data..."):
            print(datetime.today().today())
            print("Compiling master...")
            FINAL_PROCESSOR.CompileMaster()
        print("Compile: ", tracemalloc.get_traced_memory())
        tracemalloc.stop()

        tracemalloc.start()
        with st.spinner("Setting output file parameters..."):
            FINAL_PROCESSOR.SetExportName()

        RawTemplate, MasterTemplate = FINAL_PROCESSOR.GetTemplateStyle()
        print(datetime.today().today())
        tracemalloc.start()
        with st.spinner("Writing raw file..."):
            FINAL_PROCESSOR.WriteFileToArchive(#_RawFile이 새로 쓴 파일 
                FINAL_PROCESSOR._RawFile, FINAL_PROCESSOR._RawFileName, RawTemplate
            )
        print("Write raw file: ", tracemalloc.get_traced_memory())
        tracemalloc.stop()
        with st.spinner("Writing master file..."):
            FINAL_PROCESSOR.WriteFileToArchive(
                FINAL_PROCESSOR._MasterFile,
                FINAL_PROCESSOR._MasterFileName,
                MasterTemplate,
            )

        with st.spinner("Exporting file...)"):
            st.session_state["DOWNLOAD-FILE"] = FINAL_PROCESSOR.Export()
        print("Export:", tracemalloc.get_traced_memory())
        tracemalloc.stop()

        st.error(
            f"취합 제외된 파일: {', '.join(FINAL_PROCESSOR._ErrorFiles['SHEETNAME-ERROR'])}"
        )
        st.success("Compile complete!")
        print(datetime.today().time())


# Base class for options menu
class OptionMenu(Widget):
    def __init__(self, root=None, option_type=None, label="Options"):
        self._option_type = option_type
        self._label = label
        self._option_list = list()
        if f"INSTANCES_{self._option_type}" not in st.session_state.keys():
            st.session_state[f"INSTANCES_{self._option_type}"] = 0
        super().__init__(root)

    def initUI(self):
        with st.expander(label=self._label):

            self._add = st.button(
                label="Add", on_click=self.ADD, key=f"OPTIONS_{self._option_type}"
            )

            for key in st.session_state[self._option_type]:
                self.POPULATE(key)

    def ADD(self):
        st.session_state[f"INSTANCES_{self._option_type}"] += 1
        st.session_state[self._option_type][
            f"{self._option_type}_{st.session_state[f'INSTANCES_{self._option_type}']}"
        ] = []

    def POPULATE(self, key):
        return Option(root=self, key=key)

    def DELETE(self, key):
        st.session_state[self._option_type].pop(key)


# Base class for options widgets
class Option(Widget):
    def __init__(self, root=None, key=0, items=1):
        try:
            print(self._key)
        except Exception:
            self._key = 0
        self._WIDGETS = st.columns(items)
        super().__init__(root=root)

    def initUI(self):

        self.POPULATE()
        self.ADD_DELETE_BUTTON()

    def POPULATE(self):
        with st.container():
            pass

    def ADD_DELETE_BUTTON(self):
        try:
            self._keys.append(f"DELETE_{self._key}")
        except Exception:
            self._keys = [f"DELETE_{self._key}"]

        self.DELETE_BUTTON = self._WIDGETS[-1].button(
            label="x",
            on_click=self._root.DELETE,
            args=[self._key],
            key=self._keys[-1],
            type="primary",
        )


# Actual classes to use for function assignment/file type assignment
class FileType_OptionMenu(OptionMenu):
    def __init__(
        self, root=None, option_type="FILE-TYPE-SETTINGS", label="파일 유형 설정"
    ):
        super().__init__(root=root, option_type=option_type, label=label)

    def POPULATE(self, key):
        return FileType_Option(root=self, key=key)


class FileType_Option(Option):
    def __init__(self, root=None, key=0, items=[7, 3, 1]):
        self._key = key  # f'FILE-TYPE-SETTINGS_{key}'
        self._keys = [f"FILE_{self._key}", f"TYPE_{self._key}"]
        super().__init__(root=root, key=key, items=items)

    def POPULATE(self):

        with st.container():
            self.file_select = self._WIDGETS[0].selectbox(
                label="적용 파일",
                options=st.session_state["PROCESSOR"]._FileNames,
                key=self._keys[0],
            )

            self.file_type = self._WIDGETS[1].text_input(
                label="Type", key=self._keys[1]
            )

            st.session_state[self._root._option_type][self._key] = (
                self.file_select,
                self.file_type,
            )

    def DELETE(self, key):
        st.session_state.pop(f"FILE_{key}")
        st.session_state.pop(f"TYPE_{key}")
        st.session_state[self._option_type].pop(key)


#
class FunctionMenu(Widget):
    def __init__(self, root=None, key=1):
        self._key = key
        self._keys = [f"FTYPE_{key}", f"SRC_{key}", f"TR1_{key}", f"TR2_{key}"]

        super().__init__(root=root)

        print("FUNCTIONMENU 안에서 root",self._root)

    def initUI(self):
        with st.container():
            st.divider()

            self._WIDGETS = st.columns([5, 3, 3, 3, 1])
            columns = list(st.session_state["PROCESSOR"]._Headers["COLUMNS"]) #엑셀 파일 안에 있는 컬럼들

            f_types = ("Tr1 = Tr2", "Source = Tr1 or Tr2")

            self.f_type = self._WIDGETS[0].radio(
                label="검증 유형",
                options=f_types,
                key=self._keys[0],
                on_change=self._root._root.FLUSH,
                args=["DOWNLOAD-FILE"],
            )

            self.tr1 = self._WIDGETS[2].selectbox(
                label="Tr1",
                options=columns, #엑셀 파일 안에 있는 컬럼들 (f_id', 'id', 'Source', 'Translation1', 'Translation2', 'Source is nonsensical'..)
                key=self._keys[2],
                on_change=self._root._root.FLUSH,
                args=["DOWNLOAD-FILE"],
            )

            self.tr2 = self._WIDGETS[3].selectbox(
                label="Tr2",
                options=columns,
                key=self._keys[3],
                on_change=self._root._root.FLUSH,
                args=["DOWNLOAD-FILE"],
            )
            self.src = st.empty()

            if self.f_type == f_types[-1]:
                self.src = self._WIDGETS[1].selectbox(
                    label="Source",
                    options=columns,
                    key=self._keys[1],
                    on_change=self._root._root.FLUSH,
                    args=["DOWNLOAD-FILE"],
                )
            else:
                self.src = None

            st.session_state[f"FUNCTION-SETTINGS-{self._key}"] = (
                self.f_type,
                self.tr1,
                self.tr2,
                self.src,
            )

            st.divider()


if __name__ == "__main__":
    Main()
     # URL을 변경합니다.
    # st.markdown("Local URL: http://34.216.211.155:8501")
    # st.markdown("Network URL: http://34.216.211.155:8501")
