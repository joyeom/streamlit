import streamlit as st

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
        col1, col2 = st.columns(2)
        with col1:
            option = st.radio(
                "Select environment",
                key="environment",
                options=["json -> excel", "excel -> json"],
            )
        with col2:
            if option == "json -> excel":
                st.subheader("json -> excel")
                uploaded_file = st.file_uploader(
                    "Choose a File", accept_multiple_files=True, type=".json"
                )
                self.__DEFAULT_STATE["uploaded_file"] = uploaded_file
                need_inspect = st.toggle("include inspection")
                self.__DEFAULT_STATE["need_inspect"] = need_inspect

                next_button = st.button("button")
                if next_button:
                    st.spinner("generating files....")
                    # call json to excel class
                    # if need_inspect add inspect
                    # else convert it and make it download in zip file

            elif option == "excel -> json":
                st.subheader("검수완료된 엑셀 값을 json에다 덮힐 것 입니다")
                st.text("엑셀과 원문 json을 모두 짝지어서 올려주세요")
                # Create an empty placeholder for dynamic content
                placeholder = st.empty()
                with placeholder.container():
                    pair_dict_keys_count = len(self.__DEFAULT_STATE["pair_dict"].keys())
                    self.create_pair_uploader(pair_dict_keys_count)
                    # Function to add more file uploaders dynamically
                    st.button(
                        "add_more",
                        type="primary",
                        on_click=placeholder.write(
                            self.create_pair_uploader(
                                len(self.__DEFAULT_STATE["pair_dict"].keys())
                            )
                        ),
                    )

                submitted = st.button("submit")
                if submitted:
                    st.spinner("generating files....")
                    # generate excel_json using pair_dict
                    # create download button then make it download as zip file
            else:
                raise ValueError("need to select environment")

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
