import pdfplumber
import json
import sys
import PyPDF2
import os

from create_entry import extract_entries
from without_breaker import without_breaker
from with_breaker import with_breaker


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
        # with_breaker(pdf)
        # without_breaker(pdf)

        table_data = (
            with_breaker(pdf)
            if json.dumps(with_breaker(pdf)) != "[]"
            else without_breaker(pdf)
        )

        return table_data


def process_pdf(file, password, output_name):
    decrypted_file = decrypt_pdf(file, password, output_name)
    final_data = extract_data(decrypted_file)
    os.remove(decrypted_file)

    return extract_entries(final_data)


if __name__ == "__main__":
    file = sys.argv[1]
    password = "" if sys.argv[2] == "null" else str(sys.argv[2])
    output_name = sys.argv[3]

    process_pdf(file, password, output_name)

# process_pdf(
#     "statements/iob.pdf",
#     "",
#     "report",
# )
