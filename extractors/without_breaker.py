from typing import List, Tuple, Optional

from functions.format_functions import valid_entry, is_float
from functions.regex_functions import is_date

# Define configurable keyword lists
HEADER_KEYWORDS = {
    "date": ["date", "txn date", "txndate", "transaction date", "transactiondate"],
    "description": ["particulars", "description", "narration", "transaction reference"],
    "debit": {
        "debit", "debits", "withdrawal", "withdrawals", "withdrawl",
        "dr", "debit amount", "debitamount", "withdrawalamt.",
    },
    "credit": { "credit", "credits", "deposit", "deposits",
                "cr", "credit amount", "creditamount", "depositamt."
    },
    "closing_balance": {"balance", "closing balance", "bal"},
}

VALUE_DATE_KEYWORDS = {"value date"}
EXCLUDE_KEYWORDS = {"value date", "chq.no.", "ref.no.", "ref. no.", "ref.No./chq.No.", "chq. / ref. No"}
DR_CR_KEYWORDS = {"dr/cr", "cr/dr"}
AMOUNT_KEYWORDS = {"amount", "txn amount", "txnamount", "trxn amount", "trxn amount"}

from typing import List, Optional, Tuple

def is_header_row(
    row: List[str],
    keywords: dict = HEADER_KEYWORDS,
) -> Optional[Tuple[bool, dict]]:
    """
    Check if a row is a header row and return the indices of relevant columns.
    :param row: List of strings representing a row.
    :param keywords: Dictionary of keyword sets for each column type.
    :return: Tuple (is_header: bool, indices: dict) or (False, {}) if not a header row.
    """
    indices = {}

    # Normalize row and handle None values
    normalized_row = [
        cell.lower().strip() if isinstance(cell, str) else ""
        for cell in row if cell is not None
    ]

    for i, cell in enumerate(normalized_row):
        if not cell or cell in EXCLUDE_KEYWORDS:
            continue

        # First: Handle CR/DR format case
        if cell in DR_CR_KEYWORDS:
            indices["cr/dr"] = i
            amount_index = next(
                (j for j, c in enumerate(normalized_row) if c in AMOUNT_KEYWORDS),
                None,
            )
            if amount_index is not None:
                indices["amount"] = amount_index
            continue

        # Now handle header keyword categories
        for key, keyword_set in keywords.items():
            if key not in indices and cell in keyword_set:
                indices[key] = i
                break  # no need to check other keys for this cell

    # Handle missing 'date' with fallback to 'value date'
    if "date" not in indices:
        for i, cell in enumerate(normalized_row):
            if cell in VALUE_DATE_KEYWORDS:
                indices["date"] = i
                break

    # Determine if the row qualifies as a header
    required_set_1 = {"date", "description", "debit", "credit"}
    required_set_2 = {"date", "description", "cr/dr"}

    is_header = required_set_1.issubset(indices) or required_set_2.issubset(indices)

    if is_header: print(indices)

    return (True, indices) if is_header else (False, {})


def find_header_len(row: List[str]) -> int:
    """
    Finds the number of empty string presented in the header row.
    """
    return len(row) - row.count("") - row.count(None)


def is_broken_desc_row(row: List[str]) -> Optional[Tuple[bool, int]]:
    """
    Returns the True if the row contains a broken description.
    """
    count = 0
    index = 0

    for i, cell in enumerate(row):
        if cell is not None and len(cell) > 1:
            index = i
            count = count + 1

    if count == 1 and row.count(None) == 0:
        return True, index

    return False, -1


def clean_row(row: List[str], header_len: int, indeces: dict) -> List[str]:
    """
    Cleans a row by removing excessive empty strings and fixing broken descriptions.
    """
    
    while len(row) > header_len:
        # Remove excessive Nones:
        if row.count(None) > 0:
            row.remove(None)

        # Remove excessive empty strings
        if row.count("") > 2:
            row.remove("")
            continue

        # Join broken description if length still exceeds header length
        if len(row) > header_len:

            desc_index = indeces.get("description")
            broken_row_desc = row[desc_index + 1]

            if broken_row_desc is not None and 1 < len(broken_row_desc) <= 10:
                row[desc_index] = row[desc_index] + " " + broken_row_desc
                row.pop(desc_index + 1)
            continue

         # Removing any excessive empty strings if still exists
        if len(row) > header_len:
            if row.count("") > 1:
                row.pop(row.index(""))

    return row


