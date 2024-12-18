from functions import format_functions


class ChartFormatter:

    def __init__(
        self,
        data,
        dr_sorted_list,
        cr_sorted_list,
        total_dr,
        total_cr,
        gross_outcome,
        gross_income,
    ) -> None:

        self.data = data
        self.dr_list = dr_sorted_list
        self.cr_list = cr_sorted_list
        self.total_dr = total_dr
        self.total_cr = total_cr
        self.income_limit = gross_income
        self.outcome_limit = gross_outcome

    # pie_chart - Debit:
    def pie_debit(self):

        pie_debit_list = [[], []]
        tracker = 0

        for entry in self.dr_list:

            amount = float(entry[1])
            tracker += amount

            if len(pie_debit_list[0]) >= 8 or len(pie_debit_list[1]) >= 8:

                pie_debit_list[0].append("Others")
                pie_debit_list[1].append(
                    round(float(self.total_dr) - float(tracker - amount), 2)
                )
                return ["DR", pie_debit_list]

            if tracker > self.outcome_limit:
                pie_debit_list[0].append("Others")
                pie_debit_list[1].append(
                    round(float(self.total_dr) - float(tracker - amount), 2)
                )
                return ["DR", pie_debit_list]

            else:
                pie_debit_list[0].append(entry[0])  # labels
                pie_debit_list[1].append(entry[1])  # values

        return ["DR", pie_debit_list]

    # pie_chart - Credit:
    def pie_credit(self):

        pie_credit_list = [[], []]
        tracker = 0

        for entry in self.cr_list:

            amount = float(entry[2])
            tracker += amount

            if len(pie_credit_list[0]) >= 8 or len(pie_credit_list[1]) >= 8:

                pie_credit_list[0].append("Others")
                pie_credit_list[1].append(
                    round(float(self.total_dr) - float(tracker - amount), 2)
                )
                return ["CR", pie_credit_list]

            if tracker > self.income_limit:
                pie_credit_list[0].append("Others")
                pie_credit_list[1].append(
                    round(float(self.total_cr - float(tracker - amount)), 2)
                )
                return ["CR", pie_credit_list]

            else:
                pie_credit_list[0].append(entry[0])  # labels
                pie_credit_list[1].append(entry[2])  # values

        return ["CR", pie_credit_list]

    # Line chart

    def line_chart(self):

        month_key = ""
        date_key = ""
        graph_months = []
        graph_months_set = set()
        month_data = {}

        graph_dates = []
        graph_dates_set = set()
        date_data = {}

        for d in self.data:

            month_key = format_functions.chart_key(date=d["date"])[0]
            date_key = format_functions.chart_key(date=d["date"])[1]

            # month-wise data
            if month_key not in graph_months_set:
                graph_months_set.add(month_key)
                graph_months.append(month_key)

            if month_key not in month_data:
                month_data[month_key] = {"Month": month_key, "DR": 0, "CR": 0}

            month_data[month_key][d["type"]] += float(d["amount"].replace(",", ""))

            # date-wise data
            if date_key not in graph_dates_set:
                graph_dates_set.add(date_key)
                graph_dates.append(date_key)

            if date_key not in date_data:
                date_data[date_key] = {"Date": date_key, "DR": 0, "CR": 0}

            date_data[date_key][d["type"]] += float(d["amount"].replace(",", ""))

        if len(graph_months) > 1:
            return [month_data, graph_months]

        return [date_data, graph_dates]
