from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    PageBreak,
    Spacer,
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
import PyPDF2
import sys
import os
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.lib.colors import black, white, blueviolet, darkcyan
from reportlab.graphics.charts.textlabels import Label


# Define a custom style for the Header text
styles = getSampleStyleSheet()
header_style = styles["Heading1"]
header_style.fontSize = 25
header_style.spaceAfter = 15
header_style.fontWeight = "Bold"
header_style.textColor = colors.HexColor("#743BC2")

# Define a custom style for the footer text
styles = getSampleStyleSheet()
footer_style = styles["Normal"]
footer_style.fontSize = 15
footer_style.spaceAfter = 10

# Table Header Style
table_header_style = ParagraphStyle(
    "CellStyle",
    parent=getSampleStyleSheet()["Normal"],
    fontName="Helvetica-Bold",
    fontSize=11,
    textColor=colors.white,
    alignment=1,  # 0=Left, 1=Center, 2=Right
)

# Cell Style
table_cell_Style = ParagraphStyle(
    "CellStyle",
    parent=getSampleStyleSheet()["Normal"],
    fontName="Helvetica",
    fontSize=10,
    textColor=colors.black,
    alignment=1,  # 0=Left, 1=Center, 2=Right
)

elements = []


def line_chart(data):

    footer_style.textColor = black
    label = Paragraph("------ Outflow", footer_style)
    elements.append(label)

    footer_style.textColor = darkcyan
    label = Paragraph("------ Inflow", footer_style)
    elements.append(label)

    dr_values = [month_data["DR"] for month_data in data[0].values()]
    cr_values = [month_data["CR"] for month_data in data[0].values()]
    values = [dr_values, cr_values]

    # labels = [[str(value) for value in row] for row in values]

    min_value = min(dr_values) if min(dr_values) < min(cr_values) else min(cr_values)
    max_value = max(dr_values) if max(dr_values) > max(cr_values) else max(cr_values)

    drawing = Drawing(400, 200)

    lc = HorizontalLineChart()
    lc.x = 50
    lc.y = -70
    lc.height = 200
    lc.width = 400
    lc.data = values
    lc.joinedLines = 1
    lc.fillColor = colors.HexColor("#a69ff9")
    lc.categoryAxis.categoryNames = data[1]
    lc.categoryAxis.labels.boxAnchor = "n"
    lc.valueAxis.valueMin = min_value
    lc.valueAxis.valueMax = max_value + 100
    lc.lines[0].strokeColor = black
    lc.lines[1].strokeColor = darkcyan
    lc.lines[0].strokeWidth = 2
    lc.lines[1].strokeWidth = 1.5

    # lc.lineLabelArray = labels
    # lc.lineLabelFormat = 'values'
    drawing.add(lc)

    return drawing


# Create a pie chart


def create_pie_chart(data, total_income, total_outcome, labels):
    if len(data) > 1:
        # Calculate total for percentage calculation
        # total = sum(data[1:])
        total = total_income if data[0] == "Debit" else total_outcome

        # print(data[:5])
        data = sorted(data[1:], reverse=True)[:5]
        data.append(total - sum(data))

        # Calculate percentages
        # percentages = [value / total * 100 for value in data if value > 0]

        # Create a drawing
        drawing = Drawing(width=200, height=200)

        # Create a pie chart
        pie_chart = Pie()
        pie_chart.x = 125
        pie_chart.y = -35
        pie_chart.width = 200
        pie_chart.height = 200
        pie_chart.data = data
        pie_chart.labels = [d[0] for d in labels]
        pie_chart.sideLabels = 1
        pie_chart.sideLabelsOffset = 0.2
        pie_chart.strokeWidth = 2
        pie_chart.checkLabelOverlap = 1
        pie_chart.pointerLabelMode = "LeftAndRight"
        # 'LeftAndRight'

        # Add the pie chart to the drawing
        drawing.add(pie_chart)

    return drawing


