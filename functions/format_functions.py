from functions import regex_functions
from data import keyword_list, keyword_pattern
from data import MONTHS


def ded_section(input_string: str):

    # best cases first:
    if input_string == "PENSION":
        return "80cc"
    elif input_string == "ELECTRIC" or input_string == "VEHICLE":
        return "80eeb"
    elif input_string == "POLITICAL" or input_string == "PARTY":
        return "80ggb"

    # worst cases second:
    elif input_string in (
        "INS",
        "INSURANCE",
        "LIFE",
        "HEALTH",
        "PROVI",
        "FUND",
        "PF",
        "SCHL",
        "SCHOOL",
        "CLG",
        "COLLEGE",
        "UNIVERSITY",
        "EDUCATIONAL INSTITUTE",
        "EDU INST",
        "STAMP DUTY",
        "REGISTRATION FEES",
        "STAMP",
        "REGISTRAR OFFICE",
    ):
        return "80c"

    elif input_string in ("MONEY", "MUTUAL", "FUND", "ASSET", "FINAN", "LIFE"):
        return "80ccg"

    elif input_string in ("MEDI", "HOSP", "HOSPITAL", "CHECKUP", "BODYCHECKUP", "SCAN"):
        return "80d/80dd"

    elif input_string in (
        "EDU",
        "FINAN",
        "INSTITU",
        "CHARITAB",
        "INT",
        "HOUSE LOAN",
        "INTEREST",
        "INTREST",
    ):
        return "80ee"

    elif input_string in ("DONATION", "DONA", "TRUST", "HOME", "RENT"):
        return "80g"


def format_float(input_string: str, count=False):

    if input_string == "0":
        return "-"

    if regex_functions.isAmount(input_string):
        if not count:
            return "{:,}".format(round(float(input_string), 2))
        return input_string

    return input_string


def chart_key(date):

    seperator = "-" if "-" in date else " " if " " in date else "/"

    # for 26-OCT-2023
    if regex_functions.only_alpha(date) and date.split(seperator)[1].isalpha():
        month_key = date.split(seperator)[1] + f" '{ date.split(seperator)[-1][-2:] }"
        date_key = date.split(seperator)[0] + "\n" + date.split(seperator)[1]

    # for 26-10-2023
    else:
        date = date.split(seperator)

        if date[1].isnumeric():
            month_key = MONTHS[int(date[1]) - 1][:3] + f" '{ date[-1][-2:] }"
            date_key = date[0] + "\n" + MONTHS[int(date[1]) - 1][:3]

        else:
            month_key = date[1] + f" '{ date[-1][-2:] }"
            date_key = date.split(seperator)[0] + "\n" + MONTHS[int(date[1]) - 1][:3]

    return [month_key, date_key]


def find_date(raw):
    date_index = (
        raw[list(raw.keys())[0]]
        if len(raw[list(raw.keys())[0]]) > 6
        else raw[list(raw.keys())[1]]
    )
    date = (
        (
            date_index.split("\n")[0]
            if len(date_index.split("\n")[1]) > 4
            else date_index.replace("\n", "")
        )
        if len(date_index.split("\n")) > 1
        else date_index
    )

    return date


def fetch_amount(raw_entry, trans_type, num_index):

    amount = ""

    if raw_entry.get(trans_type) is not None and len(raw_entry.get(trans_type)) > 1:
        amount = raw_entry.get(trans_type)

    else:
        amount = raw_entry.get("AMOUNT") or raw_entry[list(raw_entry.keys())[num_index]]

    return amount.replace(",", "")


def find_transaction_type(raw: list):
    if "type" in raw:
        return raw.index("type")

    return None


def find_transaction_type(raw_entry, check_index) -> str:

    if raw_entry.get("TYPE") is not None:
        if len(raw_entry.get("TYPE")) == 2:
            return raw_entry.get("TYPE")
        else:
            return "DR" if str(raw_entry.get("TYPE")).lower() == "debit" else "CR"

    if raw_entry.get("CR") is not None and len(raw_entry.get("CR")) > 1:
        return "CR"

    if raw_entry.get("DR") is not None and len(raw_entry.get("DR")) > 1:
        return "DR"

    if len(raw_entry) - 1 == check_index:
        return "CR"

    if (
        raw_entry[list(raw_entry.keys())[check_index]] == "-"
        or raw_entry[list(raw_entry.keys())[check_index]] == ""
    ):
        return "DR"

    return ""


def closing_balance_index(raw: list):
    cb_keys = ["balance(Rs)", "balance"]

    for k in cb_keys:
        if k in raw:
            return raw.index(k)

    return None


def convert_closing_balance(input_string: str):

    balance = input_string

    if "\n" in balance:
        balance = balance.split("\n")

        if len(balance) > 0 and "DR" in balance[1] and "." in balance[0]:
            return f"-{balance[0]}"

    if "." in balance:
        return regex_functions.extract_numbers(balance)

    return None


def find_desc(raw):
    desc = r"" + (
        raw.get("PARTICULARS")
        or raw.get("DESCRIPTION")
        or raw.get("DETAILS")
        or raw.get("NARRATION")
    ).replace("\n", "")

    return desc


def find_attr(raw_desc, transc_type):

    match = regex_functions.primary_attribute_checker(raw_desc)
    attr_desc = []

    if "ATM" in raw_desc:
        if transc_type == "DR":
            attr_desc.append("ATM WITHDRAWAL")

        else:
            attr_desc.append("ATM DEPOSIT")

    elif match == []:
        match = regex_functions.secondary_attribute_checker(raw_desc)

    if len(match) > 0:
        if "WITHDRAWAL TRANSFER" in match[0]:
            attr_desc.append(match[0].replace("WITHDRAWAL TRANSFER", ""))

        elif "WITHDRAWALTRANSFER" in match[0]:
            attr_desc.append(match[0].replace("WITHDRAWALTRANSFER", ""))

        else:
            for string in match:
                attr = regex_functions.ternary_attribute_checker(
                    string, keyword_pattern
                )

                if attr != None:
                    attr_desc.append(attr)

            # pattern_result = regex_functions.ternary_attribute_checker(''.join(match), keyword_pattern)

    return attr_desc


def find_first_float(raw):

    values_list = list(raw.values())

    first_float = next(filter(lambda x: isinstance(x, float), values_list), None)

    return first_float
