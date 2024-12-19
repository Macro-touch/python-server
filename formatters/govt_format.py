from functions import transaction_functions


def format_govt(entry: dict) -> list | None:
    govt_key = transaction_functions.govt_checker(entry["description"])
    if govt_key != None:

        if govt_key == "INTEREST":
            return [
                govt_key,
                [
                    entry["date"],
                    entry["description"],
                    entry["amount"] if entry["type"] == "DR" else "-",
                    entry["amount"] if entry["type"] == "CR" else "-",
                ],
            ]

        else:
            return [govt_key, [entry["date"], entry["description"], entry["amount"]]]

    return None
