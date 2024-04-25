from io import BytesIO
import pandas as pd
import json
import streamlit as st
import jsonpickle
import numpy as np

domains_col = ["ecommerce", "refEdu", "socialMedia", "literature", "other"]
checkbox_col = [
    "wrongLang",
    "garbled",
    "nonsensical",
    "noncoherent",
    "typos",
    "missingContext",
    "noneofAbove",
    "freeText",
]


# 주어진 엑셀 파일과 JSON 파일에서 데이터를 읽어들이고 처리하는 함수
def update_json_with_excel_data(excel_file, json_file):

    try:
        json_content = json_file.getvalue()
        og = json.loads(json_content)

    except json.JSONDecodeError:
        st.error("Browses files 안에 보이는 파일들로 선택해주세요")

    # Read Excel file into a DataFrame
    with BytesIO(excel_file.getvalue()) as excel_content:
        excel_df = pd.read_excel(excel_content, engine="openpyxl")  # Open Excel files

    excel_df.replace(
        np.nan, None, inplace=True
    )  # to prevent printing NaN instead of null
    updated_data = excel_df.to_dict(orient="records")

    # apply changes to the json_data
    for idx, ann in enumerate(og["annotations"]):
        ann["annotatorID"] = updated_data[idx]["annotatorID"]
        ann["translation"] = updated_data[idx]["translation"]
        for domain in domains_col:
            ann["domains"][domain] = updated_data[idx][domain]
        for checkbox in checkbox_col:
            ann["checkBoxes"][checkbox] = updated_data[idx][checkbox]

    st.json(og)
    print(type(og))
    updated_json = json.dumps(og, ensure_ascii=False, indent=4)

    return updated_json
