import re
from functions import regex_functions
from constants.MONTHS import MONTHS


def ded_section(input_string: str):
    input_string = input_string.upper()

    # best cases first:
    if re.search(r'PENSION', input_string):
        return "80cc"

    elif re.search(r'(ELECTRIC|VEHICLE)', input_string):
        return "80eeb"

    elif re.search(r'(POLITICAL|PARTY)', input_string):
        return "80ggb"

    # worst cases second:
    elif re.search(r'\b(INS|INSURANCE|LIFE|HEALTH|PROVI|FUND|PF|SCHL|SCHOOL|CLG|COLLEGE|UNIVERSITY|EDUCATIONAL INSTITUTE|EDU INST|STAMP DUTY|REGISTRATION FEES|STAMP|REGISTRAR OFFICE)\b', input_string):
        return "80c"

    elif re.search(r'\b(MONEY|MUTUAL|FUND|ASSET|FINAN|LIFE)\b', input_string):
        return "80ccg"

    elif re.search(r'\b(MEDI|HOSP|HOSPITAL|CHECKUP|BODYCHECKUP|SCAN)\b', input_string):
        return "80d/80dd"

    elif re.search(r'\b(EDU|FINAN|INSTITU|CHARITAB|INT|HOUSE LOAN|INTEREST|INTREST)\b', input_string):
        return "80ee"

    elif re.search(r'\b(DONATION|DONA|TRUST|HOME|RENT)\b', input_string):
        return "80g"
    
    return "-"


def format_float(input_string: str, count=False):

    if input_string == "0":
        return "-"

    if regex_functions.is_amount(input_string):
        if not count:
            return "{:,}".format(round(float(input_string), 2))
        return input_string

    return input_string


def chart_key(date):

    if "/" in date and " " in date:
        date = date.replace(" ", "")

    separator = "-" if "-" in date else "/" if "/" in date else " "

    # for 26-OCT-2023 or 2 Sep 2023
    if regex_functions.only_alpha(date) or (date.split(separator)[1].isalpha() and date.split(separator)[0].isnumeric()):
        # Extract parts of the date
        parts = date.split(separator)
        day   = parts[0]  # Numeric day
        month = parts[1]  # Month as a word
        year  = parts[2]  # Year

        # Construct the keys
        month_key = month[:3] + f" '{year[-2:]}"  # Abbreviated month + last two digits of the year
        date_key = day + "\n" + month[:3]  # Day + abbreviated month

    # for 26-10-2023
    else:
        date = date.split(separator)

        if date[1].isnumeric():
            month_key = MONTHS[int(date[1]) - 1][:3] + f" '{date[-1][-2:]}"
            date_key = date[0] + "\n" + MONTHS[int(date[1]) - 1][:3]

        else:
            month_key = date[1] + f" '{date[-1][-2:]}"
            date_key = date.split(separator)[0] + "\n" + MONTHS[int(date[1]) - 1][:3]

    return [month_key, date_key]


def find_date(raw):
    keys = list(raw.keys())
    first_val = str(raw[keys[0]])
    sec_val = str(raw[keys[1]])

    date_index = (
        first_val
        if len(first_val) > 6
        else sec_val
    )

    splitted_date = date_index.split("\n")

    date = ""
    
    if len(splitted_date) > 1:
        
        if len(splitted_date[1]) > 4:
            date = splitted_date[0]
        
        elif len(splitted_date[1]) <= 4:
            date = splitted_date[0] + " " + splitted_date[1]
        
        else:
            date_index.replace("\n", "")
    
    else:
        date = splitted_date[0]

    return date


def fetch_amount(raw_entry, trans_type, num_index):

    amount = ""

    if raw_entry.get(trans_type) is not None and len(raw_entry.get(trans_type)) > 1:
        amount = raw_entry.get(trans_type)

    else:
        amount = raw_entry.get("AMOUNT") or raw_entry[list(raw_entry.keys())[num_index]]

    return re.sub("inr", "", str(amount).replace(',', ""), flags=re.IGNORECASE).strip()


def is_float(s: str | float) -> bool:
    if (isinstance(s, float)) or (isinstance(s, int)): 
        return True
    
    if s is None or s == "" or len(s) == 0: 
        return False
    
    try:
        if float(s.replace(",", "")):
            return True
        
    except ValueError:
        return False
    
    return False

def valid_entry(str_list: list[str|None]) -> bool:
    has_date = any(regex_functions.is_date(s) for s in str_list if s is not None)
    has_float = any(is_float(s) for s in str_list if s is not None)
    
    return has_date and has_float