def create_pdf(
    data,
    govt_list,
    table_headings,
    chart_data,
    total_income,
    total_outcome,
    line_chart_data,
    current_lang,
    outflow_labels,
    inflow_labels,
):
    space_added = False
    total_len = 12
    remain_len = 0
    table_len = 0

    # print(total_income, total_outcome)

    pdf_path = sys.path[0] + "/table.pdf"
    pdf = SimpleDocTemplate(pdf_path, pagesize=letter)
    heading_index = 0

    # font_path = sys.path[0] + "/fonts/" + str(current_lang) + ".ttf"
    # pdfmetrics.registerFont(TTFont('TamilFont', font_path))
    # tamil_font = "TamilFont"
    for d in data:

        heading_text = table_headings[heading_index].upper()
        heading = Paragraph(heading_text, header_style)

        if heading_text == "HIGH VALUE TRANSACTIONS":
            prim_heading = (
                "HIGH VALUE TRANSACTIONS, UNUSUAL TRANSACTIONS, DUPLICATE TRANSACTIONS"
            )
            styled_prim_heading = Paragraph(prim_heading, header_style)
            elements.append(styled_prim_heading)

        if (
            heading_text == "HIGH VALUE TRANSACTIONS"
            or heading_text == "UNUSUAL TRANSACTIONS"
            or heading_text == "DUPLICATE TRANSACTIONS"
        ):
            heading = Paragraph(heading_text, getSampleStyleSheet()["Heading1"])

        elements.append(heading)

        table_data = []
        table_data.append([Paragraph(cell, table_header_style) for cell in d[0]])

        for row in d[1:]:
            table_data.append([Paragraph(str(cell), table_cell_Style) for cell in row])

        # Define a custom style
        if table_headings[heading_index] == "UPI - MODE OF PAYMENT\n(STATUS COUNT)":
            style = TableStyle(
                [
                    # ('FONT', (0, 0), (-1, 0), tamil_font),
                    # Header background color
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#C79FE4")),
                    # Header background color
                    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#C79FE4")),
                    ("TOPPADDING", (0, 0), (-1, -1), 12),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (1, 1), (-1, -1), colors.white),
                    ("GRID", (0, 0), (-1, -1), 1, colors.gray),
                ]
            )

        else:
            style = TableStyle(
                [
                    # ('FONT', (0, 0), (-1, 0), tamil_font),
                    # Header background color
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#C79FE4")),
                    ("TOPPADDING", (0, 0), (-1, -1), 12),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                    ("GRID", (0, 0), (-1, -1), 1, colors.gray),
                ]
            )

        col_width = []
        if table_headings[heading_index] == "Bank Charges Analysis":
            col_width = ["15%", "35%", "15%", "35%"]
        elif table_headings[heading_index] == "UPI - MODE OF PAYMENT\n(STATUS COUNT)":
            col_width = ["16%", "28%", "28%", "28%"]
        elif (
            table_headings[heading_index] == "High Value Transactions"
            or table_headings[heading_index] == "Unusual Transactions"
            or table_headings[heading_index] == "Duplicate Transactions"
        ):
            col_width = ["15%", "45%", "20%", "20%"]
        elif table_headings[heading_index] == "Attribute Classification":
            col_width = ["50%", "25%", "25%"]

        table = Table(table_data, colWidths=col_width, style=style)
        elements.append(table)
        table_len = table_len + len(table_data)

        if table_len == total_len:
            space_added = True
            table_len = 0
            elements.append(PageBreak())

        elif remain_len == 0:
            remain_len = total_len - len(table_data)
            space_added = False
            elements.append(Spacer(1, 50))

        else:
            if len(table_data) > remain_len:
                space_added = True
                elements.append(PageBreak())
            else:
                space_added = False
                elements.append(Spacer(1, 50))

        # if (len(table_data) >= 4 and loop != len(data)) or (loop == len(data) and len(table_data) >= 6):
        #     space_added = True
        #     elements.append(PageBreak())

        # else:
        #     space_added = False
        #     if loop != len(data):
        #         elements.append(Spacer(1, 50))

        # loop = loop + 1

        heading_index = heading_index + 1

    if not space_added:
        elements.append(PageBreak())

    heading_text = "Chart Analysis"
    heading = Paragraph(heading_text, getSampleStyleSheet()["Heading1"])
    elements.append(heading)

    # Pie Chart
    for ch in chart_data:
        # print(ch)

        label = inflow_labels if ch[0] == "Credit" else outflow_labels
        heading_text = (
            "> Overall Cash Inflow" if ch[0] == "Credit" else "> Overall Cash Outflow"
        )
        heading = Paragraph(heading_text, getSampleStyleSheet()["Title"])
        elements.append(heading)

        elements.append(
            create_pie_chart(ch, total_income[0], total_outcome[0], labels=label)
        )
        # elements.append(PageBreak())
        elements.append(Spacer(1, 80))

    heading_text = "Monthly Analytics"
    heading = Paragraph(heading_text, getSampleStyleSheet()["Heading1"])
    elements.append(heading)

    # Line Chart
    line_ch = line_chart(line_chart_data)
    elements.append(line_ch)
    elements.append(PageBreak())

    # GOVT TDS LISTS
    heading_text = "RECEIPT OF GOVERNMENT GRANT & LIST OF TDS"
    heading = Paragraph(heading_text, header_style)
    elements.append(heading)

    for d in govt_list:
        heading_text = table_headings[heading_index].upper()
        heading = Paragraph(heading_text, getSampleStyleSheet()["Heading1"])

        if heading_text == "DEDUCTION":
            prim_heading = "FINDER REGARDING TAXATION LAW"
            styled_prim_heading = Paragraph(prim_heading, header_style)
            elements.append(styled_prim_heading)

        if heading_text == "EMI":
            prim_heading = "LIST OF SPECIAL TRANSACTIONS"
            styled_prim_heading = Paragraph(prim_heading, header_style)
            elements.append(styled_prim_heading)

        elements.append(heading)

        table_data = []
        table_data.append([Paragraph(cell, table_header_style) for cell in d[0]])

        for row in d[1:]:
            table_data.append([Paragraph(str(cell), table_cell_Style) for cell in row])

            style = TableStyle(
                [
                    # ('FONT', (0, 0), (-1, 0), tamil_font),
                    # Header background color
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#C79FE4")),
                    ("TOPPADDING", (0, 0), (-1, -1), 12),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                    ("GRID", (0, 0), (-1, -1), 1, colors.gray),
                ]
            )

        col_width = []
        if table_headings[heading_index] == "Interest credited and debited":
            col_width = ["20%", "40%", "20%", "20%"]
        else:
            col_width = ["20%", "60%", "20%"]

        table = Table(table_data, colWidths=col_width, style=style)
        elements.append(table)
        elements.append(Spacer(1, 50))

        heading_index = heading_index + 1

    # random
    heading_text = "RANDOM VERIFICATION"
    heading = Paragraph(heading_text, header_style)
    elements.append(heading)

    heading_text = "Closure"
    heading = Paragraph(heading_text, getSampleStyleSheet()["Heading1"])
    elements.append(heading)

    closure_table = [
        ["Particular", "Debit", "Credit"],
        ["Amount", "{:.2f}".format(total_outcome[0]), "{:.2f}".format(total_income[0])],
        [
            "Transactions",
            "{:.2f}".format(total_outcome[1]),
            "{:.2f}".format(total_income[1]),
        ],
    ]

    table_data = []
    table_data.append(
        [Paragraph(cell, table_header_style) for cell in closure_table[0]]
    )

    table_data.append(
        [Paragraph(str(cell), table_cell_Style) for cell in closure_table[1]]
    )

    table_data.append(
        [Paragraph(str(cell), table_cell_Style) for cell in closure_table[2]]
    )

    style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#C79FE4")),
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#C79FE4")),
            ("TOPPADDING", (0, 0), (-1, -1), 12),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (1, 1), (-1, -1), colors.white),
            ("GRID", (0, 0), (-1, -1), 1, colors.gray),
        ]
    )

    col_width = ["40%", "30%", "30%"]
    table = Table(table_data, colWidths=col_width, style=style)
    elements.append(table)
    elements.append(Spacer(1, 50))

    # Function to add page numbers
    def add_page_number(canvas, doc):
        page_num = canvas.getPageNumber()
        text = "macrotouch.in ________________________________________________ %d" % (
            page_num + 1
        )
        canvas.drawString(130, 50, text)

    # Build the PDF
    pdf.build(elements, onFirstPage=add_page_number, onLaterPages=add_page_number)

    # return output_file
    return pdf_path
