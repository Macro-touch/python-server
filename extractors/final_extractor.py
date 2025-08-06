import pdfplumber
from functions.regex_functions import is_date, extract_amount

# Define header synonyms
HEADER_KEYWORDS = {
    "serial": {"s.no", "sr.no"},
    "date": {"date", "transaction", "txn", "txn date", "txndate", "transaction date", "transactiondate"},
    "description": { "remarks", "details of transaction", "transaction details", "particulars", "description", "narration", "transaction reference"},
    "debit": {
        "debit", "debits", "withdrawal", "withdrawal amt", "withdrawalamt", "withdrawals", "withdrawl",
        "dr", "debit amount", "debitamount", "withdrawalamt.",
    },
    "credit": { "credit", "credits", "deposit amt" , "deposit", "deposits", "depositamt",
                "cr", "credit amount", "creditamount", "depositamt."
    },
    "amount": {"amount", "amount(rs.)", "amt", "trxn amount", "trxnamount", "withdrawal(dr)/"},
    "type": {"type", "txn type", "txntype", "dr/cr", "cr/dr", "transaction type"},
    "closing_balance": {"balance", "balance(inr)", "closingbalance", "closing balance", "bal"},
    "value date": {"Value Dt", "value", "ValueDt", "value date"},
    "ref. no.": {"chq.no.", "chq no", "ref.no.", "chq/ref No", "ref. no.", "ref.No./chq.No.", "chq. / ref. No", "Chq./Ref.No.", "reference no."},
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

def format_headers(header_list: list[dict]) -> list[dict]:
    merged = []

    for current in header_list:
        merged_flag = False
        for existing in merged:
            if current['header'] == existing['header']:
                # Check if current x0-x1 is fully inside existing range AND has higher top value
                if existing['x0'] <= current['x0'] <= current['x1'] <= existing['x1'] and current['top'] > existing['top']:
                    # Merge: expand x0 and x1, keep the top of the existing (lower one)
                    existing['x0'] = min(existing['x0'], current['x0'])
                    existing['x1'] = max(existing['x1'], current['x1'])
                    merged_flag = True
                    break

        if not merged_flag:
            # Only add if it's the first one of its type
            if not any(current['header'] == m['header'] for m in merged):
                merged.append(current.copy())

    return merged


def find_header_positions(headers: list[dict], page_width: int, average_y_axis: int):
    y_axis_range = [average_y_axis - 10, average_y_axis + 10]
    
    # sorting headers based on the x0 (ascending)
    sorted_headers = sorted(headers, key=lambda item: item['x0'])
    
    # removing the out of bound headers
    ranged_headers = format_headers([h for h in sorted_headers if  h['top'] >= y_axis_range[0] and h['top'] <= y_axis_range[1]])

    positions = {}
    start = 0
    for i, header in enumerate(ranged_headers):
        
        end = page_width
        if i < len(ranged_headers) - 1:
            end = ranged_headers[i + 1]['x0']
        
        positions[header['header']] = [start, end]
        start = header['x1']

    print(positions)
    return positions

# Function to find headers and their x0
def find_headers(pdf_path):
    page_num = 0
    page_width = 0
    
    with pdfplumber.open(pdf_path) as pdf:
        while page_num < len(pdf.pages):
            curr_page = pdf.pages[page_num]
            page_width = curr_page.width
            possible_headers = []
            total_y_axis = 0
            words = curr_page.extract_words(
                            x_tolerance=0.5, 
                            y_tolerance=3, 
                            use_text_flow=True, 
                            keep_blank_chars=True
                        )

            for word in words:
                norm_word = normalize(word['text'])
                for header, aliases in HEADER_KEYWORDS.items():
                    aliases = [normalize(a) for a in aliases]
                    if norm_word in aliases:
                        possible_headers.append({
                            'header': header,
                            'x0': word['x0'],
                            'x1': word['x1'],
                            'top': word['top']
                        })
                        total_y_axis += word['top']
            
            if len(possible_headers) > 0:
                break

            page_num = page_num + 1

    print("Header found on page num: ", page_num)
    return find_header_positions(
            possible_headers, 
            page_width, 
            total_y_axis / len(possible_headers)
        )


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

            row = []
            rows = []
            row_start_x0 = 0
            
            for word in words:
                if word['x0'] < row_start_x0:
                    if len(row) > 0:
                        rows.append(row)
                        row = []
                
                row.append(word)
                row_start_x0 = word['x0']
            
            # Adding the last entry into rows at page end;
            if len(row) > 0:
                rows.append(row)
                row = []

            for row_words in rows:
                total_words = len(row_words)
                
                # Invalid no. of cells in a row
                if total_words <= 3:
                    continue
                
                columns = {
                    "date": "", "description": "",
                    "debit": "", "credit": "",
                    "amount": "", "type": "",
                    "closing_balance": ""
                }
                
                # Capturing broken description
                # Valid only if the extraction order is like:
                    # Date
                    # -> Desc. line: 1
                    # -> Desc. line: 2
                    # Amount
                    # Balance
                curr = 0
                while curr < total_words:
                    word = row_words[curr]
                    
                    next = curr + 1
                    while next < total_words and word["x0"] == row_words[next]["x0"]:
                        word["text"] += row_words[next]["text"]
                        word["x1"] = max(word["x1"], row_words[next]["x1"])
                        next += 1
                    curr = next

                    col = classify_column(word["x0"], word["x1"])
                    if col and col in columns.keys():
                        columns[col] += word["text"] + " "

                # Clean up and strip extra spaces
                for key in columns:
                    columns[key] = columns[key].strip()

                if is_broken_line(columns) and last_entry:
                    # Merge broken description
                    last_entry["DESCRIPTION"] += " " + columns["description"]
                    continue

                # Skip empty or header rows
                if not columns["date"] or columns["date"].lower().startswith("date"):
                    continue
                
                amount = ""
                trans_type = "unknown"

                # Determine transaction type
                if columns["credit"] and columns['credit'] != '-' and (columns['debit'] == '-' or not columns["debit"]):
                    trans_type = "credit"
                    amount = columns["credit"]
                elif columns["debit"] and columns['debit'] != '-' and (columns['credit'] == '-' or not columns["credit"]):
                    trans_type = "debit"
                    amount = columns["debit"]
                elif columns["amount"] and columns["type"]:
                    trans_type = columns["type"].lower()
                    if "cr" in trans_type or "credit" in trans_type:
                        trans_type = "credit"
                    elif "dr" in trans_type or "debit" in trans_type:
                        trans_type = "debit"
                    amount = columns["amount"]
                else:
                    if columns["amount"] is None:
                        continue
                    amount = columns['amount'].strip().lower()
                    
                    if columns["amount"] != "-" and len(columns['amount']) > 0:
                        if "cr" in amount:
                            trans_type = "CR"
                        if "dr" in amount:
                            trans_type = "DR"
                            
                # Invalid date
                if not is_date(columns["date"]):
                    continue
                
                # Invalid entry or description in an entry
                desc = columns['description'].lower().strip()
                if len(desc) == 0 or "closing balance" in desc or "opening balance" in desc:
                    continue
                
                # Invalid amount in an entry
                if amount == "" or amount is None or trans_type == 'unknown':
                    continue

                entry = {
                    "DATE": columns["date"],
                    "DESCRIPTION": columns["description"],
                    "AMOUNT": extract_amount(str(amount)),
                    "TYPE": trans_type,
                    "CLOSING_BALANCE": columns["closing_balance"]
                }
                # print(entry, flush=True)
                all_entries.append(entry)
                last_entry = entry

    return all_entries
