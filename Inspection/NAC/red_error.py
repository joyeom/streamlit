import pandas as pd
import re
import numpy as np


# check_redacted
redacted = [
    r"\[\s*redacted_name\s*\]",
    r"\[\s*redacted_address\s*\]",
    r"\[\s*redacted_email\s*\]",
    r"\[\s*redacted_id\s*\]",
    r"\[\s*redacted_number\s*\]",
    r"\[\s*redacted_url\s*\]",
    r"\[\s*redacted_words\s*\]",
    r"\[\s*redacted_info\s*\]",
    r"\[\s*redacted_infos\s*\]",
]

red_pattern = "|".join(redacted)


def extract_redacted(text):
    if pd.notna(text):
        return ", ".join(re.findall(red_pattern, str(text), re.IGNORECASE))
    else:
        return np.nan


def calculate_red_error(og, t):
    red_error_t = []
    for r_og, r_t in zip(og, t):
        if pd.isna(r_t):
            red_error_t.append(False)
        else:
            red_error_t.append(r_og != r_t)
    return red_error_t


def check_redacted(df):
    df["redacted_matched_og"] = df["Origin"].apply(extract_redacted)
    df["redacted_matched_t1"] = df["Translation1"].apply(extract_redacted)
    df["redacted_error_t1"] = calculate_red_error(
        df["redacted_matched_og"], df["redacted_matched_t1"]
    )

    if "Translation2" in df.columns:
        df["redacted_matched_t2"] = df["Translation2"].apply(extract_redacted)
        df["redacted_error_t2"] = calculate_red_error(
            df["redacted_matched_og"], df["redacted_matched_t2"]
        )

    return df
