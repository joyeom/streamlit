import pandas as pd
import re
import numpy as np


def contains_t2(df):
    if df.iloc[0].str.contains("target").sum() == 2:
        return True
    return False


# check emoji
emoji_pattern = r'[\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF\u2600-\u26FF\u2700-\u27BF\◦●•■]|"""|^- |^–'  # 맨앞에 있는 -, """ 있는 것들은 특수문자 처리


def extract_emojis(text):
    if pd.notna(text):
        return ", ".join(re.findall(emoji_pattern, str(text)))
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


def get_emojis(df):
    df["emoji_og"] = df.iloc[:, 2].apply(extract_emojis)
    df["emoji_t1"] = df.iloc[:, 3].apply(extract_emojis)
    df["emoji_error_t1"] = calculate_emoji_error(df["emoji_og"], df["emoji_t1"])

    if contains_t2(df):
        df["emoji_t2"] = df.iloc[:, 4].apply(extract_emojis)
        df["emoji_error_t2"] = calculate_emoji_error(df["emoji_og"], df["emoji_t2"])

    return df
