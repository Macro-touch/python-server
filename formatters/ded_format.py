from functions import format_functions, transaction_functions


def deduct_format(entry: dict) -> list | None:
    is_deduct = transaction_functions.deduct_checker(entry["description"])

    if is_deduct and entry["type"] == "DR":

        return [
            entry["date"],
            entry["description"],
            entry["amount"],
            format_functions.ded_section(is_deduct),
        ]

    return None
