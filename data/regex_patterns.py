import re
from data.keywords import attr_keywords_3, govt_keywords, deduct_keyword_list

date_regex = re.compile(
    r"\b(?:\d{2}-\d{2}-\d{4}|\d{2}/\d{2}/\d{4}|\d{2}/\d{2}/\d{2}|\d{4}-\d{2}-\d{2}|\d{2}-\d{2}-\d{2}|\d{2}\.\d{2}\.\d{4}|\d{4}/\d{2}/\d{2}|\d{8}|\d{4}\.\d{2}\.\d{2}|\d{1,2}-(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*-\d{4}|\d{1,2}\s(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s\d{4}|\d{1,2}\s(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s\d{2}|\d{1,2}\s(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*,?\s\d{4}|\d{1,2}\s(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*|\d{4}/\d{2}/\d{2})\b"
)

govt_pattern = re.compile(
    rf'(?<![a-zA-Z0-9]){ "|".join(map(re.escape, govt_keywords)) }(?![a-zA-Z0-9])',
    re.IGNORECASE,
)

keyword_pattern = re.compile(
    r"\b(?:" + "|".join(map(re.escape, attr_keywords_3)) + r")\b", flags=re.IGNORECASE
)

deduct_key_pattern = re.compile(
    r"\b(?:" + deduct_keyword_list + r")\b", flags=re.IGNORECASE
)
