import pdfplumber
import re
import json
import sys
import PyPDF2
import os
from segregate import segregate
from without_breaker import without_breaker
from with_breaker import with_breaker

# Define global variables or constants
decimal_pattern = re.compile(r"[\d,]+\.\d{2}")
new_line_patterns = [
    re.compile(
        r"(\b\d{2}/\d{2}/\d{2}\b) ([a-zA-Z0-9\-@#*/.]+)\s+([a-zA-Z0-9]+)\s+(\b\d{2}/\d{2}/\d{2}\b) (?:(\s|[\d,]+\.\d{2})) ?(?:(\s|[\d,]+\.\d{2}))?\s([\d,]+\.\d{2})"
    ),
    re.compile(
        r"(\b\d{2}-[A-Z]{3}-\d{4}\b) (\b\d{2}-[A-Z]{3}-\d{4}\b) ([A-Za-z0-9/.-]+) ([A-Za-z0-9]+) (\d+\.\d{2}) (\d+,\d+\.\d{2}) (\d+,\d+\.\d{2})"
    ),
]
contains_new_line = re.compile(r"^\d+(\.\d*)?\n(?:[a-zA-Z]{0,2}|\d+)$")
date_pattern = re.compile(r"(\b\d{2}/\d{2}/\d{2}\b)")

from typing import List


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


def combine_text_lines(text):
    combined_text = ""
    condition_met = False

    for line in text.split("\n"):
        match_found = False
        print(line)
        # Check each pattern to see if it matches the line
        for pattern in new_line_patterns:
            if pattern.match(line):
                match_found = True
                condition_met = True
                # Add line with newline if it ends with a decimal, otherwise append to the previous line
                combined_text += (
                    f"\n{line}"
                    if decimal_pattern.search(line.split()[-1])
                    else f" {line}"
                )
                break

        # For unmatched lines after the condition has been met
        if not match_found and condition_met:
            # Continue appending if line does not end with a decimal
            if not decimal_pattern.search(line.split()[-1]):
                combined_text += f" {line}"

    return combined_text


def find_text_position(value, page_num, pdf, texts):
    page = pdf.pages[page_num]
    raw_text = page.extract_words()
    rvalue = [item for item in raw_text if item.get("text") == value]

    # print(raw_text)

    if len(rvalue) > 1:

        if len(texts) == 0:
            texts.append(value)

        elif len(texts) != 0:
            if value not in texts:
                texts = []
            texts.append(value)

        return [rvalue[len(texts) - 1]]

    return [item for item in raw_text if item.get("text") == value] if rvalue else None


def with_breaker_(pdf):
    tables = []
    for page in pdf.pages:
        rows = page.extract_table()

        if rows:
            tables.extend(rows)

    if tables:
        headers = tables[0]
        table_data = [
            {
                headers[col]: (
                    float(val)
                    if val.isdigit()
                    else (
                        val.split("\n")[0]
                        if bool(contains_new_line.match(val))
                        else val
                    )
                )
                for col, val in enumerate(row)
                if headers[col]
            }
            for row in tables[1:]
        ]

        return table_data

    return []


def without_breaker_(pdf):
    final = []
    texts = []  # Initialize texts here, if needed across multiple pages
    for page_num, page in enumerate(pdf.pages):
        entry_dict = {}
        combined_text = combine_text_lines(page.extract_text())

        for line in combined_text.split("\n"):
            trimmed = line.split(" ")[:7]
            if len(trimmed) > 1:
                entry = trimmed
                entry_dict["Date"] = entry[0]
                entry_dict["Description"] = (
                    entry[1] + entry[-1] if len(entry) == 7 else entry[1]
                )
                found = find_text_position(entry[4], page_num, pdf, texts)
                if found:
                    pos = found[0]["x1"]
                    entry_dict["Amount"] = found[0]["text"].replace(",", "")
                    entry_dict["Type"] = "CR" if pos == 548.187 else "DR"
                entry_dict["Closing Balance"] = entry[5].replace(",", "")
                final.append(entry_dict.copy())

    return final


def extract_data(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        # with_breaker(pdf)
        without_breaker(pdf)

    # table_data = (
    #     with_breaker(pdf)
    #     if json.dumps(with_breaker(pdf)) != "[]"
    #     else without_breaker(pdf)
    # )

    # return table_data


def process_pdf(file, password, output_name, threshold, lang):
    decrypted_file = decrypt_pdf(file, password, output_name)
    final_data = extract_data(decrypted_file)
    os.remove(decrypted_file)

    return segregate(final_data, threshold, lang)


# extract_data("statements/h.pdf")

if __name__ == "__main__":
    file = sys.argv[1]
    password = "" if sys.argv[2] == "null" else str(sys.argv[2])
    output_name = sys.argv[3]
    threshold = 0 if sys.argv[4] == "null" else str(sys.argv[4])
    lang = 0 if sys.argv[5] == "null" else int(sys.argv[5])

    process_pdf(file, password, output_name, threshold, lang)
