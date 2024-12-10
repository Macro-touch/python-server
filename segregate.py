import re
from pdf_generate import create

MONTHS = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


def contains_non_alphabet_substring(input_string):
    charge_keyword = [
        "CHARGES",
        "CHG",
        "BG CHARGES",
        "CHRGS",
        "FEE",
        "MISC",
        "MISC-REMIT",
        "BULK",
    ]

    for substring in charge_keyword:
        pattern = re.compile(
            rf"(?<![a-zA-Z]){re.escape(substring)}(?![a-zA-Z])", re.IGNORECASE
        )
        if pattern.search(input_string):
            return substring
    return None


keywords = [
    "tax",
    "ibrtgs",
    "ACCOUNT",
    "neft",
    "upi",
    "imps",
    "chq",
    "rtgs",
    "atm",
    "coll",
    "vps",
    "transfer",
    "paytm",
    "transferee",
    "to",
    "from",
    "by",
    "depo",
    "clearing",
    "withdrawal",
    "NEWCARDISSUE",
    "impbill",
    "trf",
    "payment",
    "chrgs",
    "remit",
    "bank",
    "atm",
    "ecom",
    "pos",
    "apbs",
    "chg",
    "cash",
    "cheque",
    "dd",
    "eft",
    "swift",
    "web",
    "net",
    "liq",
    "mobile",
    "tfr",
    "wdl",
    "dep",
    "deposit",
    "tds",
    "grant",
    "emi",
    "inst",
    "installment",
    "int",
    "interest",
    "pf",
    "pension",
    "deposit",
    "closure",
    "terminated",
    "ins",
    "insurance",
    "refund",
    "advtax",
    "advancetax",
    "bill",
]
keyword_list = "|".join(keywords)
key_pattern = re.compile(r"\b(?:" + keyword_list + r")\b", flags=re.IGNORECASE)
attr_desc = []

deduct_keywords = [
    "INS",
    "INSURANCE",
    "LIFE",
    "HEALTH",
    "PROVI",
    "FUND",
    "PF",
    "PF",
    "SCHL",
    "SCHOOL",
    "CLG",
    "COLLEGE",
    "UNIVERSITY",
    "EDUCATIONAL INSTITUTE",
    "EDU INST",
    "STAMP DUTY",
    "REGISTRATION FEES",
    "STAMP",
    "REGISTRAR OFFICE",
    "PENSION",
    "MONEY",
    "MUTUAL",
    "FUND",
    "ASSET",
    "FINAN",
    "LIFE",
    "MEDI",
    "HOSP",
    "HOSPITAL",
    "CHECKUP",
    "BODYCHECKUP",
    "SCAN",
    "INT",
    "EDU",
    "FINAN",
    "INSTITU",
    "CHARITAB",
    "DONATION",
    "DONA",
    "TRUST",
    "HOME",
    "RENT",
    "INT",
    "HOUSE LOAN",
    "INTEREST",
    "INTREST",
    "ELECTRIC",
    "VEHICLE",
    "POLITICAL",
    "PARTY",
]
deduct_keyword_list = "|".join(deduct_keywords)
deduct_key_pattern = re.compile(
    r"\b(?:" + deduct_keyword_list + r")\b", flags=re.IGNORECASE
)

isDate = ""


def contains_keyword(string):
    result = key_pattern.search(string)
    if not bool(result):
        attr_desc.append(string)


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


