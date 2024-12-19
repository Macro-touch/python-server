import re
from data.keywords import attr_keywords_3, govt_keywords, deduct_keyword_list

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
