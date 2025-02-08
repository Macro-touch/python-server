class OversightFormat:
    def __init__(self, data) -> None:
        self.data = data
        self.amount_oversight = {"DR": [0, 0], "CR": [0, 0]}
        self.calculate_oversight()

    def calculate_oversight(self):
        """Calculate the total amount and count for each transaction type."""
        for entry in self.data:
            transaction_amount = self.get_transaction_amount(entry)
            transaction_type = self.get_transaction_type(entry)
            self.update_oversight(transaction_type, transaction_amount)
        # self.print_oversight_summary()

    def get_transaction_amount(self, entry) -> float:
        """Extract and return the transaction amount as a float."""
        return float(entry["amount"])

    def get_transaction_type(self, entry) -> str:
        """Extract and return the transaction type."""
        return entry["type"]

    def update_oversight(self, transaction_type: str, transaction_amount: float):
        """Update the oversight data with the new transaction."""
        self.amount_oversight[transaction_type][0] += transaction_amount
        self.amount_oversight[transaction_type][1] += 1

    def print_oversight_summary(self):
        """Print the oversight summary for debugging."""
        print(self.amount_oversight)

    def get_threshold(self) -> float:
        """Calculate and return the threshold as 15% of the maximum amount."""
        max_amount = max(
            float(self.amount_oversight["DR"][0]), float(self.amount_oversight["CR"][0])
        )
        return round(max_amount * 15 / 100, 2)

    def get_closure_table(self) -> list:
        """Return a table summarizing amounts and transaction counts."""
        return [
            ["Amount", self.amount_oversight["DR"][0], self.amount_oversight["CR"][0]],
            ["Transaction", self.amount_oversight["DR"][1], self.amount_oversight["CR"][1]],
        ]

    def get_totals(self) -> list[float]:
        """Return the total amounts for 'DR' and 'CR' transactions, rounded to two decimals."""
        return [
            round(self.amount_oversight["DR"][0], 2),
            round(self.amount_oversight["CR"][0], 2),
        ]
