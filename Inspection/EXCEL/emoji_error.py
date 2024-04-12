import pandas as pd
import re
import numpy as np
from Inspection.emoji import emojis
import emoji

# check emoji
emoji_pattern = r'[\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF\u2600-\u26FF\u2700-\u27BF\◦●•■]|"""|^- |^–'

bb_pattern = r'[●•■]|"""|^- |^–'

def extract_emojis(text):
    if pd.notna(text):
        extracted_emojis = []
        for e in emoji.emoji_list(text):
            extracted_emojis.append(e["emoji"])

        extracted_emojis += re.findall(bb_pattern, str(text))

        return ", ".join(extracted_emojis)
    else:
        return np.nan


def calculate_emoji_error(og, t):
    emoji_error_t = []
    for e_og, e_t in zip(og, t):
        if pd.isna(e_t):
            emoji_error_t.append(False)
        else:
            emoji_error_t.append(e_og != e_t)
    return emoji_error_t


def get_emojis(df, has_t2):
    df["emoji_og"] = df.iloc[:, 2].apply(extract_emojis)
    df["emoji_t1"] = df.iloc[:, 3].apply(extract_emojis)
    df["emoji_error_t1"] = calculate_emoji_error(df["emoji_og"], df["emoji_t1"])

    if has_t2:
        df["emoji_t2"] = df.iloc[:, 4].apply(extract_emojis)
        df["emoji_error_t2"] = calculate_emoji_error(df["emoji_og"], df["emoji_t2"])

    return df
