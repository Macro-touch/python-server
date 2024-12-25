import json
import re

from functions.regex_functions import multiple_dates

contains_new_line = re.compile(r"^\d+(\.\d*)?\n(?:[a-zA-Z]{0,2}|\d+)$")


def with_breaker(pdf):
    tables = []

    for page in pdf.pages:
        empty_rows_count = 0

        rows = page.extract_table()

        if rows is None:
            return []

        rows_count = len(rows)
        if rows:
            for row in rows:
                # Taking count of empty rows
                if row.count("") == len(row):
                    empty_rows_count = empty_rows_count + 1

                # Detecting whether the row contains more than one date
                for cell in row:
                    if cell is not None and cell.count("\n") > 3:
                        if multiple_dates(cell):
                            return []

        # Making sure if the rows are fine, no empty rows are taken into the account
        if rows_count > 1 and empty_rows_count < rows_count - 1:
            tables.extend(rows)

    if tables:
        headers = tables[0]
        table_data = [
            {
                headers[col]: (
                    float(val)
                    if val is not None and val.isdigit()
                    else (
                        val.split("\n")[0]
                        if val is not None and bool(contains_new_line.match(val))
                        else val
                    )
                )
                for col, val in enumerate(row)
                if headers[col]
            }
            for row in tables[1:]
        ]

        # for t in table_data:
        #     print(t)

        return table_data

    return []
