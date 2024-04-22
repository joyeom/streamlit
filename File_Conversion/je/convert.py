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
    try:
        content = json_file.read()
        data = json.loads(content)

    except json.JSONDecodeError:
        st.error("Invalid JSON file. Please upload a valid JSON file.")

    extracted_data = extract_data(data)  # returns pandas dataframe

    # Excel 파일로 변환
    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        extracted_data.to_excel(writer, index=False)

    excel_buffer.seek(0)
    return excel_buffer


# df.to_excel("/content/drive/MyDrive/B/LCT/sample.xlsx", engine='openpyxl', index=False)

# # Create a new Excel workbook
# wb = Workbook()
# sheet = wb.active

# from openpyxl.styles import PatternFill

# # Define fill colors
# grey_fill = PatternFill(start_color='BFBFBF', end_color='BFBFBF', fill_type='solid')
# light_green_fill = PatternFill(start_color='90EE90', end_color='90EE90', fill_type='solid')
# light_yellow_fill = PatternFill(start_color='FFFF99', end_color='FFFF99', fill_type='solid')
# light_pink_fill = PatternFill(start_color='FFB6C1', end_color='FFB6C1', fill_type='solid')
# light_blue_fill = PatternFill(start_color='ADD8E6', end_color='ADD8E6', fill_type='solid')


# thin_border = Border(left=Side(style='thin'),
#                      right=Side(style='thin'),
#                      top=Side(style='thin'),
#                      bottom=Side(style='thin'))


# # Add headers to the Excel sheet with color coding and column width adjustments
# headers = df.columns
# for col_index, header in enumerate(headers, start=1):
#     cell = sheet.cell(row=1, column=col_index, value=header)
#     cell.alignment =  Alignment(horizontal='center', vertical='center')
#     cell.border = thin_border
#     if "relevant" in header or header in ["payload", "translation"]:
#         cell.fill = grey_fill if "relevant" in header else light_green_fill
#         column_letter = get_column_letter(col_index)
#         column = sheet.column_dimensions[column_letter]
#         column.width = 60

#     elif header in ["ecommerce", "refEdu", "socialMedia", "literature", "other"]:
#         cell.fill = light_yellow_fill
#     elif header in ["wrongLang", "garbled", "nonsensical", "noncoherent", "typos", "missingContext", "noneofAbove", "freeText"]:
#         cell.fill = light_pink_fill
#     else:
#         cell.fill = light_blue_fill


# for i in range(len(df.columns)):
#   add_start = get_column_letter(i+1)
#   for idx, value in enumerate(df[df.columns[i]], start=2):
#     sheet[f"{add_start}{idx}"] = value
#     sheet[f"{add_start}{idx}"].border = thin_border
#     sheet[f"{add_start}{idx}"].alignment = Alignment(vertical='top',wrapText = True)

# # # Adjust row heights based on content
# # for row in sheet.iter_rows(min_row=2, max_row=len(df) + 1):
# #     relevant_cells = [cell for cell in row if cell.column in ['B','C','D'] and cell.value]
# #     max_height = cell.max_height
# #     for cell in row:
# #         cell.alignment = Alignment(vertical='top',wrapText = True)  # Align text to top ,자동 줄 바꿈
# #     sheet.row_dimensions[row[0].row].height = max_height

# sheet.row_dimensions[1].height = None
# ann_cols = df.columns

# # # Save the Excel file
# wb.save("/content/drive/MyDrive/B/LCT/"+name+".xlsx")
