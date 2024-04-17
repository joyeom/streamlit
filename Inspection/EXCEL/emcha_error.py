import pandas as pd
import re
import numpy as np
from Inspection.EXCEL.red_error import red_pattern
from Inspection.EXCEL.emoji_error import emoji_pattern

# english, portuguese tokenizer
import nltk

nltk.download("punkt")
from nltk.tokenize import word_tokenize

# vietnmaese tokenizer
from underthesea import word_tokenize

# chinese tokenizer
import jieba

# japanese tokenize
from pyknp import Juman


# remove red_pattern and emoji_pattern
def remove_re(text):
    rep = f"({red_pattern})|({emoji_pattern})"
    removed = text.apply(lambda t: re.sub(rep, "", str(t), flags=re.IGNORECASE))
    return removed


def contains_t2(df):
    if df.iloc[0].str.contains("target").sum() == 2:
        return True
    return False


def tokenize_vietnamese(text):
    return word_tokenize(text)


def tokenize_english(text):
    return word_tokenize(str(text))


def tokenize_chinese(text):
    return jieba.lcut(text)


def tokenize_japanese(text):
    juman = Juman(jumanpp=False)
    result = juman.analysis(text)
    tokens = [mrph.midasi for mrph in result.mrph_list()]
    return tokens


def tokenize(
    text, lang
):  # 딱히 필요 없이 word_tokenize 쓰면 될꺼 같은데..? #chinese 는 꼭 jieba
    if lang == "vi":
        tokens = text.apply(lambda t: tokenize_vietnamese(t))
    elif (lang == "cn") or (lang == "tw"):
        tokens = text.apply(lambda t: tokenize_chinese(t))
    # if lang == "ko":#너무 오래걸려서
    #   tokens = text.apply(lambda t: tokenize_korean(t))
    elif lang == "jp":
        tokens = text.apply(lambda t: tokenize_japanese(t))
    else:
        tokens = text.apply(
            lambda t: tokenize_english(t)
        )  # if it doesn't have specific targeted open source just use word_tokenize from nltk

    # will add more languages
    return tokens


def is_website_link(text):
    # Regular expression pattern to match website links
    # website_link_pattern =  r'(?:^https?://|^www\.|com$|org$)' #remove "http",".com","www.","org"
    website_link_pattern = r"(https?://|^www|.com$|.net$|.org$|.io$)|@"

    # Check if the text does not match the website link pattern
    return bool(re.search(website_link_pattern, text))


def is_number(text):
    # Regular expression pattern to match any digit characters
    number_pattern = r"\d"

    # Check if the text contains any digit characters
    return bool(re.search(number_pattern, text))


def is_metric(text):
    # Define a regular expression pattern to match metric units
    metric_pattern = (
        r"\b(kg|g|mg|km|cm|mm|m|ml|l|cm\^2|m\^2|mm\^2|cm\^3|m\^3|mm\^3|kph|mph)\b"
    )

    # Check if the pattern matches any part of the text (case-insensitive)
    return bool(re.search(metric_pattern, text, re.IGNORECASE))


def is_punctuation(text):
    # Check if the character is a punctuation mark
    punct_pattern = r"[\u2000-\u206F\u2E00-\u2E7F\\!\"#$%&()*+,\-./:;<=>?@[\\\]^_`{|}~]"

    return bool(re.search(punct_pattern, text))


def is_nan(text):
    return text == "nan"


def find_common_words(og, trans):
    emcha = []
    for og, tran in zip(og, trans):
        if isinstance(tran, list) and (tran == ["nan"] or tran == []):
            common_words = np.nan
            
        else:
            common_words = list(set(og).intersection(set(tran)))  # Get common words
            if common_words:
                common_words = [
                    t
                    for t in common_words
                    if not (
                        is_number(t)
                        or is_website_link(t)
                        or is_metric(t)
                        or is_punctuation(t)
                        or len(t) <= 1
                    )
                ]

                # Check if the word becomes empty after removing unwanted characters

            if len(common_words) == 0:
                common_words = ""

        emcha.append(common_words)

    return emcha


def get_emcha(df, has_t2, src, tg):  # src = source language, tg = target language
    removed_og = remove_re(df.iloc[:, 2])
    removed_t1 = remove_re(df.iloc[:, 3])
    tokenized_og = tokenize(removed_og, src)
    tokenized_t1 = tokenize(removed_t1, tg)
    df["emcha_t1"] = find_common_words(tokenized_og, tokenized_t1)

    if has_t2:
        removed_t2 = remove_re(df.iloc[:, 4])
        tokenized_t2 = tokenize(removed_t2, tg)
        df["emcha_t2"] = find_common_words(tokenized_og, tokenized_t2)

    return df
