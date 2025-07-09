import pdfplumber
import json

from extractors.without_breaker import without_breaker
from extractors.with_breaker import with_breaker
from extractors.final_extractor import extract_bank_entries
from formatters.entry_format import format_entries
from scripts.segregate import segregate


def extract_data(pdf_path: str):
    with pdfplumber.open(pdf_path) as pdf:
        method = "with_breaker"
        table_data = with_breaker(pdf)

        if json.dumps(table_data) == "[]":
            try:
                method = "without_breaker"
                print("Extraction using With-Breaker failed: ", flush=True)
                table_data = without_breaker(pdf)

            except Exception as e:
                method = "ternary"
                print("Extraction using Without-Breaker failed: ", e, flush=True)
                table_data = extract_bank_entries(pdf_path)

        print(method)
        return table_data


def process_pdf(file):
    print("Processing pdf...")
    data = extract_data(file)

    try:
        print("Formatting processed data...")
        formatted_entry = format_entries(data)

    except Exception as e:
        print("Formatting entries failed: ", e, flush=True)
        return {}

    print("Segregating formatted data...")
    return segregate(formatted_entry)