import re
from data.regex_patterns import keyword_pattern


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


def multiple_dates(input_string):
    # Regex for common date formats
    date_patterns = [
        r"\b\d{2}/\d{2}/\d{2,4}\b",  # dd/mm/yy or dd/mm/yyyy
        r"\b\d{4}-\d{2}-\d{2}\b",  # yyyy-mm-dd
        r"\b\d{1,2}-\w{3}-\d{2,4}\b",  # dd-MMM-yyyy or d-MMM-yy (e.g., 25-Dec-2021)
        r"\b\w{3} \d{1,2}, \d{4}\b",  # MMM dd, yyyy (e.g., Dec 25, 2021)
        r"\b\d{1,2} \w+ \d{4}\b",  # d MMMM yyyy (e.g., 25 December 2021)
    ]

    # Combine all patterns into a single regex
    combined_pattern = "|".join(date_patterns)

    # Find all matches
    matches = re.findall(combined_pattern, input_string, re.IGNORECASE)

    # Return True if there is one match, otherwise False
    return len(matches) > 1
