import pdfplumber
from collections import defaultdict
from functions.regex_functions import is_date

# Define header synonyms
HEADER_KEYWORDS = {
    "date": ["date", "txn", "txn date", "txndate", "transaction date", "transactiondate"],
    "description": ["details of transaction", "transaction details", "particulars", "description", "narration", "transaction reference"],
    "debit": {
        "debit", "debits", "withdrawal", "withdrawal amt", "withdrawalamt", "withdrawals", "withdrawl",
        "dr", "debit amount", "debitamount", "withdrawalamt.",
    },
    "credit": { "credit", "credits", "deposit amt" , "deposit", "deposits", "depositamt",
                "cr", "credit amount", "creditamount", "depositamt."
    },
    "amount": {"amount", "amt", "trxn amount", "trxnamount"},
    "type": {"type", "txn type", "txntype", "dr/cr", "cr/dr", "transaction type"},
    "closing_balance": {"balance", "balance(inr)", "closingbalance", "closing balance", "bal"},
    "value date": {"Value Dt", "value", "ValueDt", "value date"},
    "ref. no.": {"chq.no.", "ref.no.", "ref. no.", "ref.No./chq.No.", "chq. / ref. No", "Chq./Ref.No."},
}

# Normalize text function
def normalize(text):
    return text.lower().strip().replace('.', '')


def is_broken_line(columns):
    return (
        not columns["date"]
        and columns["description"]
        and not columns["debit"]
        and not columns["credit"]
        and not columns["closing_balance"]
    )

def find_header_positions(headers: dict, page_width: int):
    sorted_headers = sorted(headers.items(), key=lambda item: item[1]['x0'])
    positions = {}
    
    start = 0
    for i, (col_name, pos) in enumerate(sorted_headers):
        end = page_width
        if i < len(sorted_headers) - 1:
            end = sorted_headers[i + 1][1]['x0']
            
        positions[col_name] = [start, end]
        start = pos['x1']
    
    return positions

# Function to find headers and their x0
def find_headers(pdf_path):
    page_num = 0
    header_positions = {}
    page_width = 0
    
    with pdfplumber.open(pdf_path) as pdf:
        while page_num < len(pdf.pages):
            curr_page = pdf.pages[page_num]
            page_width = curr_page.width
            words = curr_page.extract_words(
                            x_tolerance=0.5, 
                            y_tolerance=3, 
                            use_text_flow=True, 
                            keep_blank_chars=True
                        )

            for word in words:
                norm_word = normalize(word['text'])
                for header, aliases in HEADER_KEYWORDS.items():
                    aliases = [a.lower().strip().replace('.','') for a in aliases]
                    if norm_word in aliases and header not in header_positions:
                        header_positions[header] = {
                            'x0': word['x0'],
                            'x1': word['x1']
                        }
            
            if len(header_positions) > 0:
                break

            page_num = page_num + 1

    print("Header found on page num: ", page_num)
    return find_header_positions(header_positions, page_width)


def extract_bank_entries(pdf_path):
    print("Final extraction started")
    header_positions = find_headers(pdf_path)
    
    if len(header_positions.items()) == 0:
        return []

    def classify_column(x0, x1):
        for col_name, pos in header_positions.items():
            if x0 >= pos[0] and x1 <= pos[1]:
                return col_name
        return None

    all_entries = []
    last_entry = None

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            words = page.extract_words(
                        x_tolerance=0.5, 
                        y_tolerance=3, 
                        use_text_flow=True, 
                        keep_blank_chars=True
                    )

            # Step 1: group words by row (by 'top')
            rows = defaultdict(list)
            for word in words:
                top_key = round(word['top'] / 3) * 3  # cluster nearby rows
                rows[top_key].append(word)

            for top, row_words in sorted(rows.items()):
                columns = {
                    "date": "", "description": "",
                    "debit": "", "credit": "",
                    "amount": "", "type": "",
                    "closing_balance": ""
                }

                # Classifying rows
                for word in row_words:
                    col = classify_column(word["x0"], word["x1"])
                    if col and col in columns.keys():
                        columns[col] += word["text"] + " "

                # Clean up and strip extra spaces
                for key in columns:
                    columns[key] = columns[key].strip()

                if is_broken_line(columns) and last_entry:
                    # Merge broken description
                    last_entry["description"] += " " + columns["description"]
                    continue

                # Skip empty or header rows
                if not columns["date"] or columns["date"].lower().startswith("date"):
                    continue

                # Determine transaction type
                if columns["credit"] and (columns['debit'].strip() == '-' or not columns["debit"]):
                    trans_type = "credit"
                    amount = columns["credit"]
                elif columns["debit"] and (columns['credit'].strip() == '-' or not columns["credit"]):
                    trans_type = "debit"
                    amount = columns["debit"]
                elif columns["amount"] and columns["type"]:
                    trans_type = columns["type"].lower()
                    if "cr" in trans_type or "credit" in trans_type:
                        trans_type = "credit"
                    elif "dr" in trans_type or "debit" in trans_type:
                        trans_type = "debit"
                    else:
                        trans_type = "unknown"
                    amount = columns["amount"]
                else:
                    trans_type = "unknown"
                    amount = ""

                # Valid entry
                if is_date(columns["date"]):
                    entry = {
                        "date": columns["date"],
                        "description": columns["description"],
                        "amount": amount,
                        "type": trans_type,
                        "closing_balance": columns["closing_balance"]
                    }
                    # print(entry, flush=True)
                    all_entries.append(entry)
                    last_entry = entry

    return all_entries
