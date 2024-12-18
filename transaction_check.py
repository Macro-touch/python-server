from functions import transaction_functions


class TransactionCheck:

    def __init__(self, entry: dict):

        self.date = entry["date"]
        self.description = (entry["description"]).upper()
        self.amount = entry["amount"]
        self.trans_type = entry["type"]

    def charges_checker(self):
        if transaction_functions.charge_checker(self.description) != None:
            return [
                self.date,
                self.description,
                self.amount,
                self.trans_type,
                "Lorem Ipsum is simply dummy text of the printing and typesetting industry.",
            ]

        return None

    def mode_of_payment_checker(self):
        return transaction_functions.mop_checker(self.description)

    def government_grants(self):
        return transaction_functions.govt_checker(self.description)

    def deduction_check(self):
        check = transaction_functions.deduct_checker(self.description)
        if not check or self.trans_type != "DR":
            return False
        else:
            return check
