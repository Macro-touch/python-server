import re

from functions.extract_attribute import extract_attribute


def find_float(obj):
    index = 0
    for key, value in obj.items():
        try:
            float_value = float(value.replace(",", ""))

            if index != 0 and isinstance(float_value, float):
                return index

        except ValueError:
            pass

        index += 1
    return index


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


def fetch_amount(raw_entry, trans_type, num_index):

    amount = ""

    if raw_entry.get(trans_type) is not None and len(raw_entry.get(trans_type)) > 1:
        amount = raw_entry.get(trans_type)

    else:
        amount = raw_entry.get("AMOUNT") or raw_entry[list(raw_entry.keys())[num_index]]

    return amount.replace(",", "")


def extract_entries(data) -> list[dict]:
    data_upper = []
    entries = []

    for input_dict in data:
        renewed = {
            key.upper(): "-" if value is None else value
            for key, value in input_dict.items()
        }
        data_upper.append(renewed)

    data = data_upper
    for raw_entry in data:
        num_index = find_float(raw_entry)

        is_date = (
            raw_entry[list(raw_entry.keys())[0]]
            if len(raw_entry[list(raw_entry.keys())[0]]) > 6
            else raw_entry[list(raw_entry.keys())[1]]
        )

        date = (
            (
                is_date.split("\n")[0]
                if len(is_date.split("\n")[1]) > 4
                else is_date.replace("\n", "")
            )
            if len(is_date.split("\n")) > 1
            else is_date
        )
        alpha_pattern = re.compile(r"\d+")

        if len(date) > 2 and bool(alpha_pattern.search(date)):
            desc = r"" + (
                raw_entry.get("PARTICULARS")
                or raw_entry.get("DESCRIPTION")
                or raw_entry.get("NARRATION")
            ).replace("\n", "")

            trans_type = find_transaction_type(raw_entry, num_index + 1)
            amount = fetch_amount(raw_entry, trans_type, num_index)
            attribute = extract_attribute(desc, trans_type)

            entry = {
                "date": date,
                "description": desc,
                "type": trans_type,
                "amount": amount,
                "attribute": attribute,
            }
            entries.append(entry)

    return entries