lang_heading = {
    0: [
        ["Date", "Decription", "Amount", "Type"],
        ["Particular", "Count", "Amount INFLOW", "Amount OUTFLOW"],
        ["Date", "Decription", "Amount INFLOW", "Amount OUTFLOW"],
        ["Date", "Decription", "Amount", "Type"],
        ["Date", "Decription", "Amount", "Type"],
        ["Description", "Debit", "Credit"],
        ["Date", "Decription", "Amount"],
        ["Date", "Decription", "IN", "OUT"],
    ],
    1: [
        ["தேதி", "விளக்கம்", "தொகை", "வகை"],
        ["விளக்கம்", "எண்ணிக்கை", "வரவுத்தொகை", "செலவுத்தொகை"],
        ["தேதி", "விளக்கம்", "வரவுத்தொகை", "செலவுத்தொகை"],
        ["தேதி", "விளக்கம்", "தொகை", "வகை"],
        ["தேதி", "விளக்கம்", "தொகை", "வகை"],
        ["விளக்கம்", "செலவு", "வரவு"],
    ],
    2: [
        ["തീയതി", "വിവരണം", "തുക", "തരം"],
        ["വിവരണം", "എണ്ണുക", "തുകയുടെ വരവ്", "തുക പുറത്തേക്ക് ഒഴുകുന്നു"],
        ["തീയതി", "വിവരണം", "തുകയുടെ വരവ്", "തുക പുറത്തേക്ക് ഒഴുകുന്നു"],
        ["തീയതി", "വിവരണം", "തുക", "തരം"],
        ["തീയതി", "വിവരണം", "തുക", "തരം"],
        ["വിവരണം", "ഡെബിറ്റ്", "കടപ്പാട്"],
    ],
    3: [
        ["తేదీ", "వివరణ", "మొత్తం", "రకము"],
        ["వివరణ", "లెక్కించు", "ఇన్‌ఫ్లో మొత్తం", "అవుట్‌ఫ్లో మొత్తం"],
        ["తేదీ", "వివరణ", "ఇన్‌ఫ్లో మొత్తం", "అవుట్‌ఫ్లో మొత్తం"],
        ["తేదీ", "వివరణ", "మొత్తం", "రకము"],
        ["తేదీ", "వివరణ", "మొత్తం", "రకము"],
        ["వివరణ", "డెబిట్", "క్రెడిట్"],
    ],
    4: [
        ["तारीख", "विवरण", "मात्रा", "प्रकार"],
        ["विवरण", "गणना", "राशि का प्रवाह", "राशि का बहिर्प्रवाह"],
        ["तारीख", "विवरण", "राशि का प्रवाह", "राशि का बहिर्प्रवाह"],
        ["तारीख", "विवरण", "मात्रा", "प्रकार"],
        ["तारीख", "विवरण", "मात्रा", "प्रकार"],
        ["विवरण", "नामे", "श्रेय"],
    ],
}


