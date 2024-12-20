class OversightFormat:
    amount_oversight = {"DR": [0, 0], "CR": [0, 0]}

    def __init__(self, data) -> None:

        self.data = data
        self.calculate_oversight()

    def calculate_oversight(self):

        for entry in self.data:

            transaction_amount = float(entry["amount"])
            transaction_type = entry["type"]

            self.amount_oversight[transaction_type][0] += transaction_amount
            self.amount_oversight[transaction_type][1] += 1

    def get_threshold(self):
        return round(
            (
                max(
                    float(self.amount_oversight["DR"][0]),
                    float(self.amount_oversight["CR"][0]),
                )
                * 15
            )
            / 100,
            2,
        )

    def get_closure_table(self, header: list) -> list:

        return [
            header,
            ["Amount", self.amount_oversight["DR"][0], self.amount_oversight["CR"][0]],
            [
                "Transaction",
                self.amount_oversight["DR"][1],
                self.amount_oversight["CR"][1],
            ],
        ]

    def get_totals(self) -> list[int]:

        return [
            round(self.amount_oversight["DR"][0], 2),
            round(self.amount_oversight["CR"][0], 2),
        ]
