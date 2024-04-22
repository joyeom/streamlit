import pandas as pd
import json


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


# json doesn't allow python True, False, it allows true, false
# json style : null , python style : NaN but if you return as None it will automatically change it to null
def match_json_format(text, col):
    if pd.isna(text) or text == "nan":
        return None
    if isinstance(text, str) and col != "translation":
        try:
            return json.loads(text.lower())
        except (json.JSONDecodeError, AttributeError):
            raise TypeError(f"Unexpected data type. {text}, {type(text)}")
    elif isinstance(text, bool):
        try:
            return json.dumps(text)
        except (json.JSONDecodeError, AttributeError):
            raise TypeError(f"Unexpected data type. {text}, {type(text)}")
    elif isinstance(text, float):
        try:
            return json.dumps(bool(text))
        except (json.JSONDecodeError, AttributeError):
            raise TypeError(f"Unexpected data type. {text}, {type(text)}")


def get_data(df):
    df["translation"] = df["translation"].apply(
        lambda x: match_json_format(x, "translation")
    )
    for d in domains_col:
        df[d] = df[d].apply(lambda x: match_json_format(x, d))
    for c in checkbox_col:
        df[c] = df[c].apply(lambda x: match_json_format(x, c))
    return df


# 주어진 엑셀 파일과 JSON 파일에서 데이터를 읽어들이고 처리하는 함수
def update_json_with_excel_data(excel_file, json_file):
    data = pd.read_excel(excel_file)
    with open(json_file, "r") as jf:
        og = json.load(jf)

    updated_data = get_data(
        data
    )  # excel에서 값이 변경 된거 를 json 에 잎힐건데, json 형식에 맞게 수정할꺼야

    # apply changes to the json_data
    for idx, ann in enumerate(og["annotations"]):
        ann["translation"] = updated_data["translation"][idx]
        for domain in domains_col:
            ann["domains"][domain] = updated_data[domain][idx]
        for checkbox in checkbox_col:
            ann["checkBoxes"][checkbox] = updated_data[checkbox][idx]