def extract_table_strategy(page) -> List:
    """
    Function: Will determine wether to use between the following methods
    returns: table from the pdf
    """
    tables = []

    try:
        tables = page.extract_tables(
            table_settings={
                "horizontal_strategy": "text",
                "min_words_vertical": 12,
            }
        )[1]

    except IndexError:
        tables = page.extract_tables(
            table_settings={
                "vertical_strategy": "text",
                "horizontal_strategy": "text",
                "min_words_vertical": 12,
            }
        )

        tables = tables[0] if len(tables) > 0 else []

    return tables


def create_entry(row: List[str], indices: dict) -> dict:
    """
    Receives row as argument and returns formatted entry
    """
    return {
        "date": row[indices.get("date")],
        "description": row[indices.get("description")],
        "type": (
            row[indices.get("cr/dr")].upper()
            if "cr/dr" in indices
            else "CR" 
                if "credit" in indices and is_float(row[indices.get("credit")]) 
                else "DR"
        ),
        "amount": (
            row[indices.get("amount")]
            if "amount" in indices
            else (
                row[indices.get("credit")]
                if is_float(row[indices.get("credit")])
                else row[indices.get("debit")]
            )
        ),
    }


    
#        v   h
# order: l - t,
#        t - l,
#        t - t,
def find_strategy(first_page):
    v_strategy = "lines"
    h_strategy = "text"

    # thresholds:
    ACCEPTED_ROW_THRESHOLD = 4
    ACCEPTED_LINES_THRESHOLD = 4


    while h_strategy != v_strategy:

        data = first_page.extract_table({
            "vertical_strategy": v_strategy,
            "horizontal_strategy": h_strategy,
            "min_words_vertical": 12,
        })

        if data is not None and len(data) > 0:
            accepted_lines = []
            for row in data:
                # checking if the rows are valid
                if row is not None and len(list(row)) >= ACCEPTED_ROW_THRESHOLD:
                    accepted_lines.append(row)
            
                if len(accepted_lines) > ACCEPTED_LINES_THRESHOLD:
                    # Returning the strategies
                    return [v_strategy, h_strategy]
        
        # Proceeding to the next strategy
        if h_strategy == "text":
            # Swapping the values (l, t -> t, l)
            v_strategy, h_strategy = h_strategy, v_strategy

        else:
            # Final case
            v_strategy = h_strategy = "text"

    return [v_strategy, h_strategy]


def without_breaker(pdf):
    header = []
    header_len = 0
    indeces = {}

    entries: List[dict] = []

    strategies = find_strategy(pdf.pages[0])
    print(strategies)

    for page in pdf.pages:
        entry = {}

        tables = page.extract_table({
            "vertical_strategy": strategies[0],
            "horizontal_strategy": strategies[1],
            "min_words_vertical": 12,
        })

        if tables is None:
            continue

        for index, row in enumerate(tables):

            # capturing the header row & working on it
            # print(row)
            if len(header) == 0:
                is_header, i = is_header_row(row)
                if is_header:
                    header = row
                    header_len = find_header_len(header)
                    indeces = i
                    # print(header)
                    # print(indeces)
                    continue
            
            broken_desc = is_broken_desc_row(row)

            if not valid_entry(row) and not broken_desc[0]: 
                # print(row)
                continue

            # capturing the entry row & working on it
            if row[0] != None and is_date(row[0]):

                if entry:
                    entries.append(entry)
                    entry = {}

                row = clean_row(row, header_len, indeces)
                entry = create_entry(row, indeces)
                print(row)

                # if "closing_balance" in indeces:
                #     entry["BALANCE"] = row[indeces.get("closing_balance")]

            # capturing the broken desc in the next lines and adding it to the last accounted entry
            elif broken_desc[0] and entry:
                desc_index = broken_desc[1]

                is_last_letter_same = entry["description"][-1] == row[desc_index][0]

                entry[
                    "description"
                ] += f'{" " if (entry["description"][-1] != "-") and (row[desc_index][-1] != "-") and (not is_last_letter_same) else ""}{row[desc_index]}'

        if entry: 
            # print(entry)
            entries.append(entry)
        
    # for e in entries:
    #     print(e)

    return entries
