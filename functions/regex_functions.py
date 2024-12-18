import re
from data import keyword_pattern


def isAmount(input_str):
    pattern = r"^[0-9.]+$"
    match = re.match(pattern, input_str)
    return bool(match)


def extract_numbers(input_string):
    check = re.sub(r"[^0-9.]", "", input_string)

    if check and len(check) > 0 and check[-1] == ".":
        return check[:-1]
    return check


def only_alpha(input_string):
    return bool(re.search("[a-zA-Z]", input_string))


def only_number(input_string):
    pattern = re.compile(r"\d+")

    return bool(pattern.search(input_string))


def charges_checker(input_string, piece):
    pattern = re.compile(rf"(?<![a-zA-Z])({piece})(?![a-zA-Z])", re.IGNORECASE)
    match = re.findall(pattern, input_string)

    if match:
        return match[0]
    return None


def deduction_checker(input_string, piece):
    pattern = re.compile(r"\b(?:" + piece + r")\b", flags=re.IGNORECASE)
    match = pattern.search(input_string)

    return bool(match)


def primary_attribute_checker(input_string):
    pattern = re.compile(r"(?=.*[a-zA-Z]{3,})(?=.*\d{3,})[a-zA-Z\d.]+@[a-zA-Z]{3,}")
    match = re.findall(pattern, input_string)

    return match


def secondary_attribute_checker(input_string):
    pattern = re.compile(r"\b[a-zA-Z@\s]{6,}\d*\b")
    match = re.findall(pattern, input_string)

    return match


def ternary_attribute_checker(string):
    pattern_result = keyword_pattern.search(string)
    if not bool(pattern_result):
        return string


def extract_numbers(input_string):
    if re.sub(r"[^0-9.-]", "", input_string)[-1] == ".":
        return re.sub(r"[^0-9.-]", "", input_string)[:-1]

    return re.sub(r"[^0-9.-]", "", input_string)
