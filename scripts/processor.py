import pdfplumber
import json
import PyPDF2
import os

from extractors.without_breaker import without_breaker
from extractors.with_breaker import with_breaker
from extractors.final_extractor import extract_bank_entries
from formatters.entry_format import format_entries
from scripts.segregate import segregate


def decrypt_pdf(file, password, output_name):
    pdf_reader = PyPDF2.PdfReader(open(file, "rb"))
    if pdf_reader.is_encrypted:
        pdf_reader.decrypt(password)
        pdf_writer = PyPDF2.PdfWriter()
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)
        decrypted_file_path = f"decrypted_{output_name}.pdf"
        with open(decrypted_file_path, "wb") as decrypted_file:
            pdf_writer.write(decrypted_file)
        return decrypted_file_path

    return file


def extract_data(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        table_data = with_breaker(pdf)

        if json.dumps(table_data) == "[]":
            try:
                table_data = without_breaker(pdf)
            except (IndexError, ValueError) as e:
                print("Error during without_breaker:", e, flush=True)
                table_data = extract_bank_entries(pdf_path)

        return table_data


def process_pdf(file, password, output_name):
    decrypted_file = decrypt_pdf(file, password, output_name)

    try:
        data = extract_data(decrypted_file)
        print(data, flush=True)
        formatted_entry = format_entries(data)
    except (IndexError, ValueError) as e:
        print("Error during first extraction or formatting:", e)
        data = extract_bank_entries(decrypted_file)
        formatted_entry = format_entries(data)
    finally:
        os.remove(decrypted_file)

    return segregate(formatted_entry)

# process_pdf(
#     "statements/lvb.pdf",
#     "",
#     "report",
# )