def segregate(data, threshold: int, current_lang: int):

    result = []
    charges = []
    m_o_p = {}
    high_value_transaction = {"inflow": [], "outflow": []}

    hvt_list = []
    final = []
    table_headings = []
    attr_result = []

    tds = []
    grant = []
    deduction = []
    tax_refund = []
    ad_tax = []
    emi_list = []
    closure_list = []
    interest_list = []

    outflow_labels = []
    inflow_labels = []

    total_income = [0, 0]
    total_outcome = [0, 0]
    table_lang_head = lang_heading[current_lang]

    new_list = []
    for input_dict in data:
        renewed = {
            key.upper(): "-" if value == None else value
            for key, value in input_dict.items()
        }
        new_list.append(renewed)

    data = new_list

    for raw in data:
        num_index = find_float(raw)
        check_index = num_index + 1

        isDate = (
            raw[list(raw.keys())[0]]
            if len(raw[list(raw.keys())[0]]) > 6
            else raw[list(raw.keys())[1]]
        )

        date = (
            (
                isDate.split("\n")[0]
                if len(isDate.split("\n")[1]) > 4
                else isDate.replace("\n", "")
            )
            if len(isDate.split("\n")) > 1
            else isDate
        )
        alpha_pattern = re.compile(r"\d+")

        if len(date) > 2 and bool(alpha_pattern.search(date)):
            desc = r"" + (
                raw.get("PARTICULARS") or raw.get("DESCRIPTION") or raw.get("NARRATION")
            ).replace("\n", "")

            transc_type = raw.get("TYPE") or (
                "CR"
                if len(raw) - 1 == check_index
                else ("DR" if raw[list(raw.keys())[check_index]] == "-" else "CR")
            )

            transc_type = (
                "DR"
                if transc_type == "Debit"
                else "CR" if transc_type == "Credit" else transc_type
            )

            amount = (raw.get("AMOUNT") or raw[list(raw.keys())[num_index]]).replace(
                ",", ""
            )

            entry = {
                "DATE": date,
                "DESCRIPTION": desc,
                "AMOUNT": amount,
                "TYPE": transc_type,
            }

            # print(entry)

            pattern = re.compile(
                r"(?=.*[a-zA-Z]{3,})(?=.*\d{3,})[a-zA-Z\d.]+@[a-zA-Z]{3,}"
            )
            match = re.findall(pattern, desc)

            if match == []:
                pattern = re.compile(r"\b[a-zA-Z@\s]{6,}\d*\b")
                match = re.findall(pattern, desc)

            if len(match) > 0 and "WITHDRAWAL TRANSFER" in match[0]:
                attr_desc.append(match[0].replace("WITHDRAWAL TRANSFER ", ""))

            else:
                for string in match:
                    pattern_result = key_pattern.search(string)
                    if not bool(pattern_result):
                        # print(string)
                        attr_desc.append(string)

            if attr_desc:
                new_attr_entry = {
                    "DATE": date,
                    "DESCRIPTION": str(attr_desc[0]),
                    "AMOUNT": amount,
                    "TYPE": transc_type,
                }

                if (
                    (len(date) > 1)
                    and (len(str(attr_desc[0])) > 1)
                    and (len(amount) > 1)
                    and (len(transc_type) > 1)
                ):
                    attr_result.append(new_attr_entry)

            else:
                # if none returned
                pass

            attr_desc.clear()

            if (
                (len(date) > 1)
                and (len(desc) > 1)
                and (len(amount) > 1)
                and (len(transc_type) > 1)
            ):
                result.append(entry)

            temp_desc = desc.upper()

            # Totals
            if transc_type == "DR":
                total_income[0] += float(amount)
                total_income[1] += 1

            if transc_type == "CR":
                total_outcome[0] += float(amount)
                total_outcome[1] += 1

            charg_result = contains_non_alphabet_substring(temp_desc)
            if bool(charg_result):
                charges.append(entry)

            mode = None
            if re.search(r"UPI.*?(?=\s|$)", temp_desc):
                mode = "UPI"
            elif re.search(r"IMPS.*?(?=\s|$)", temp_desc):
                mode = "IMPS"
            elif re.search(r"NEFT.*?(?=\s|$)", temp_desc):
                mode = "NEFT"
            elif re.search(r"CHQ.*?(?=\s|$)", temp_desc):
                mode = "CHQ"
            elif re.search(r"RTGS.*?(?=\s|$)", temp_desc) or re.search(
                r"RTG.*?(?=\s|$)", temp_desc
            ):
                mode = "RTGS"

            if mode and mode not in m_o_p:
                m_o_p[mode] = []
            if mode:
                m_o_p[mode].append(entry)

            sub_entry = [entry["DATE"], entry["DESCRIPTION"], entry["AMOUNT"]]

            ded_pattern_result = deduct_key_pattern.search(temp_desc)
            if bool(ded_pattern_result):
                deduction.append(sub_entry)

            # TDS
            if "TDS" in temp_desc:
                tds.append(sub_entry)

            elif "GRANT" in temp_desc:
                grant.append(sub_entry)

            elif "REFUND" in temp_desc or "TAXDEPARTMENT" in temp_desc:
                tax_refund.append(sub_entry)

            elif (
                "ADVTAX" in temp_desc
                or "ADVANCETAX" in temp_desc
                or "PAID" in temp_desc
                or "ADVANCETAX" in temp_desc
            ):
                ad_tax.append(sub_entry)

            elif (
                "EMI" in temp_desc
                or "INST" in temp_desc
                or "INSTALLMENT" in temp_desc
                or "INSTALMENT" in temp_desc
            ):
                emi_list.append(sub_entry)

            elif (
                "PF CLOSURE" in temp_desc
                or "PENSION CLOSURE" in temp_desc
                or "DEPOSIT CLOSURE" in temp_desc
                or "CLOSURE" in temp_desc
                or "TERMINATED" in temp_desc
            ):
                closure_list.append(sub_entry)

            elif (
                "INT" in temp_desc
                or "INTEREST" in temp_desc
                or "INT RECEIVED" in temp_desc
                or "INTEREST RECEIVED" in temp_desc
            ):
                new_interest = [
                    entry["DATE"],
                    desc,
                    entry["AMOUNT"] if entry["TYPE"] == "DR" else 0,
                    entry["AMOUNT"] if entry["TYPE"] == "CR" else 0,
                ]

                interest_list.append(new_interest)

            # High Value Transaction
            if (float(amount) > float(threshold)) and float(threshold) > 0:
                if transc_type == "CR":
                    high_value_transaction["inflow"].append(sub_entry)
                elif transc_type == "DR":
                    high_value_transaction["outflow"].append(sub_entry)

                new_hvt = [
                    date,
                    desc,
                    amount if transc_type == "CR" else "-",
                    amount if transc_type == "DR" else "-",
                ]
                hvt_list.append(new_hvt)

    # print(hvt_list)

    # Unusual Transaction
    date = ""
    desc_amount_type = {}
    first_date_value = dict

    unsual_list = []
    duplicate_list = []

    for d in attr_result:
        current_date = d["DATE"]
        current_desc = d["DESCRIPTION"]
        current_amount = d["AMOUNT"]
        current_type = d["TYPE"]

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
                    if first_date_value not in unsual_list:
                        unsual_list.append(first_date_value)

                    # avoiding duplicate values.
                    if d not in unsual_list:
                        unsual_list.append(d)
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
    # charge_header = ['Date', 'Decription', 'Amount', 'Type']
    charge_header = table_lang_head[0]
    if len(charge_list) > 0:
        charge_list.insert(0, charge_header)
        final.append(charge_list)
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

    # mode_header = ['Particular', 'Count', 'Amount INFLOW' , 'Amount OUTFLOW']
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
    unusual_trans_list = [list(my_dict.values()) for my_dict in unsual_list]
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
        description_value = my_dict["DESCRIPTION"]
        amount_value = float(my_dict["AMOUNT"].replace(",", ""))
        transaction_type = my_dict["TYPE"]

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
    if len(tds) > 0:
        tds.insert(0, govt_heading)
        govt_list.append(tds)

    else:
        tds.append(["-", "-", "-"])
        tds.insert(0, govt_heading)
        govt_list.append(tds)
    table_headings.append(f"List of TDS detucted")
    # print(tds)

    if len(grant) > 0:
        grant.insert(0, govt_heading)
        govt_list.append(grant)

    else:
        grant.append(["-", "-", "-"])
        grant.insert(0, govt_heading)
        govt_list.append(grant)
    table_headings.append(f"Recepit of Government Grant")
    # print(grant)

    if len(deduction) > 0:
        deduction.insert(0, govt_heading)
        govt_list.append(deduction)

    else:
        deduction.append(["-", "-", "-"])
        deduction.insert(0, govt_heading)
        govt_list.append(deduction)
    table_headings.append(f"Deduction")
    # print(deduction)

    if len(tax_refund) > 0:
        tax_refund.insert(0, govt_heading)
        govt_list.append(tax_refund)

    else:
        tax_refund.append(["-", "-", "-"])
        tax_refund.insert(0, govt_heading)
        govt_list.append(tax_refund)
    table_headings.append(f"Tax Refund")
    # print(tax_refund)

    if len(ad_tax) > 0:
        ad_tax.insert(0, govt_heading)
        govt_list.append(ad_tax)

    else:
        ad_tax.append(["-", "-", "-"])
        ad_tax.insert(0, govt_heading)
        govt_list.append(ad_tax)
    table_headings.append(f"Advance tax")
    # print(ad_tax)

    if len(emi_list) > 0:
        emi_list.insert(0, govt_heading)
        govt_list.append(emi_list)

    else:
        emi_list.append(["-", "-", "-"])
        emi_list.insert(0, govt_heading)
        govt_list.append(emi_list)
    table_headings.append(f"EMI")
    # print(emi_list)

    if len(closure_list) > 0:
        closure_list.insert(0, govt_heading)
        govt_list.append(closure_list)

    else:
        closure_list.append(["-", "-", "-"])
        closure_list.insert(0, govt_heading)
        govt_list.append(closure_list)
    table_headings.append(f"Closure")
    # print(closure_list)

    govt_heading = table_lang_head[7]

    if len(interest_list) > 0:
        interest_list.insert(0, govt_heading)
        govt_list.append(interest_list)

    else:
        interest_list.append(["-", "-", "-"])
        interest_list.insert(0, govt_heading)
        govt_list.append(interest_list)
    table_headings.append(f"Interest credited and debited")

    if len(final) > 0 and len(govt_list) > 0:

        return result

        # return {
        #     "data": final,
        #     "govt_list": govt_list,
        #     "outflow_labels": outflow_labels,
        #     "inflow_labels": inflow_labels,
        #     "lang": current_lang,
        #     "table_headings": table_headings,
        #     "chart_data": chart_data,
        #     "total_income": total_income,
        #     "total_outcome": total_outcome,
        #     "line_chart_data": [date_data, graph_months],
        # }

        # create(
        #     final,
        #     govt_list=govt_list,
        #     outflow_labels=outflow_labels,
        #     inflow_labels=inflow_labels,
        #     current_lang=current_lang,
        #     table_headings=table_headings,
        #     chart_data=chart_data,
        #     total_income=total_income,
        #     total_outcome=total_outcome,
        #     line_chart_data=[date_data, graph_months],
        # )


if __name__ == "__main__":
    segregate()
