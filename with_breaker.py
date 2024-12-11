import re

contains_new_line = re.compile(r"^\d+(\.\d*)?\n(?:[a-zA-Z]{0,2}|\d+)$")


def with_breaker(pdf):
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
