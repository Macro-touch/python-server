import regex_functions


def extract_attribute(raw_desc: str, trans_type: str) -> str:

    match = regex_functions.primary_attribute_checker(raw_desc)
    attr_desc = []

    if "ATM" in raw_desc:
        if trans_type == "DR":
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

    attribute = attr_desc[0] if len(attr_desc) > 0 else "-"
    return attribute
