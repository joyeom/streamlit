import pandas as pd
import re
import numpy as np
from Inspection.NAC.emoji_error import emoji_pattern

##check exact
def remove_pes(source):
    punct = r'[\u2000-\u206F\u2E00-\u2E7F\\!\"#$%&()*+,\-./:;<=>?@[\\\]^_`{|}~]'
    emoji= emoji_pattern
    space = r'\s+'

    if pd.notna(source):
        source = re.sub(punct, '', str(source))  # remove punctuation
        source = re.sub(emoji,'',str(source)) #remove emoji
        source = re.sub(space,'',str(source)) #remove newline, space(s), tab
        return source
    else:
        return np.nan


def calculate_chars_error(og,t):
  chars_error = []
  for c_og, c_t in zip(og,t):
    if pd.isna(c_t):
      chars_error.append(False)
    else:
      if c_og == "" and c_t == "" : #check if it is just empty string since it is no need to check
        chars_error.append(False)
      elif c_og.lower() == c_t.lower(): #check capitalization
        chars_error.append(True)
      else:
        chars_error.append(c_og == c_t) #if it has same content then make it TRUE
  return chars_error



def get_chars_error(df):
    chars_og = df["Origin"].apply(remove_pes)
    chars_t1 =  df["Translation1"].apply(remove_pes)
    df["chars_error_t1"] = calculate_chars_error(chars_og, chars_t1)

    if "Translation2" in df.columns:
      chars_t2 = df["Translation2"].apply(remove_pes)
      df["chars_error_t2"] = calculate_chars_error(chars_t1, chars_t2)

    return df