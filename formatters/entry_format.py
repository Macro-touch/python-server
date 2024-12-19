import re

from functions.extract_attribute import extract_attribute
from functions.format_functions import (
    find_date,
    find_desc,
    find_transaction_type,
    find_first_float,
    fetch_amount,
)


def format_entries(data) -> list[dict]:
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
        num_index = find_first_float(raw_entry)

        date = find_date(raw_entry)
        alpha_pattern = re.compile(r"\d+")

        if len(date) > 2 and bool(alpha_pattern.search(date)):

            desc = find_desc(raw_entry)
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
