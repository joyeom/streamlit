# we only need annotations from json file
# convert json to excel in NAC so that we can do internal audit tool
import pandas as pd
from openpyxl import Workbook, load_workbook
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment
from openpyxl.utils import get_column_letter
from openpyxl.styles import PatternFill, Border, Side
from io import BytesIO
import json
import streamlit as st
from io import StringIO

# Define styles
grey_fill = PatternFill(start_color="BFBFBF", end_color="BFBFBF", fill_type="solid")
light_green_fill = PatternFill(
    start_color="90EE90", end_color="90EE90", fill_type="solid"
)
light_yellow_fill = PatternFill(
    start_color="FFFF99", end_color="FFFF99", fill_type="solid"
)
light_pink_fill = PatternFill(
    start_color="FFB6C1", end_color="FFB6C1", fill_type="solid"
)
light_blue_fill = PatternFill(
    start_color="ADD8E6", end_color="ADD8E6", fill_type="solid"
)


thin_border = Border(
    left=Side(style="thin"),
    right=Side(style="thin"),
    top=Side(style="thin"),
    bottom=Side(style="thin"),
)


domains_col = ["ecommerce", "refEdu", "socialMedia", "literature", "other"]
errorType_col = [
    "wrongLang",
    "garbled",
    "nonsensical",
    "noncoherent",
    "typos",
    "missingContext",
    "noneofAbove",
    "freeText",
]


def extract_data(data):
    # Extract the desired fields from each annotation and create a list of dictionaries
    annotations_data = []
    for annotation in data["annotations"]:
        annotation_dict = {
            "id": annotation["id"],
            "relevantContextBefore": annotation["relevantContextBefore"],
            "payload": annotation["payload"],
            "relevantContextAfter": annotation["relevantContextAfter"],
            "translation": annotation["translation"],
        }
        annotation_dict.update(
            annotation["checkBoxes"]
        )  # Add checkBoxes keys as columns
        annotation_dict.update(annotation["domains"])  # Add domains keys as columns
        annotations_data.append(annotation_dict)

    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(annotations_data)
    return df



def get_data(json_file):
    # try:
    #    data = json.loads(json_file)

    # except json.JSONDecodeError:
    #     st.error("Invalid JSON file. Please upload a valid JSON file.")

    
    data = json_file.decode('utf-8')
    json_data = json.loads(data)
    #data = json.load(json_file)
    extracted_data = extract_data(json_data)  # returns pandas dataframe

    # Excel 파일로 변환
    excel_buffer = BytesIO()
    wb = Workbook()  # Create a new Workbook
    sheet = wb.active

    sheet = apply_style(sheet, extracted_data)

    wb.save(excel_buffer)

    # with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
    #     apply_style(writer, extracted_data) #apply style to the excel
    #     extracted_data.to_excel(writer, index=False) #write data

    excel_buffer.seek(0)
    return excel_buffer


def apply_style(sheet, df):
    # sheet = writer.sheets["Sheet1"]  # Get the sheet from the writer object

    # Add headers to the Excel sheet with color coding and column width adjustments
    headers = df.columns

    for col_index, header in enumerate(headers, start=1):
        cell = sheet.cell(row=1, column=col_index, value=header)
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border
        if "relevant" in header or header in ["payload", "translation"]:
            cell.fill = grey_fill if "relevant" in header else light_green_fill
            column_letter = get_column_letter(col_index)
            column = sheet.column_dimensions[column_letter]
            column.width = 60

        elif header in domains_col:
            cell.fill = light_yellow_fill
        elif header in errorType_col:
            cell.fill = light_pink_fill
        else:
            cell.fill = light_blue_fill

        for i in range(len(headers)):
            add_start = get_column_letter(i + 1)
            for idx, value in enumerate(df[headers[i]], start=2):
                sheet[f"{add_start}{idx}"] = value  # write value here
                sheet[f"{add_start}{idx}"].border = thin_border
                sheet[f"{add_start}{idx}"].alignment = Alignment(
                    vertical="top", wrapText=True
                )

        sheet.row_dimensions[1].height = None
    return sheet
