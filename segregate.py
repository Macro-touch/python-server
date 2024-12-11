from data import MONTHS, lang_heading
from desc_classifier import DescriptionClassifier
from keyword_checker import KeywordChecker
from generate_pdf import create_pdf


def segregate(data, threshold: int, lang: int):
    m_o_p = {}
    charges = []
    hvt_list = []
    final = []
    table_headings = []
    attr_result = []
    deduction = []

    govt_categories = {
        "TDS": [],
        "Grant": [],
        "Tax Refund": [],
        "Advance Tax": [],
        "EMI": [],
        "Closure": [],
        "Interest": [],
    }

    outflow_labels = []
    inflow_labels = []

    total_income = [0, 0]
    total_outcome = [0, 0]
    table_lang_head = lang_heading[lang]

    for entry in data:
        date = entry.get("date")
        desc = entry.get("description")
        amount = entry.get("amount")
        trans_type = entry.get("type")

        # ############# Checking whether the entry comes under attribute classification ############# #
        checker = KeywordChecker(desc)
        classifier = DescriptionClassifier(desc)
        desc_attribute = checker.contains_keyword()
        if bool(desc_attribute):
            if (
                (len(date) > 1)
                and (len(desc_attribute) > 1)
                and (len(amount) > 1)
                and (len(trans_type) > 1)
            ):
                attr_result.append(entry)
        else:
            pass
        # ############# Checking whether the entry comes under attribute classification ############# #

        # ############# Checking whether the entry comes charges ############# #
        charge_result = checker.contains_non_alphabet_substring()
        if bool(charge_result):
            charges.append(entry)
        # ############# Checking whether the entry comes under charges ############# #

        # ############# Total income outcome ############# #
        if trans_type == "DR":
            total_income[0] += float(amount)
            total_income[1] += 1

        if trans_type == "CR":
            total_outcome[0] += float(amount)
            total_outcome[1] += 1
        # ############# Total income outcome ############# #

        # ############# Verifying Mode of payments ############# #
        mode = classifier.mode_of_payment_finder()
        if mode:
            m_o_p.setdefault(mode, []).append(entry)
        # ############# Verifying Mode of payments ############# #

        # ############# Validating Deductions ############# #
        sub_entry = [entry["DATE"], entry["DESCRIPTION"], entry["AMOUNT"]]
        is_deduction = checker.deduction_checker()
        if bool(is_deduction):
            deduction.append(sub_entry)
        # ############# Validating Deductions ############# #

        # ############# Extracting Govt. Lists ############# #
        classifier.categorize_govt_entry(sub_entry, entry["type"], govt_categories)
        # ############# Extracting Deductions ############# #

        # ############# Validating High Value Transaction ############# #
        if float(threshold) > 0 and (float(amount) > float(threshold)):
            new_hvt = [
                date,
                desc,
                amount if trans_type == "CR" else "-",
                amount if trans_type == "DR" else "-",
            ]
            hvt_list.append(new_hvt)
        # ############# Validating High Value Transaction ############# #

    # Unusual Transaction
    date = ""
    desc_amount_type = {}
    first_date_value = dict

    unusual_list = []
    duplicate_list = []

    for d in attr_result:
        current_date = d["date"]
        current_desc = d["description"]
        current_amount = d["amount"]
        current_type = d["type"]

        combined_text = str(current_desc) + "/" + str(current_amount)

        if current_date != date:

            desc_amount_type.clear()
            date = current_date
            desc_amount_type[combined_text] = current_type

            first_date_value = d  # keeping the first value for adding it later =>

        else:
            if combined_text in desc_amount_type.keys():

                if desc_amount_type[combined_text] != current_type:

                    # adding the first value after checking <=
                    if first_date_value not in unusual_list:
                        unusual_list.append(first_date_value)

                    # avoiding duplicate values.
                    if d not in unusual_list:
                        unusual_list.append(d)
                    # final.append(d)

                else:
                    desc_amount_type[combined_text] = current_type

                    if first_date_value not in duplicate_list:
                        duplicate_list.append(d)

                    if d not in duplicate_list:
                        duplicate_list.append(d)

            # checking for new payee under the same date
            else:
                desc_amount_type[combined_text] = current_type
                first_date_value = d

    # Bank Charges
    charge_list = [list(obj.values())[:-1] + ["Bank Charges"] for obj in charges]
    charge_header = table_lang_head[0]
    if len(charge_list) > 0:
        charge_list.insert(0, charge_header)
    else:
        charge_list.append(["-", "- ", "- ", "-"])
        charge_list.insert(0, charge_header)

    final.append(charge_list)
    table_headings.append("Bank Charges Analysis")

    # Mode Of Payment
    mode_list = []
    for key, value in m_o_p.items():
        d_imps = sum(
            float(obj["AMOUNT"].replace(",", ""))
            for obj in value
            if obj["TYPE"] == "DR" and float(obj["AMOUNT"].replace(",", "")) > 0
        )
        c_imps = sum(
            float(obj["AMOUNT"].replace(",", ""))
            for obj in value
            if obj["TYPE"] == "CR" and float(obj["AMOUNT"].replace(",", "")) > 0
        )
        mode_list.append(
            [key, str(len(value)), "{:.2f}".format(d_imps), "{:.2f}".format(c_imps)]
        )

    mode_header = table_lang_head[1]
    if len(mode_list) > 0:
        mode_list.insert(0, mode_header)
        final.append(mode_list)
    else:
        mode_list.append(["-", "- ", "- "])
        mode_list.insert(0, mode_header)
        final.append(mode_list)

    table_headings.append("UPI - MODE OF PAYMENT\n(STATUS COUNT)")

    # High Value Transaction
    hvt_header = table_lang_head[2]
    # hvt_header = ['Date', 'Decription', 'Amount INFLOW' , 'Amount OUTFLOW']
    if len(hvt_list) > 0:
        hvt_list.insert(0, hvt_header)
        final.append(hvt_list)
    else:
        hvt_list.append(["-", "-", "-", "-"])
        hvt_list.insert(0, hvt_header)
        final.append(hvt_list)

    table_headings.append(f"High Value Transactions")

    # Unusual Transactions
    unusual_trans_list = [list(my_dict.values()) for my_dict in unusual_list]
    unusual_header = table_lang_head[3]
    # unusual_header = ['Date', 'Decription', 'Amount', 'Type']
    if len(unusual_trans_list) > 0:
        unusual_trans_list.insert(0, unusual_header)
        final.append(unusual_trans_list)

    else:
        unusual_trans_list.append([" -", "- ", "- ", "-"])
        unusual_trans_list.insert(0, unusual_header)
        final.append(unusual_trans_list)

    table_headings.append("Unusual Transactions")

    duplicates = [list(my_dict.values()) for my_dict in duplicate_list]
    dup_header = table_lang_head[4]
    # dup_header = ['Date', 'Decription', 'Amount', 'Type']

    if len(duplicates) > 0:
        duplicates.insert(0, dup_header)
        final.append(duplicates)

    else:
        duplicates.append([" -", "- ", "- ", "-"])
        duplicates.insert(0, dup_header)
        final.append(duplicates)

    table_headings.append(f"Duplicate Transactions")

    # Attribute Classification & Month Wise Data

    description_stats = {}
    limit = 3
    date_data = {}
    graph_months = []
    min_amount = 0
    max_amount = 0
    graph_dots = []

    for my_dict in attr_result:

        # --------------- Attr. Classftn. --------------- #
        description_value = my_dict["description"]
        amount_value = float(my_dict["amount"].replace(",", ""))
        transaction_type = my_dict["type"]

        # Initialize count and sum if the 'Description' is not seen before
        if description_value not in description_stats:
            description_stats[description_value] = {
                "Desc": description_value,
                "DR": 0,
                "CR": 0,
                "count": 0,
            }

        # Update count and sum for the 'Description' and type
        description_stats[description_value][transaction_type] = round(
            amount_value, 2
        ) + round(description_stats[description_value][transaction_type])
        description_stats[description_value]["count"] += 1

        # --------------- Month Wise Data --------------- #
        present_date = list(my_dict.values())[0]

        present_date = (
            present_date.split(",")
            if "," in present_date
            else (
                present_date.split("-")
                if "-" in present_date
                else present_date.split("/")
            )
        )

        if present_date[1].isnumeric():
            date_key = (
                MONTHS[int(present_date[1]) - 1][:3] + f" '{ present_date[-1][-2:] }"
            )
        else:
            date_key = present_date[1] + f" '{ present_date[-1][-2:] }"

        if date_key not in graph_months:
            graph_months.append(date_key)

        if date_key not in date_data:
            date_data[date_key] = {"Month": date_key, "DR": 0, "CR": 0}

        date_data[date_key][transaction_type] += amount_value

        if min_amount != 0:
            min_amount = amount_value if amount_value < min_amount else min_amount

        max_amount = amount_value if amount_value > max_amount else max_amount

        if my_dict["TYPE"] == "Debit":
            graph_dots.append((0, amount_value))
        if my_dict["TYPE"] == "Credit":
            graph_dots.append((amount_value, 0))

    attributes_list = [
        list(my_dict.values())[:-1]
        for my_dict in description_stats.values()
        if my_dict["count"]
    ]
    # attributes_list = [list(my_dict.values())[:-1] for my_dict in description_stats.values() if my_dict['count']  > limit]
    # print( my_dict for my_dict in description_stats.values() )
    # print(description_stats.values())

    # line_chart = [ graph_months, graph_dots, min_amount, max_amount ]

    chart_data = []
    attr_header = table_lang_head[5]

    # attr_header = ['Description', 'Debit', 'Credit']
    if len(attributes_list) > 0:

        attributes_list.insert(0, attr_header)
        final.append(attributes_list)

        # print([d[0], d[1]] for d in attributes_list[1:])

        outflow_labels = [[d[0], d[1]] for d in attributes_list[1:]]
        inflow_labels = [[d[0], d[1]] for d in attributes_list[1:]]

        attr_outflow_list = [sublist[-2] for sublist in attributes_list]
        attr_inflow_list = [sublist[-1] for sublist in attributes_list]

        if len(attr_outflow_list) > 0:
            chart_data.append(attr_outflow_list)
        if len(attr_inflow_list) > 0:
            chart_data.append(attr_inflow_list)

    else:
        attributes_list.append(["-", "-", "-"])
        attributes_list.insert(0, attr_header)
        final.append(attributes_list)
    table_headings.append(f"Attribute Classification")

    govt_list = []

    # TDS
    govt_heading = table_lang_head[6]
    if len(govt_categories["TDS"]) > 0:
        govt_categories["TDS"].insert(0, govt_heading)
        govt_list.append(govt_categories["TDS"])

    else:
        govt_categories["TDS"].append(["-", "-", "-"])
        govt_categories["TDS"].insert(0, govt_heading)
        govt_list.append(govt_categories["TDS"])
    table_headings.append(f"List of TDS detucted")
    # print(govt_categories['TDS'])

    if len(govt_categories["Grant"]) > 0:
        govt_categories["Grant"].insert(0, govt_heading)
        govt_list.append(govt_categories["Grant"])

    else:
        govt_categories["Grant"].append(["-", "-", "-"])
        govt_categories["Grant"].insert(0, govt_heading)
        govt_list.append(govt_categories["Grant"])
    table_headings.append(f"Recepit of Government Grant")
    # print(govt_categories['Grant'])

    if len(deduction) > 0:
        deduction.insert(0, govt_heading)
        govt_list.append(deduction)

    else:
        deduction.append(["-", "-", "-"])
        deduction.insert(0, govt_heading)
        govt_list.append(deduction)
    table_headings.append(f"Deduction")
    # print(deduction)

    if len(govt_categories["Tax Refund"]) > 0:
        govt_categories["Tax Refund"].insert(0, govt_heading)
        govt_list.append(govt_categories["Tax Refund"])

    else:
        govt_categories["Tax Refund"].append(["-", "-", "-"])
        govt_categories["Tax Refund"].insert(0, govt_heading)
        govt_list.append(govt_categories["Tax Refund"])
    table_headings.append(f"Tax Refund")
    # print(govt_categories['Tax Refund'])

    if len(govt_categories["Advance Tax"]) > 0:
        govt_categories["Advance Tax"].insert(0, govt_heading)
        govt_list.append(govt_categories["Advance Tax"])

    else:
        govt_categories["Advance Tax"].append(["-", "-", "-"])
        govt_categories["Advance Tax"].insert(0, govt_heading)
        govt_list.append(govt_categories["Advance Tax"])
    table_headings.append(f"Advance tax")
    # print(govt_categories['Advance Tax'])

    if len(govt_categories["EMI"]) > 0:
        govt_categories["EMI"].insert(0, govt_heading)
        govt_list.append(govt_categories["EMI"])

    else:
        govt_categories["EMI"].append(["-", "-", "-"])
        govt_categories["EMI"].insert(0, govt_heading)
        govt_list.append(govt_categories["EMI"])
    table_headings.append(f"EMI")
    # print(govt_categories['EMI'])

    if len(govt_categories["Closure"]) > 0:
        govt_categories["Closure"].insert(0, govt_heading)
        govt_list.append(govt_categories["Closure"])

    else:
        govt_categories["Closure"].append(["-", "-", "-"])
        govt_categories["Closure"].insert(0, govt_heading)
        govt_list.append(govt_categories["Closure"])
    table_headings.append(f"Closure")
    # print(govt_categories['Closure'])

    govt_heading = table_lang_head[7]

    if len(govt_categories["Interest"]) > 0:
        govt_categories["Interest"].insert(0, govt_heading)
        govt_list.append(govt_categories["Interest"])

    else:
        govt_categories["Interest"].append(["-", "-", "-"])
        govt_categories["Interest"].insert(0, govt_heading)
        govt_list.append(govt_categories["Interest"])
    table_headings.append(f"Interest credited and debited")

    if len(final) > 0 and len(govt_list) > 0:
        return create_pdf(
            final,
            govt_list=govt_list,
            outflow_labels=outflow_labels,
            inflow_labels=inflow_labels,
            current_lang=lang,
            table_headings=table_headings,
            chart_data=chart_data,
            total_income=total_income,
            total_outcome=total_outcome,
            line_chart_data=[date_data, graph_months],
        )
