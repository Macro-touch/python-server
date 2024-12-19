class AttributeModel:

    def __init__(self, entry):
        self.date = entry["date"]
        self.attribute = entry["attribute"]
        self.amount = entry["amount"]
        self.trans_type = entry["type"]

    def __hash__(self) -> int:
        return hash(self.attribute)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, type(self)) and (
            self.attribute == other.attribute
            and (self.attribute != "-" and other.attribute != "-")
        )

    def __ne__(self, other: object) -> bool:
        return isinstance(other, type(self)) and (
            self.attribute != other.attribute
            and (self.attribute == "-" or other.attribute == "-")
        )
