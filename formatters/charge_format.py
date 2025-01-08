from functions import transaction_functions


def format_charge(entry: dict) -> list | None:
    if transaction_functions.charge_checker(entry["description"]) != None:
        return [
            entry["date"],
            entry["description"],
            entry["amount"],
            entry["type"],
        ]

    return None
