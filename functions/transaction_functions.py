import re
from data.keywords import charge_keyword
from data.regex_patterns import deduct_key_pattern


def type_changer(type: str) -> str:
    if type == "DR":
        return "CR"
    return "DR"


def charge_checker(input_string):

    for substring in charge_keyword:
        pattern = re.compile(
            rf"(?<![a-zA-Z]){re.escape(substring)}(?![a-zA-Z])", re.IGNORECASE
        )
        if pattern.search(input_string):
            return substring

    return None


def mop_checker(desc):

    mode = None

    if re.search(r"UPI.*?(?=\s|$)", desc):
        mode = "UPI"
    elif re.search(r"IMPS.*?(?=\s|$)", desc):
        mode = "IMPS"
    elif re.search(r"NEFT.*?(?=\s|$)", desc):
        mode = "NEFT"
    elif re.search(r"CHQ.*?(?=\s|$)", desc):
        mode = "CHQ"
    elif re.search(r"RTGS.*?(?=\s|$)", desc) or re.search(r"RTG.*?(?=\s|$)", desc):
        mode = "RTGS"

    return mode


def govt_checker(desc) -> str | None:

    conditions = {
        "TDS": ["TDS"],
        "Grant": ["GRANT"],
        "Tax Refund": ["REFUND", "TAXDEPARTMENT"],
        "Advance Tax": ["ADVTAX", "ADVANCETAX", "PAID"],
        "EMI": ["EMI", "INST", "INSTALLMENT", "INSTALMENT"],
        "Closure": [
            "PF CLOSURE",
            "PENSION CLOSURE",
            "DEPOSIT CLOSURE",
            "CLOSURE",
            "TERMINATED",
        ],
        "Interest": ["INT", "INTEREST", "INT RECEIVED", "INTEREST RECEIVED"],
    }

    for category, keywords in conditions.items():
        if any(keyword in desc for keyword in keywords):
            return category.upper()

    return None


def deduct_checker(desc):
    if deduct_key_pattern.search(desc):
        return deduct_key_pattern.search(desc).group()

    return False
