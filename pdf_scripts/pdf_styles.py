from reportlab.platypus import TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

fonts = {
    0: "Helvetica",  # English
    1: "Hindi",  # Hindi
    2: "Tamil",  # Tamil
    3: "Noto-Telugu",  # Hindi
    4: "Malayalam",  # Malayalam
    5: "Noto-Kannada",  # Telugu
}

# Table Header Style
table_header_style = ParagraphStyle(
    "HeaderStyle",
    parent=getSampleStyleSheet()["Heading1"],
    fontSize=11,
    textColor=colors.white,
    alignment=1,  # 0=Left, 1=Center, 2=Right
)

# Cell Style
table_cell_Style = ParagraphStyle(
    "CellStyle",
    parent=getSampleStyleSheet()["Normal"],
    fontSize=10,
    textColor=colors.black,
    alignment=1,  # 0=Left, 1=Center, 2=Right
)

# Table Style
table_style = TableStyle(
    [
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#C79FE4")),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ("BACKGROUND", (0, 1), (-1, -1), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.gray),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]
)


UPI_table_style = TableStyle(
    [
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#C79FE4")),
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#C79FE4")),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ("BACKGROUND", (1, 1), (-1, -1), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.gray),
    ]
)


closure_table_style = TableStyle(
    [
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#C79FE4")),
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#C79FE4")),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ("BACKGROUND", (1, 1), (-1, -1), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.gray),
    ]
)

# Heading1 Style
def header1_style(font:str): 
    return ParagraphStyle(
        "Header1Style",
        parent = getSampleStyleSheet()["Heading1"],
        fontName=font,
        fontSize=25,
        spaceAfter=15,
        textColor=colors.HexColor("#743BC2"),
        alignment=0,  # 0=Left, 1=Center, 2=Right
    )
    
# Heading2 Style
def header2_style(font:str): 
    return ParagraphStyle(
        "Header2Style",
        fontName=font,
        parent = getSampleStyleSheet()["Heading1"],
        textColor=colors.black,
        alignment=0,  # 0=Left, 1=Center, 2=Right
    )

def side_head_style1(font:str):
    return ParagraphStyle(
        "SideHeading1",
        fontName=font,
        parent=getSampleStyleSheet()["Normal"],
        fontSize=15,
        spaceAfter=10,
        textColor=colors.black,
        alignment=0
    )

def side_head_style2(font:str):
    return ParagraphStyle(
        "SideHeading1",
        fontName=font,
        parent=getSampleStyleSheet()["Normal"],
        fontSize=15,
        spaceAfter=10,
        textColor=colors.darkcyan,
        alignment=0
    )

COL_WIDTH = {
    # 'CHG': ["15%", "30%", "15%", "10%", "30%"],
    "CHG": ["15%", "45%", "20%", "20%"],
    "MOP": ["16%", "28%", "28%", "28%"],
    "HVT": ["15%", "45%", "20%", "20%"],
    "UNT": ["15%", "45%", "20%", "20%"],
    "DUP": ["15%", "45%", "20%", "20%"],
    "ATTR": ["50%", "25%", "25%"],
    "TDS": ["20%", "60%", "20%"],
    "GRANT": ["20%", "60%", "20%"],
    "DEDUCTION": ["20%", "40%", "20%", "20%"],
    "REFUND": ["20%", "60%", "20%"],
    "ADVTAX": ["20%", "60%", "20%"],
    "EMI": ["20%", "60%", "20%"],
    "CLOSURE": ["20%", "60%", "20%"],
    "INTEREST": ["20%", "40%", "20%", "20%"],
    "CLS": ["33.3%", "33.3%", "33.3%"],
}

HEADINGS = {
    "HVT": {
        "texts": [
            "HIGH VALUE TRANSACTIONS,\nUNUSUAL TRANSACTIONS,\nDUPLICATE TRANSACTIONS",  # English
            "उच्च मूल्य लेनदेन,\nअसामान्य लेनदेन,\nडुप्लिकेट लेनदेन",  # Hindi
            "உயர் மதிப்பு பரிவர்த்தனைகள்,\nஅசாதாரண பரிவர்த்தனைகள்,\nநகல் பரிவர்த்தனைகள்",  # Tamil
            "అధిక విలువ లావాదేవీలు,\nఅసాధారణ లావాదేవీలు,\nనకిలీ లావాదేవీలు",  # Telugu
            "ഉയർന്ന മൂല്യത്തിലുള്ള ഇടപാടുകൾ,\nഅസാധാരണ ഇടപാടുകൾ,\nആവർത്തിച്ച ഇടപാടുകൾ",  # Malayalam
            "ಉನ್ನತ ಮೌಲ್ಯದ ವ್ಯವಹಾರಗಳು,\nಅಸಾಮಾನ್ಯ ವ್ಯವಹಾರಗಳು,\nಪ್ರತಿಲಿಪಿ ವ್ಯವಹಾರಗಳು",  # Kannada
        ],
        "style": header1_style,
    },
    "PRIMARY_GOV": {
        "texts": [
            "RECEIPT OF GOVERNMENT GRANT & LIST OF TDS",  # English
            "सरकारी अनुदान की रसीद और टीडीएस की सूची",  # Hindi
            "அரசு நன்கொடை ரசீதும் மற்றும் TDS பட்டியலும்",  # Tamil
            "ప్రభుత్వ గ్రాంట్ స్వీకారం & TDS జాబితా",  # Telugu
            "സർക്കാർ ധനസഹായം ലഭിക്കൽ & TDS ലിസ്റ്റ്",  # Malayalam
            "ಸರ್ಕಾರಿ ಅನುದಾನದ ಸ್ವೀಕೃತಿ ಮತ್ತು TDS ಪಟ್ಟಿ",  # Kannada
        ],
        "style": header1_style,
    },
    "PIE_CHART": {
        "texts": [
            "CHART ANALYSIS",  # English
            "चार्ट विश्लेषण",  # Hindi
            "வழிகாட்டி பகுப்பாய்வு",  # Tamil
            "చార్ట్ విశ్లేషణ",  # Telugu
            "ചാർട്ട് വിശകലനം",  # Malayalam
            "ಚಾರ್ಟ್ ವಿಶ್ಲೇಷಣೆ",  # Kannada
        ],
        "style": header1_style,
    },
    "PIE_LINE_HEADING": [
        {"texts": ["Monthly Analysis", "मासिक विश्लेषण", "மாதாந்திர பகுப்பாய்வு", "నెలవారీ విశ్లేషణ", "മാസാന്ത്യ വിശകലനം", "ಮಾಸಿಕ ವಿಶ್ಲೇಷಣೆ"], "style":header2_style},
        {"texts": ["-- OUTFLOW", "-- आउटफ्लो", "-- வெளியேற்றம்", "-- అవుట్‌ఫ్లో", "-- ഔട്ട്‌ഫ്ലോ", "-- ಔಟ್‌ಫ್ಲೋ"], "style": side_head_style1},
        {"texts": ["-- INFLOW", "-- इनफ्लो", "-- உள்ளேற்றம்", "-- ఇన్‌ఫ్లో", "-- ഇൻഫ്ലോ", "-- ಇನ್‌ಫ್ಲೋ"], "style": side_head_style2},
    ],
    "RANDOM": {
        "texts": [
            "RANDOM VERIFICATION",  # English
            "यादृच्छिक सत्यापन",  # Hindi
            "சீரற்ற சரிபார்ப்பு",  # Tamil
            "యాదృచ్ఛిక ధృవీకరణ",  # Telugu
            "യാദൃച്ഛിക സ്ഥിരീകരണം",  # Malayalam
            "ಯಾದೃಚ್ಛಿಕ ಪರಿಶೀಲನೆ",  # Kannada
        ],
        "style": header1_style,
    },
    "CLOSURE": {
        "texts": [
            "CLOSURE",  # English
            "समापन",  # Hindi
            "மூடல்",  # Tamil
            "మూసివేత",  # Telugu
            "നടവിലാക്കൽ",  # Malayalam
            "ಮುಚ್ಚುವಿಕೆ",  # Kannada
        ],
        "style": header2_style,
    },
    "RB": {
        "texts": [
            "RUNNING BALANCE CHECK",  # English
            u"चल रहा शेष जांच",  # Hindi
            u"இயங்கும் இருப்பு சரிபார்ப்பு",  # Tamil
            u"రన్నింగ్ బ్యాలెన్స్ చెక్",  # Telugu
            u"റണ്ണിംഗ് ബാലൻസ് പരിശോധിക്കുക",  # Malayalam
            u"ರನ್ನಿಂಗ್ ಬ್ಯಾಲೆನ್ಸ್ ಚೆಕ್",  # Kannada
        ],
        "style": header2_style,
    },
    "DR": {
        "texts": [
        "Overall Cash Outflow",  # English
        u"कुल नकदी बहिर्वाह",  # Hindi
        u"மொத்த ரொக்க வெளியேற்றம்",  # Tamil
        u"మొత్తం నగదు అవుట్‌ఫ్లో",  # Telugu
        u"മൊത്തത്തിലുള്ള ക്യാഷ് ഔട്ട്‌ഫ്ലോ",  # Malayalam
        u"ಒಟ್ಟು ನಗದು ಔಟ್‌ಫ್ಲೋ",  # Kannada
    ],
    "style": header2_style,
    },
    "CR": {
        "texts": [
            "Overall Cash Inflow",  # English
            u"कुल नकदी प्रवाह",  # Hindi
            u"மொத்த ரொக்க உள்ளேற்றம்",  # Tamil
            u"మొత్తం నగదు ఇన్‌ఫ్లో",  # Telugu
            u"മൊത്തത്തിലുള്ള ക്യാഷ് ഇൻഫ്ലോ",  # Malayalam
            u"ಒಟ್ಟು ನಗದು ಇನ್‌ಫ್ಲೋ",  # Kannada
        ],
        "style": header2_style,
    },
}


TABLE_TITLES = {
    "CHG": [
        "BANK CHARGES ANALYSIS",  # English
        u"बैंक शुल्क विश्लेषण",  # Hindi
        u"வங்கி கட்டணங்கள் பகுப்பாய்வு",  # Tamil
        u"బ్యాంక్ ఛార్జెస్ విశ్లేషణ",  # Telugu
        u"ബാങ്ക് ചാർജുകൾ വിശകലനം",  # Malayalam
        u"ಬ್ಯಾಂಕ್ ಶುಲ್ಕಗಳ ವಿಶ್ಲೇಷಣೆ",  # Kannada
    ],
    "MOP": [
        "UPI - MODE OF PAYMENT\n(STATUS COUNT)",  # English
        u"यूपीआई - भुगतान का तरीका\n(स्थिति गणना)",  # Hindi
        u"யுபிஐ - கட்டண முறை\n(நிலை எண்ணிக்கை)",  # Tamil
        u"యూపీఐ - చెల్లింపు మోడ్\n(స్థితి సంఖ్య)",  # Telugu
        u"യുപിഐ - പേയ്മെന്റ് മോഡ്\n(സ്റ്റാറ്റസ് കൗണ്ട്)",  # Malayalam
        u"ಯುಪಿಐ - ಪಾವತಿ ವಿಧಾನ\n(ಸ್ಥಿತಿ ಎಣಿಕೆ)",  # Kannada
    ],
    "HVT": [
        "HIGH VALUE TRANSACTIONS",  # English
        u"उच्च मूल्य लेनदेन",  # Hindi
        u"உயர் மதிப்பு பரிவர்த்தனைகள்",  # Tamil
        u"అధిక విలువ లావాదేవీలు",  # Telugu
        u"ഉയർന്ന മൂല്യത്തിലുള്ള ഇടപാടുകൾ",  # Malayalam
        u"ಉನ್ನತ ಮೌಲ್ಯದ ವ್ಯವಹಾರಗಳು",  # Kannada
    ],
    "UNT": [
        "UNUSUAL TRANSACTIONS",  # English
        u"असामान्य लेनदेन",  # Hindi
        u"அசாதாரண பரிவர்த்தனைகள்",  # Tamil
        u"అసాధారణ లావాదేవీలు",  # Telugu
        u"അസാധാരണ ഇടപാടുകൾ",  # Malayalam
        u"ಅಸಾಮಾನ್ಯ ವ್ಯವಹಾರಗಳು",  # Kannada
    ],
    "DUP": [
        "DUPLICATE TRANSACTIONS",  # English
        u"डुप्लिकेट लेनदेन",  # Hindi
        u"நகல் பரிவர்த்தனைகள்",  # Tamil
        u"నకిలీ లావాదేవీలు",  # Telugu
        u"ആവർത്തിച്ച ഇടപാടുകൾ",  # Malayalam
        u"ಪ್ರತಿಲಿಪಿ ವ್ಯವಹಾರಗಳು",  # Kannada
    ],
    "ATTR": [
        "ATTRIBUTE CLASSIFICATION",  # English
        "गुणवत्ता वर्गीकरण",  # Hindi
        "பண்புக்கூறுகளின் வகைப்படுத்தல்",  # Tamil
        "లక్షణాల వర్గీకరణ",  # Telugu
        "ഗുണവിശേഷത്തിന്റെ വിഭാഗീകരണം",  # Malayalam
        "ಗುಣಲಕ್ಷಣ ವರ್ಗೀಕರಣ",  # Kannada
    ],
    "TDS": [
        "LIST OF TDS DEDUCTED",  # English
        "कटौती किए गए टीडीएस की सूची",  # Hindi
        "கழிக்கப்பட்ட TDS பட்டியல்",  # Tamil
        "తగ్గించిన TDS జాబితా",  # Telugu
        "കുറച്ചെടുത്ത TDS ലിസ്റ്റ്",  # Malayalam
        "ಕಡಿತಗೊಂಡ TDS ಪಟ್ಟಿ",  # Kannada
    ],
    "GRANT": [
        "RECEIPT OF GOVERNMENT GRANT",  # English
        "सरकारी अनुदान की रसीद",  # Hindi
        "அரசு நன்கொடை ரசீது",  # Tamil
        "ప్రభుత్వ గ్రాంట్ స్వీకారం",  # Telugu
        "സർക്കാർ ധനസഹായം കിട്ടൽ",  # Malayalam
        "ಸರ್ಕಾರಿ ಅನುದಾನದ ಸ್ವೀಕೃತಿ",  # Kannada
    ],
    "DEDUCTION": [
        "DEDUCTION",  # English
        "कटौती",  # Hindi
        "கழிப்பு",  # Tamil
        "తగ్గింపు",  # Telugu
        "കുറവ്",  # Malayalam
        "ಕಡಿತ",  # Kannada
    ],
    "REFUND": [
        "TAX REFUND",  # English
        "कर वापसी",  # Hindi
        "வரி மீட்பு",  # Tamil
        "పన్ను రిఫండ్",  # Telugu
        "നികുതി തിരിച്ചടവ്",  # Malayalam
        "ತೆರಿಗೆ ಮರುಪಾವತಿ",  # Kannada
    ],
    "ADVTAX": [
        "ADVANCE TAX",  # English
        "अग्रिम कर",  # Hindi
        "முன்கூட்டிய வரி",  # Tamil
        "ముందస్తు పన్ను",  # Telugu
        "മുൻകൂർ നികുതി",  # Malayalam
        "ಮುಂಗಡ ತೆರಿಗೆ",  # Kannada
    ],
    "EMI": [
        "EMI",  # English
        "ईएमआई",  # Hindi
        "EMI",  # Tamil
        "EMI",  # Telugu
        "EMI",  # Malayalam
        "EMI",  # Kannada
    ],
    "CLOSURE": [
        "CLOSURE",  # English
        "समापन",  # Hindi
        "மூடல்",  # Tamil
        "మూసివేత",  # Telugu
        "നടവിലാക്കൽ",  # Malayalam
        "ಮುಚ್ಚುವಿಕೆ",  # Kannada
    ],
    "INTEREST": [
        "INTEREST CREDITED AND DEBITED",  # English
        "सूद जमा और डेबिट किया गया",  # Hindi
        "பட்டுவாடா செய்யப்பட்ட மற்றும் கடன் பட்டுவாடா",  # Tamil
        "క్రెడిట్ మరియు డెబిట్ చేసిన వడ్డీ",  # Telugu
        "കയറ്റവും ക്രെഡിറ്റും",  # Malayalam
        "ಹೂಡಿಕೆ ಕ್ರೆಡಿಟ್ ಮತ್ತು ಡೆಬಿಟ್",  # Kannada
    ],
}

def get_table_title(key, lang_index):
    
    # Fetch the title text and style
    title_list = TABLE_TITLES.get(key)

    if not title_list:
        raise ValueError(f"No title found for key: {key}")
    
    if not (0 <= lang_index < len(title_list)):
        lang_index = 0
    
    title_text = title_list[lang_index]
    print(title_text)

    font_name = fonts.get(lang_index)
    print(font_name)

    style =  header2_style(font_name)

    if key == "CHG" or key == "MOP" or key == "ATTR":
        style = header1_style(font_name)
    
    # Return the Paragraph
    return Paragraph(title_text, style)

def get_heading(key, lang_index):

    font_name = fonts.get(lang_index)
    print(font_name)

    if key in HEADINGS:
        heading_data = HEADINGS[key]
    
        if not heading_data:
            raise ValueError(f"No heading found for key: {key}")


        if isinstance(heading_data, list):  # Handle grouped headings like PIE_LINE
            return [
                Paragraph(item["texts"][lang_index], item["style"](font_name)) for item in heading_data
            ]

        return Paragraph(heading_data["texts"][lang_index], heading_data["style"](font_name))

    raise ValueError(f"No heading found for key: {key}")