from reportlab.platypus import Table, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from pdf_styles import (
    table_cell_Style,
    table_header_style,
    table_style,
    TABLE_HEADINGS,
    COL_WIDTH,
    PRIMARY_HVT_HEADING,
    PRIMARY_GOV_HEADING,
    PIE_CHART_HEADING,
    PIE_CHART_TYPE_HEADING,
    PIE_LINE_HEADING,
    closure_heading,
    RANDOM_HEADING,
    UPI_table_style,
    closure_table_style,
)

from functions import format_functions
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.linecharts import HorizontalLineChart
import time


def current_milli_time():
    return round(time.time() * 1000)


class GeneratePDFChunk:

    def __init__(
        self,
        table_set1: list,
        pie_data: list,
        line_data: list,
        table_set2: list,
        closure: list,
    ):
        self.PDF_ELEMENTS = []
        self.set1 = (*table_set1,)
        self.pie_data = (*pie_data,)
        self.line_data = (*line_data,)
        self.set2 = (*table_set2,)
        self.closure = closure

        self.create_first_half()
        self.create_pie_chart()
        self.create_line_chart()
        self.create_second_half()
        self.create_random_verification()

    def get_pdf_data(self):
        return self.PDF_ELEMENTS

    def create_first_half(self):
        # tables will be like :
        # [  Table Type, Table Heading, Table Values ]

        for sec in list(self.set1):
            tables = []
            heading_code = sec[0]
            heading = TABLE_HEADINGS[heading_code]

            # Adding Primary Heading for HVT, UNUSUAL & DUPLICATE
            if heading_code == "HVT":
                self.PDF_ELEMENTS.append(PRIMARY_HVT_HEADING)
            self.PDF_ELEMENTS.append(heading)

            # Adding table heading
            table_header = sec[1]
            tables.append(
                [Paragraph(str(cell), table_header_style) for cell in table_header]
            )

            # Adding empty row if empty
            if len(sec[1:]) == 1:
                tables.append(["-"] * len(sec[1:][0]))

            # Adding table cells
            table_rows = sec[2:]
            for cells in table_rows:
                tables.append(
                    [
                        Paragraph(
                            (format_functions.format_float(str(cell))),
                            (
                                table_header_style
                                if key == 0 and heading_code == "MOP"
                                else table_cell_Style
                            ),
                        )
                        for key, cell in enumerate(cells)
                    ]
                )

            # Creating table
            table = Table(tables, colWidths=COL_WIDTH[heading_code])
            table.setStyle(table_style if heading_code != "MOP" else UPI_table_style)
            self.PDF_ELEMENTS.append(table)

            # Adding Space
            self.PDF_ELEMENTS.append(Spacer(1, 50))

    def create_pie_chart(self):

        self.PDF_ELEMENTS.append(PageBreak())
        self.PDF_ELEMENTS.append(PIE_CHART_HEADING)

        for key, data in enumerate(self.pie_data):
            self.PDF_ELEMENTS.append(PIE_CHART_TYPE_HEADING[data[0]])

            labels = data[1][0]
            data = data[1][1]

            # Create a drawing
            drawing = Drawing(width=200, height=200)

            # Create a pie chart
            pie_chart = Pie()
            pie_chart.x = 125
            pie_chart.y = -35
            pie_chart.width = 200
            pie_chart.height = 200
            pie_chart.data = data
            pie_chart.labels = labels
            pie_chart.sideLabels = 1
            pie_chart.sideLabelsOffset = 0.2
            pie_chart.strokeWidth = 2
            pie_chart.checkLabelOverlap = 1
            pie_chart.pointerLabelMode = "LeftAndRight"

            drawing.add(pie_chart)
            self.PDF_ELEMENTS.append(drawing)
            if key + 1 != len(self.pie_data):
                self.PDF_ELEMENTS.append(Spacer(1, 100))

    def create_line_chart(self):

        self.PDF_ELEMENTS.append(PageBreak())
        self.PDF_ELEMENTS.append(PIE_LINE_HEADING[0])
        self.PDF_ELEMENTS.append(PIE_LINE_HEADING[1])
        self.PDF_ELEMENTS.append(PIE_LINE_HEADING[2])

        drawing = Drawing(400, 200)
        lc = HorizontalLineChart()
        lc.x = 0
        lc.y = -70
        lc.height = 200
        lc.width = 500
        lc.data = self.line_data[0]
        lc.joinedLines = 1
        lc.fillColor = colors.HexColor("#a69ff9")
        lc.categoryAxis.categoryNames = self.line_data[1]
        lc.categoryAxis.labels.boxAnchor = "n"
        lc.lines[0].strokeColor = colors.black
        lc.lines[1].strokeColor = colors.darkcyan
        lc.lines[0].strokeWidth = 2.5
        lc.lines[1].strokeWidth = 1.5
        drawing.add(lc)
        self.PDF_ELEMENTS.append(drawing)
        self.PDF_ELEMENTS.append(PageBreak())

    def create_second_half(self):

        # tables will be like :
        # [  Table Type, Table Heading, Table Values ]

        for sec in list(self.set2):
            tables = []
            heading_code = sec[0]
            heading = TABLE_HEADINGS[heading_code]

            # Adding Primary Heading for HVT, UNUSUAL & DUPLICATE
            if heading_code == "TDS":
                self.PDF_ELEMENTS.append(PRIMARY_GOV_HEADING)
            self.PDF_ELEMENTS.append(heading)

            # Adding table heading
            table_header = sec[1]
            tables.append(
                [Paragraph(str(cell), table_header_style) for cell in table_header]
            )

            # Adding mockup if empty
            if len(sec[1:]) == 1:
                tables.append(["-"] * len(sec[1:][0]))

            # Adding table cells
            table_rows = sec[2:]
            for cells in table_rows:
                tables.append(
                    [
                        Paragraph(
                            (format_functions.format_float(str(cell))), table_cell_Style
                        )
                        for cell in cells
                    ]
                )

            # Creating table
            table = Table(tables, colWidths=COL_WIDTH[sec[0]])
            table.setStyle(table_style)
            self.PDF_ELEMENTS.append(table)

            # Adding Space
            self.PDF_ELEMENTS.append(Spacer(1, 50))

    def create_random_verification(self):

        # closure
        self.PDF_ELEMENTS.append(RANDOM_HEADING)
        self.PDF_ELEMENTS.append(Spacer(1, 10))

        self.PDF_ELEMENTS.append(closure_heading)

        closure_table = []

        # heading
        closure_table.append(
            [Paragraph(str(cell), table_header_style) for cell in self.closure[0]]
        )

        # row - 1
        closure_table.append(
            [
                Paragraph(
                    format_functions.format_float(str(cell)),
                    table_header_style if key == 0 else table_cell_Style,
                )
                for key, cell in enumerate(self.closure[1])
            ]
        )

        # row - 2
        closure_table.append(
            [
                Paragraph(
                    format_functions.format_float(str(cell), count=True),
                    table_header_style if key == 0 else table_cell_Style,
                )
                for key, cell in enumerate(self.closure[2])
            ]
        )

        # Creating table
        table = Table(closure_table, colWidths=COL_WIDTH["CLS"])
        table.setStyle(closure_table_style)
        self.PDF_ELEMENTS.append(table)

        # Running Balance
        # self.PDF_ELEMENTS.append(rb_heading)
