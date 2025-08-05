import pdfplumber
import json

from extractors.with_breaker import with_breaker
from extractors.final_extractor import extract_bank_entries
from formatters.entry_format import format_entries
from scripts.segregate import segregate


def extract_data(pdf_stream: str):
    with pdfplumber.open(pdf_stream) as pdf:
        table_data = with_breaker(pdf)

        if json.dumps(table_data) == "[]":
            print("Table Extraction Failed", flush=True)
            table_data = extract_bank_entries(pdf_stream)

        return table_data


def process_pdf(pdf_stream):
    print("Processing pdf...")
    data = extract_data(pdf_stream)

    try:
        print("Formatting processed data...")
        formatted_entry = format_entries(data)

    except Exception as e:
        print("Formatting entries failed: ", e, flush=True)
        return {}

    print("Segregating formatted data...")
    return segregate(formatted_entry)