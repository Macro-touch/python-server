import json
from formatters.chart_format import ChartFormatter
from pdf_scripts.pdf_build import build_pdf
from pdf_scripts.pdf_chunk_gen import GeneratePDFChunk


def generate_pdf(
    data,
    DR_SORTED_ATTRIBUTES_LIST,
    CR_SORTED_ATTRIBUTES_LIST,
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
    lang
):

    # print("\nDR_SORTED_ATTRIBUTES_LIST: \n")
    # print(DR_SORTED_ATTRIBUTES_LIST)
    # print("\nCR_SORTED_ATTRIBUTES_LIST: \n")
    # print(CR_SORTED_ATTRIBUTES_LIST)

    chart = ChartFormatter(
        data=data,
        dr_sorted_list=DR_SORTED_ATTRIBUTES_LIST[2:],  # without headings
        cr_sorted_list=CR_SORTED_ATTRIBUTES_LIST,
        gross_income=GROSS_INCOME,
        gross_outcome=GROSS_OUTCOME,
        total_dr=TOTAL_OUTCOME,
        total_cr=TOTAL_INCOME,
    )

    line_chart_data = chart.line_chart()
    dr_values = [month_data["DR"] for month_data in line_chart_data[0].values()]
    cr_values = [month_data["CR"] for month_data in line_chart_data[0].values()]
    line_chart_values = [[dr_values, cr_values], line_chart_data[1]]  # points  # Labels

    final = {
        "transactions": data,
        "report": json.dumps(
            {
                "CHG": CHARGES_LIST,
                "MOP": MOP_LIST,
                "HVT": HIGH_VAL_TRANSACTION,
                "UNL": UNUSUAL_LIST,
                "DPL": DUPLICATE_LIST,
                "ATR": DR_SORTED_ATTRIBUTES_LIST,
                "TDS": GOVT_LIST.get('TDS'),
                "GRANT": GOVT_LIST.get('GRANT'),
                "DEDUCTION": GOVT_LIST.get('DEDUCTION'),
                "TAX REFUND": GOVT_LIST.get('TAX REFUND'),
                "ADVANCE TAX": GOVT_LIST.get('ADVANCE TAX'),
                "EMI": GOVT_LIST.get('EMI'),
                "GOVT. CLOSURE": GOVT_LIST.get('CLOSURE'),
                "INTEREST": GOVT_LIST.get('INTEREST'),
                "CLOSURE": CLOSURE,
                "charts": [
                    [chart.pie_debit(), chart.pie_credit()],
                    line_chart_values,
                ]
            }
        ),
    }

    # print(final)

    return final

    pdf_chunk = GeneratePDFChunk(
        table_set1=[
            CHARGES_LIST,
            MOP_LIST,
            HIGH_VAL_TRANSACTION,
            UNUSUAL_LIST,
            DUPLICATE_LIST,
            DR_SORTED_ATTRIBUTES_LIST,
        ],
        table_set2=GOVT_LIST.values(),
        pie_data=[chart.pie_debit(), chart.pie_credit()],
        line_data=line_chart_values,
        closure=CLOSURE,
        lang=lang,
    )

    pdf_build_data = pdf_chunk.get_pdf_data()
    build_pdf(pdf_build_data, '')
