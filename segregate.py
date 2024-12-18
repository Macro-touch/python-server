from data import table_headings
from functions import format_functions, transaction_functions
from generate_pdf import generate_pdf
from models.model import AttributeModel, DuplicateModel, UnusualModel
from transaction_check import TransactionCheck


def segregate(data: list[dict], threshold: int, lang: int):

    # #### Variables #### #
    header = table_headings["eng"]
    CHARGES_LIST = ["CHG", header["CHG"]]
    MOP_LIST = ["MOP", header["MOP"]]
    MOP_DICT = {}
    AMOUNT_OVERSIGHT = {"DR": [0, 0], "CR": [0, 0]}

    GOVT_LIST = {
        "TDS": ["TDS", header["GOV"]],
        "GRANT": ["GRANT", header["GOV"]],
        "DEDUCTION": ["DEDUCTION", header["DED"]],
        "TAX REFUND": ["REFUND", header["GOV"]],
        "Advance Tax": ["ADVTAX", header["GOV"]],
        "EMI": ["EMI", header["GOV"]],
        "CLOSURE": ["CLOSURE", header["GOV"]],
        "INTEREST": ["INTEREST", header["INT"]],
    }

    UNUSUAL_SET = set()
    UNUSUAL_LIST = ["UNT", header["UNT"]]

    DUPLICATE_SET = set()
    DUPLICATE_LIST = ["DUP", header["UNT"]]

    ATTRIBUTES_DICT = {}
    DR_SORTED_ATTRIBUTES_DICT = []
    CR_SORTED_ATTRIBUTES_DICT = []
    DR_SORTED_ATTRIBUTES_LIST = ["ATTR", header["ATTR"]]
    CR_SORTED_ATTRIBUTES_LIST = []

    HIGH_VAL_TRANSACTION = ["HVT", header["HVT"]]
    # #### Variables #### #

    # #### Function Starts #### #
    for entry in data:
        checker = TransactionCheck(entry)

        if checker.charges_checker() != None:
            CHARGES_LIST.append(checker.charges_checker())

        if checker.mode_of_payment_checker() != None:
            mode = checker.mode_of_payment_checker()

            if mode not in MOP_DICT:
                MOP_DICT[mode] = {"mode": mode, "count": 0, "DR": 0, "CR": 0}

            MOP_DICT[mode]["mode"] = mode
            MOP_DICT[mode]["count"] += 1
            MOP_DICT[mode][entry["type"]] += float(entry["amount"])

        if checker.government_grants() != None:
            govt_key = checker.government_grants()

            if govt_key == "INTEREST":
                GOVT_LIST[govt_key].append(
                    [
                        entry["date"],
                        entry["description"],
                        entry["amount"] if entry["type"] == "DR" else "-",
                        entry["amount"] if entry["type"] == "CR" else "-",
                    ]
                )

            else:
                GOVT_LIST[govt_key].append(
                    [entry["date"], entry["description"], entry["amount"]]
                )

        if checker.deduction_check():
            GOVT_LIST["DEDUCTION"].append(
                [
                    entry["date"],
                    entry["description"],
                    entry["amount"],
                    format_functions.ded_section(checker.deduction_check()),
                ]
            )

        # high value transaction
        transaction_amount = float(entry["amount"])
        if transaction_amount > threshold:
            HIGH_VAL_TRANSACTION.append(
                [
                    entry["date"],
                    entry["attribute"],
                    transaction_amount if entry["type"] == "DR" else "-",
                    transaction_amount if entry["type"] == "CR" else "-",
                ]
            )

        model_entry = [
            entry["date"],
            entry["attribute"],
            entry["amount"],
            entry["type"],
        ]

        # unusual transaction
        unusual = UnusualModel(entry)

        if unusual in UNUSUAL_SET:

            # adding to the list
            UNUSUAL_LIST.append(
                [
                    entry["date"],
                    entry["attribute"],
                    entry["amount"],
                    transaction_functions.type_changer(entry["type"]),
                ]
            )
            UNUSUAL_LIST.append(model_entry)
            # removing after validating
            UNUSUAL_SET.remove(unusual)

        else:
            UNUSUAL_SET.add(unusual)

        # duplicate transaction
        duplicate = DuplicateModel(entry)
        if duplicate in DUPLICATE_SET:
            DUPLICATE_LIST.append(model_entry)
            DUPLICATE_LIST.append(model_entry)

        else:
            DUPLICATE_SET.add(duplicate)

        # attribute classification
        payee = AttributeModel(entry)
        attribute = payee.attribute

        if attribute in ATTRIBUTES_DICT:
            if attribute != "-":

                current_attribute = ATTRIBUTES_DICT[attribute]

                # classifying based on attributes
                current_attribute["attribute"] = attribute
                current_attribute[payee.trans_type] = round(
                    float(current_attribute[payee.trans_type]) + transaction_amount, 2
                )

                # high value transaction for single payee if type is 'Debit'
                if (
                    current_attribute[payee.trans_type] > threshold
                    and payee.trans_type == "DR"
                ):
                    HIGH_VAL_TRANSACTION.append(
                        [
                            entry["date"],
                            entry["attribute"],
                            entry["amount"],
                            "-",
                        ]
                    )

        else:
            if attribute != "-":

                ATTRIBUTES_DICT[attribute] = {
                    "attribute": attribute,
                    "DR": transaction_amount if payee.trans_type == "DR" else 0,
                    "CR": transaction_amount if payee.trans_type == "CR" else 0,
                }

        AMOUNT_OVERSIGHT[entry["type"]][0] += transaction_amount
        AMOUNT_OVERSIGHT[entry["type"]][1] += 1

    MOP_LIST.extend(list(mop.values()) for mop in MOP_DICT.values())

    DR_SORTED_ATTRIBUTES_DICT = dict(
        sorted(ATTRIBUTES_DICT.items(), key=lambda x: x[1]["DR"], reverse=True)
    )
    CR_SORTED_ATTRIBUTES_DICT = dict(
        sorted(ATTRIBUTES_DICT.items(), key=lambda x: x[1]["CR"], reverse=True)
    )

    for dr in DR_SORTED_ATTRIBUTES_DICT.values():
        DR_SORTED_ATTRIBUTES_LIST.append(list(dr.values()))

    for cr in CR_SORTED_ATTRIBUTES_DICT.values():
        CR_SORTED_ATTRIBUTES_LIST.append(list(cr.values()))

    CLOSURE = [
        header["CLS"],
        ["Amount", AMOUNT_OVERSIGHT["DR"][0], AMOUNT_OVERSIGHT["CR"][0]],
        ["Transaction", AMOUNT_OVERSIGHT["DR"][1], AMOUNT_OVERSIGHT["CR"][1]],
    ]

    # THRESHOLD = round((max(float(TOTAL_OUTCOME), float(TOTAL_INCOME)) * 15) / 100, 2)
    TOTAL_OUTCOME = round(AMOUNT_OVERSIGHT["DR"][0], 2)
    TOTAL_INCOME = round(AMOUNT_OVERSIGHT["CR"][0], 2)
    GROSS_OUTCOME = round(TOTAL_OUTCOME * 85 / 100, 2)
    GROSS_INCOME = round(TOTAL_INCOME * 85 / 100, 2)

    generate_pdf(
        data,
        DR_SORTED_ATTRIBUTES_LIST,
        DR_SORTED_ATTRIBUTES_LIST,
        GROSS_INCOME,
        GROSS_OUTCOME,
        TOTAL_INCOME,
        TOTAL_OUTCOME,
        CHARGES_LIST,
        MOP_LIST,
        HIGH_VAL_TRANSACTION,
        UNUSUAL_LIST,
        DUPLICATE_LIST,
        GOVT_LIST,
        CLOSURE,
    )
