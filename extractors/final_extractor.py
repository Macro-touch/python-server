import pdfplumber
from collections import defaultdict
from functions.regex_functions import is_date

# Define header synonyms
HEADER_KEYWORDS = {
    "date": ["date", "txn date", "txndate", "transaction date", "transactiondate"],
    "description": ["particulars", "description", "narration", "transaction reference"],
    "debit": {
        "debit", "debits", "withdrawal", "withdrawal amt", "withdrawalamt", "withdrawals", "withdrawl",
        "dr", "debit amount", "debitamount", "withdrawalamt.",
    },
    "credit": { "credit", "credits", "deposit amt" , "deposit", "deposits", "depositamt",
                "cr", "credit amount", "creditamount", "depositamt."
    },
    "closing_balance": {"balance", "closingbalance", "closing balance", "bal"},
    "value date": {"Value Dt", "ValueDt", "value date"},
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

# Function to find headers and their x0
def find_header_positions(pdf_path):
    header_positions = {}
    with pdfplumber.open(pdf_path) as pdf:
        first_page = pdf.pages[0]
        words = first_page.extract_words()

        for word in words:
            norm_word = normalize(word['text'])
            for header, aliases in HEADER_KEYWORDS.items():
                aliases = [a.lower().strip().replace('.','') for a in aliases]
                if norm_word in aliases and header not in header_positions:
                    header_positions[header] = {
                        'x0': word['x0'],
                        'x1': word['x1']
                    }

    return header_positions


def extract_bank_entries(pdf_path):
    header_positions = find_header_positions(pdf_path)

    def classify_column(x0, x1):
        sorted_headers = sorted(header_positions.items(), key=lambda item: item[1]['x0'])

        closest_col = None
        min_dist = float('inf')

        for i, (col_name, pos) in enumerate(sorted_headers):
            center = (pos['x0'] + pos['x1']) / 2
            dist = abs(x0 - center)

            # Additional condition: word must not lie before previous header's x1
            if i > 0:
                prev_x1 = sorted_headers[i - 1][1]['x1']
                if x0 < prev_x1:
                    continue

            if dist < min_dist:
                min_dist = dist
                closest_col = col_name

            # 2. Additional logic: if this header’s x1 exceeds the next header’s x1,
            # and the word is visually closer to the next header → prefer next column
            if i < len(sorted_headers) - 1:
                next_col_name, next_pos = sorted_headers[i + 1]
                if x1 >= next_pos['x1']:
                    closest_col = next_col_name

        return closest_col if min_dist < 60 else None

    all_entries = []
    last_entry = None

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            words = page.extract_words(use_text_flow=True, keep_blank_chars=True)

            # Step 1: group words by row (by 'top')
            rows = defaultdict(list)
            for word in words:
                top_key = round(word['top'] / 3) * 3  # cluster nearby rows
                rows[top_key].append(word)

            for top, row_words in sorted(rows.items()):
                columns = {
                    "date": "", "description": "",
                    "debit": "", "credit": "",
                    "closing_balance": ""
                }

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
                if columns["credit"] and not columns["debit"]:
                    trans_type = "credit"
                    amount = columns["credit"]
                elif columns["debit"] and not columns["credit"]:
                    trans_type = "debit"
                    amount = columns["debit"]
                else:
                    trans_type = "unknown"
                    amount = ""

                if is_date(columns["date"]):
                    entry = {
                        "date": columns["date"],
                        "description": columns["description"],
                        "amount": amount,
                        "type": trans_type,
                        "closing_balance": columns["closing_balance"]
                    }
                    all_entries.append(entry)
                    last_entry = entry

    return all_entries

# entries = extract_bank_entries("../statements/t4.pdf")
# for e in entries:
#     print(e)
