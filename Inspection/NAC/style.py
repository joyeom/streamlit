import pandas as pd
import re
import numpy as np
import Inspection.language as lang
import Inspection.NAC.chars_error as chars_error
import Inspection.NAC.emcha_error as emcha_error
import Inspection.NAC.red_error as red_error
import Inspection.NAC.emoji_error as emoji_error
import os.path
import pandas as pd
import re
import unicodedata
from datetime import datetime
from io import BytesIO
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from zipfile import ZipFile, ZipInfo
from BBCompiles.Styles import GetFormatStyle, ApplyStyle


# columns = data.columns

# redacted_columns = [col for col in data.columns if 'redacted' in col.lower()]
# emoji_columns = [col for col in data.columns if 'emoji' in col.lower()]
# chars_columns = [col for col in data.columns if 'chars' in col.lower()]
# emcha_columns = [col for col in data.columns if 'emcha' in col.lower()]

# # Change color for distinguishing
# def apply_color(val, color, border_color):
#     if isinstance(val,list):
#         return f'background-color: {color}; border: 1px solid {border_color};'
#     elif pd.notna(val):
#         return f'background-color: {color}; border: 1px solid {border_color};'  # Apply specified color with border
#     else:
#         return ''

# def apply_style(df):
#     with pd.ExcelWriter(save_path, engine='openpyxl') as writer:
#         data_styled = data.style

#     # Apply different colors to each category of columns

#     data_styled = data_styled.applymap(lambda x: apply_color(x, 'pink', 'black'), subset='Duplicated')

#     for col in redacted_columns:
#         data_styled = data_styled.applymap(lambda x: apply_color(x, 'yellow', 'black'), subset=col)
#     for col in emoji_columns:
#         data_styled = data_styled.applymap(lambda x: apply_color(x, 'lightgreen', 'black'), subset=col)
#     for col in chars_columns:
#         data_styled = data_styled.applymap(lambda x: apply_color(x, 'lightblue', 'black'), subset=col)
#     for col in emcha_columns:
#         data_styled = data_styled.applymap(lambda x: apply_color(x, 'cyan', 'black'), subset=col)

#     data_styled.to_excel(writer, index=False, sheet_name='corpus')

# print(f"all checked saved in {save_path}")

def WriteFileToArchive(self, data, filename, style):
        buffer = BytesIO()
        fileInfo = ZipInfo(filename=filename, date_time=datetime.today().timetuple())

        data.to_excel(buffer, index=False)
        wrap_columns = ["C", "D"]
        if "Translation2" in data.columns:
            wrap_columns += ["E"]
        bridge = self.ApplyTemplateStyle(
            style=style,
            buffer=self.ApplyTemplateStyle(
                style=self._Style,
                buffer=buffer,
                overwriteSheetSettings=True,
                wrap_columns=wrap_columns,
            ),
            offset_col=len(self._HeaderColumns),
            applyContent=False,
        )
        del buffer
        self._Archive.writestr(zinfo_or_arcname=fileInfo, data=bridge.getbuffer())

def Export(self):
    return self._Buffer