import re

def to_float(value) -> float:
    """
    Convert a string or number in any typical format to a float.
    Handles commas, currency symbols, spaces, and negative signs.
    Returns 0.0 if conversion fails.
    """
    if value is None or value == "":
        return 0.0

    if isinstance(value, (int, float)):
        return float(value)

    # Convert to string and clean up
    value_str = str(value).strip()

    # Remove common currency symbols and spaces
    value_str = re.sub(r'[^\d.,\-]', '', value_str)

    # Handle cases like 1,23,456.78 (Indian) or 1.234.567,89 (European)
    if value_str.count(',') > 1 and '.' in value_str:
        value_str = value_str.replace(',', '')  # Assume comma is a thousand separator
    elif value_str.count('.') > 1 and ',' in value_str:
        value_str = value_str.replace('.', '').replace(',', '.')  # European format
    elif ',' in value_str and '.' not in value_str:
        if len(value_str.split(',')[-1]) == 2:
            value_str = value_str.replace(',', '')  # Treat comma as thousand separator
        else:
            value_str = value_str.replace(',', '.')  # Treat comma as decimal

    try:
        return float(value_str)
    except ValueError:
        return 0.0


def find_transaction_type(raw_entry, check_index) -> str:

    if raw_entry.get("CR/DR") is not None:
        return ''.join(re.findall(r'[a-zA-Z]', str(raw_entry.get("CR/DR")))).upper()

    if raw_entry.get("TYPE") is not None:
        if len(raw_entry.get("TYPE")) == 2:
            return raw_entry.get("TYPE")
        else:
            return "DR" if str(raw_entry.get("TYPE")).lower() == "debit" else "CR"
    
    if 'CREDIT AMOUNT' in raw_entry or 'DEBIT AMOUNT' in raw_entry:
        cr_amount = to_float(raw_entry.get("CREDIT AMOUNT"))
        dr_amount = to_float(raw_entry.get("DEBIT AMOUNT"))

        if (cr_amount > 0): 
            return "CR"

        if (dr_amount > 0): 
            return "DR"
 
    if raw_entry.get("WITHDRAWALS") is not None:
        amt = str(raw_entry.get("WITHDRAWALS"))

        if amt and float(amt.replace(',', '')) > 0: 
            return "DR"
    
    if raw_entry.get("DEPOSITS") is not None:
        amt = str(raw_entry.get("DEPOSITS"))

        if amt and float(amt.replace(',', '')) > 0:
            return "CR"
        
    if raw_entry.get("DEBIT") is not None:
        amt = str(raw_entry.get("DEBIT"))

        if amt and float(amt.replace(',', '')) > 0: 
            return "DR"
    
    if raw_entry.get("CREDIT") is not None:
        amt = str(raw_entry.get("CREDIT"))

        if amt and float(amt.replace(',', '')) > 0:
            return "CR"
    
    if raw_entry.get("WITHDRAWAL") is not None:
        amt = str(raw_entry.get("WITHDRAWAL"))

        if amt and float(amt.replace(',', '')) > 0: 
            return "DR"
    
    if raw_entry.get("DEPOSIT") is not None:
        amt = str(raw_entry.get("DEPOSIT"))

        if amt and float(amt.replace(',', '')) > 0:
            return "CR"

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


def find_desc(raw: dict):
    keys = ["PARTICULARS", "DESCRIPTION", "DETAILS", "NARRATION", "REMARKS"]

    for key in keys:
        if key in raw:
            return [list(raw.keys()).index(key), str(raw.get(key))]
        
    return -1 

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
                attr = regex_functions.ternary_attribute_checker(string)

                if attr != None:
                    attr_desc.append(attr)

            # pattern_result = regex_functions.ternary_attribute_checker(''.join(match), keyword_pattern)

    return attr_desc


def find_cheque_no_index(entry: dict) -> int:

    possible_keys = [
        "CHEQUE\nNO",
        "CHEQUE NO",
        "CHECK NO",
        "CHK NO",
        "REF\nNO./CHEQUE NO",
        "TRAN ID"
    ]

    for key in possible_keys:
        if key in entry:
            return list(entry.keys()).index(key)
    
    return -1


def find_first_float(obj, desc_index):

    cheque_index = find_cheque_no_index(obj)

    index = 0
    for key, value in obj.items():
        if is_float(value):
            float_value = float(str(value).replace(",", ""))

            if index != 0 and index != desc_index and index != cheque_index and isinstance(float_value, float):
                return index

        index += 1

    return index
