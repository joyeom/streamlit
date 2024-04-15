import string
import pandas as pd
from Inspection.puntuation import non_latin_punctuation_dict
from Inspection.language import non_latin

# latin_punctuation =   !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~


def check_punct(text, lang):
    if lang not in non_latin:  # lang is latin
        if text in string.punctuation:
            return text
        else:
            return None  # if it is character
    else:  # lang is non_latin
        if text in non_latin_punctuation_dict[lang].keys():
            return non_latin_punctuation_dict[lang][
                text
            ]  # non_latin punctuation would be converted to latin punctuation
        elif text in string.punctuation:  # non_latin but written in latin punctuation
            return text
        else:
            return None  # if it is character


def compare_end(og, t, src_lang, tgt_lang):
    og_end = og.strip()[-1]
    t_end = t.strip()[-1]
    is_og_punct = check_punct(og_end, src_lang)
    is_t_punct = check_punct(t_end, tgt_lang)

    if is_og_punct != is_t_punct:
        return True
    else:
        return False


def calculate_end(og, t, src_lang, tgt_lang):
    end_punct_error = []
    for e_og, e_t in zip(og, t):
        if pd.isna(e_t):  # 번역이 없는 경우
            end_punct_error.append(False)
        else:
            end_punct_error.append(compare_end(e_og, e_t, src_lang, tgt_lang))
    return end_punct_error


def get_end_punct_error(df, has_t2, src_lang, tgt_lang):
    origin = df.iloc[:, 2]
    t1 = df.iloc[:, 3]

    df["end_punct_error_t1"] = calculate_end(origin, t1, src_lang, tgt_lang)

    if has_t2:
        t2 = df.iloc[:, 4]
        df["end_punct_error_t2"] = calculate_end(origin, t2, src_lang, tgt_lang)

    return df
