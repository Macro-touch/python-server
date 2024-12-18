from reportlab.platypus import TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# Table Header Style
table_header_style = ParagraphStyle(
    'HeaderStyle',
    parent=getSampleStyleSheet()['Heading1'],
    fontName='Helvetica-Bold',
    fontSize=11,
    textColor=colors.white,
    alignment=1  # 0=Left, 1=Center, 2=Right
)

# Cell Style
table_cell_Style = ParagraphStyle(
    'CellStyle',
    parent=getSampleStyleSheet()['Normal'],
    fontName='Helvetica',
    fontSize=10,
    textColor=colors.black,
    alignment=1  # 0=Left, 1=Center, 2=Right
)

# Table Style
table_style= TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#C79FE4')),
    ('TOPPADDING', (0, 0), (-1, -1), 12),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
    ('GRID', (0, 0), (-1, -1), 1, colors.gray),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
])


UPI_table_style = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#C79FE4')),
    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#C79FE4')),
    ('TOPPADDING', (0, 0), (-1, -1), 12),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (1, 1), (-1, -1), colors.white),
    ('GRID', (0, 0), (-1, -1), 1, colors.gray)
])


closure_table_style = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#C79FE4')),
    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#C79FE4')),
    ('TOPPADDING', (0, 0), (-1, -1), 12),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (1, 1), (-1, -1), colors.white),
    ('GRID', (0, 0), (-1, -1), 1, colors.gray)
])

# Heading Style
styles = getSampleStyleSheet()
header_style = styles["Heading1"]
header_style.fontSize = 25
header_style.spaceAfter = 15
header_style.fontWeight = 'Bold'
header_style.textColor = colors.HexColor('#743BC2')

# Side Heading 1
side_head_style1 = getSampleStyleSheet()
side_heading1 = side_head_style1["Normal"]
side_heading1.fontSize = 15
side_heading1.spaceAfter = 10
side_heading1.textColor = colors.black

# Side Heading 2
side_head_style2 = getSampleStyleSheet()
side_heading2 = side_head_style2["Normal"]
side_heading2.fontSize = 15
side_heading2.spaceAfter = 10
side_heading2.textColor = colors.darkcyan



COL_WIDTH = {
    'CHG': ["15%", "30%", "15%", "10%", "30%"],
    'MOP': ["16%", "28%", "28%", "28%"],
    'HVT': ["15%", "45%", "20%", "20%"],
    'UNT': ["15%", "45%", "20%", "20%"],
    'DUP': ["15%", "45%", "20%", "20%"],
    'ATTR': ["50%", "25%", "25%"],
    'TDS': ["20%", "60%", "20%"],
    'GRANT': ["20%", "60%", "20%"],
    'DEDUCTION': ["20%", "40%", "20%", "20%"],
    'REFUND': ["20%", "60%", "20%"],
    'ADVTAX': ["20%", "60%", "20%"],
    'EMI': ["20%", "60%", "20%"],
    'CLOSURE': ["20%", "60%", "20%"],
    'INTEREST': ["20%", "40%", "20%", "20%"],
    'CLS': ['33.3%', '33.3%', '33.3%']
}

PRIMARY_HVT_HEADING = Paragraph(
    'HIGH VALUE TRANSACTIONS, UNUSUAL TRANSACTIONS, DUPLICATE TRANSACTIONS', 
    header_style
)

PRIMARY_GOV_HEADING = Paragraph(
    'RECEIPT OF GOVERNMENT GRANT & LIST OF TDS', 
    header_style
)


PIE_CHART_HEADING = Paragraph('CHART ANALYSIS', header_style)
PIE_LINE_HEADING = [
     Paragraph('Monthly Analysis', getSampleStyleSheet()['Heading1']),
     Paragraph('-- OUTFLOW', side_heading1),
     Paragraph('-- INFLOW', side_heading2),
]

RANDOM_HEADING = Paragraph('RANDOM VERIFICATION', header_style)
closure_heading = Paragraph("CLOSURE", getSampleStyleSheet()['Heading1'])
rb_heading = Paragraph("RUNNING BALANCE CHECK", getSampleStyleSheet()['Heading1'])


PIE_CHART_TYPE_HEADING = {
    'DR' : Paragraph('Overall Cash Outflow', getSampleStyleSheet()['Heading1']),
    'CR' : Paragraph('Overall Cash Inflow', getSampleStyleSheet()['Heading1']),
}


TABLE_HEADINGS = {
    'CHG': Paragraph('BANK CHARGES ANALYSIS' , header_style),
    'MOP': Paragraph('UPI - MODE OF PAYMENT\n(STATUS COUNT)', header_style),
    'HVT': Paragraph('HIGH VALUE TRANSACTIONS', getSampleStyleSheet()['Heading1']),
    'UNT': Paragraph('UNUSUAL TRANSACTIONS', getSampleStyleSheet()['Heading1']),
    'DUP': Paragraph('DUPLICATE TRANSACTIONS',getSampleStyleSheet()['Heading1']),
    'ATTR': Paragraph('ATTRIBUTE CLASSIFICATION', header_style),
    'TDS': Paragraph('LIST OF TDS DETUCTED', getSampleStyleSheet()['Heading1']),
    'GRANT': Paragraph('RECEPIT OF GOVERNMENT GRANT', getSampleStyleSheet()['Heading1']),
    'DEDUCTION': Paragraph('DEDUCTION', getSampleStyleSheet()['Heading1']),
    'REFUND': Paragraph('TAX REFUND', getSampleStyleSheet()['Heading1']),
    'ADVTAX': Paragraph('ADVANCE TAX', getSampleStyleSheet()['Heading1']),
    'EMI': Paragraph('EMI', getSampleStyleSheet()['Heading1']),
    'CLOSURE': Paragraph('CLOSURE', getSampleStyleSheet()['Heading1']),
    'INTEREST': Paragraph('INTEREST CREDITED AND DEBITED', getSampleStyleSheet()['Heading1']),
}