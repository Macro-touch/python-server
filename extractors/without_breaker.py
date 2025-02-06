from typing import List, Tuple, Optional
import re

from functions.format_functions import contains_two_floats


# all date format regex
date_regex = re.compile(
    r"\b(?:\d{2}-\d{2}-\d{4}|\d{2}/\d{2}/\d{4}|\d{2}/\d{2}/\d{2}|\d{4}-\d{2}-\d{2}|\d{2}-\d{2}-\d{2}|\d{2}\.\d{2}\.\d{4}|\d{4}/\d{2}/\d{2}|\d{8}|\d{4}\.\d{2}\.\d{2}|\d{1,2}-(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*-\d{4}|\d{1,2}\s(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s\d{4}|\d{1,2}\s(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s\d{2}|\d{1,2}\s(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*,?\s\d{4}|\d{1,2}\s(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*|\d{4}/\d{2}/\d{2})\b"
)

# Define configurable keyword lists
HEADER_KEYWORDS = {
    "date": ["date", "txn date", "txndate", "transaction date", "transactiondate"],
    "description": ["particulars", "description", "narration"],
    "debit": [
        "debits",
        "withdrawal",
        "withdrawals",
        "dr",
        "debit amount",
        "debitamount",
        "withdrawalamt.",
    ],
    "credit": [
        "credits",
        "deposit",
        "deposits",
        "cr",
        "credit amount",
        "creditamount",
        "depositamt.",
    ],
    "closing_balance": ["balance", "closing balance", "bal"],
}

value_date_possibilities = ["value date"]
exclude_list = ["value date", "chq.no.", "ref.no.", "ref. no."]
DR_CR_KEYWORDS = ["dr/cr", "cr/dr"]
AMOUNT_KEYWORDS = ["amount", "txn amount", "txnamount", "trxn amount", "trxn amount"]


def is_valid_amount(amount: str) -> bool:
    """
    Returns True when an amount is valid (greater than 0)
    """
    amt = amount

    if amt == "":
        return False

    if amt.count(",") > 0:
        amt = amt.replace(",", "")

    return float(amt) > 0


def is_header_row(
    row: List[str],
    keywords: dict = HEADER_KEYWORDS,
) -> Optional[Tuple[bool, dict, int]]:
    """
    Check if a row is a header row and return the indices of relevant columns.
    :param row: List of strings representing a row.
    :param keywords: Dictionary of keyword lists for each column type.
    :return: Tuple (is_header: bool, indices: dict) or None if not a header row.
    """

    indices = {}

    # Find the index of each column type
    for key, keyword_list in keywords.items():
        for i, cell in enumerate(row):
            
            # neglecting unwanted headers
            if cell is None or cell == "" or cell.lower() in exclude_list: 
                continue

            # Normalize to lowercase for comparison
            cell = cell.lower()
            if key not in indices:

                # Match keywords and avoid overwriting existing indices
                if any(cell in keyword for keyword in keyword_list):
                    indices[key] = i
                    break

                # Fail Case: if the the entry contains 'CR/DR' rather than actual format
                if any(cell in keyword for keyword in DR_CR_KEYWORDS):
                    amount_index = next(
                        (
                            i
                            for i, cell in enumerate(row)
                            if cell.lower() in AMOUNT_KEYWORDS
                        ),
                        None,
                    )
                    indices["amount"] = amount_index
                    indices["cr/dr"] = i


    if len(indices.keys()) >= 3:
        if "date" not in indices.keys():

            for i, cell in enumerate(row):
                
                # neglecting unwanted headers
                if cell is None or cell == "": 
                    continue

                if cell.lower() in value_date_possibilities:
                    indices['date'] = i


    # Ensure all required columns (date, description, debit, credit) are present
    required_columns_1 = ["date", "description", "debit", "credit"]
    required_columns_2 = ["date", "description", "dr/cr"]
    is_header = all(key in indices for key in required_columns_1) or all(
        key in indices for key in required_columns_2
    )

    # Return results only if required columns are found
    if is_header:
        return True, indices

    return False, {}


def find_header_len(row: List[str]) -> int:
    """
    Finds the number of empty string presented in the header row.
    """
    return len(row) - row.count("")


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

    if len(row) > header_len:

        # Remove excessive empty strings
        if row.count("") > 2:
            row.pop(row.index(""))

        # Join broken description if length still exceeds header length
        if len(row) > header_len:

            desc_index = indeces.get("description")
            broken_row_desc = row[desc_index + 1]

            if 1 < len(broken_row_desc) <= 10:
                row[desc_index] = row[desc_index] + " " + broken_row_desc
                row.pop(desc_index + 1)

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
            if indices.get("cr/dr")
            else ("CR" if is_valid_amount(row[indices.get("credit")]) else "DR")
        ),
        "amount": (
            row[indices.get("amount")]
            if indices.get("amount")
            else (
                row[indices.get("credit")]
                if is_valid_amount(row[indices.get("credit")])
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

    entry = {}
    entries: List[dict] = []

    strategies = find_strategy(pdf.pages[0])
    print(strategies)

    for page in pdf.pages:
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

            if not contains_two_floats(row): 
                continue

            # capturing the entry row & working on it
            if row[0] != None and date_regex.match(row[0].lower()):

                if entry:
                    entries.append(entry)
                    entry = {}

                row = clean_row(row, header_len, indeces)
                entry = create_entry(row, indeces)
                # print(row)

                if "closing_balance" in indeces:
                    entry["BALANCE"] = row[indeces.get("closing_balance")]

            # capturing the broken desc in the next lines and adding it to the last accounted entry
            elif is_broken_desc_row(row)[0] and entry:
                desc_index = is_broken_desc_row(row)[1]

                is_last_letter_same = entry["description"][-1] == row[desc_index][0]

                entry[
                    "description"
                ] += f'{" " if (entry["description"][-1] != "-") and (row[desc_index][-1] != "-") and (not is_last_letter_same) else ""}{row[desc_index]}'

        if entry: entries.append(entry)

    return entries
