import re


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
    for raw in data:
        num_index = find_float(raw)
        check_index = num_index + 1

        is_date = (
            raw[list(raw.keys())[0]]
            if len(raw[list(raw.keys())[0]]) > 6
            else raw[list(raw.keys())[1]]
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
                    raw.get("PARTICULARS") or raw.get("DESCRIPTION") or raw.get("NARRATION")
            ).replace("\n", "")

            trans_type = raw.get("TYPE") or (
                "CR"
                if len(raw) - 1 == check_index
                else ("DR" if raw[list(raw.keys())[check_index]] == "-" else "CR")
            )

            trans_type = (
                "DR"
                if trans_type == "Debit"
                else "CR" if trans_type == "Credit" else trans_type
            )

            amount = (raw.get("AMOUNT") or raw[list(raw.keys())[num_index]]).replace(
                ",", ""
            )

            entry = {
                "date": date,
                "description": desc,
                "type": trans_type,
                "amount": amount,
            }
            entries.append(entry)

    return entries
