class UnusualModel:
    def __init__(self, entry):
        self.date = entry["date"]
        self.attribute = entry["attribute"]
        self.amount = entry["amount"]
        self.trans_type = entry["type"]

    def __hash__(self) -> int:
        return hash(f"${self.date}{self.attribute}{self.amount}")

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, type(self))
            and (
                f"${other.date}{other.attribute}{other.amount}"
                == f"${self.date}{self.attribute}{self.amount}"
            )
            and (self.trans_type != other.trans_type)
            and (self.attribute != "-" and other.attribute != "-")
        )

    def __ne__(self, other) -> bool:
        return (
            isinstance(other, type(self))
            and (
                f"${other.date}{other.attribute}{other.amount}"
                != f"${self.date}{self.attribute}{self.amount}"
            )
            and (self.trans_type == other.trans_type)
            and (self.attribute == "-" or other.attribute == "-")
        )


class DuplicateModel:
    def __init__(self, entry):
        self.date = entry["date"]
        self.attribute = entry["attribute"]
        self.amount = entry["amount"]
        self.trans_type = entry["type"]

    def __hash__(self) -> int:
        return hash(f"${self.date}{self.attribute}{self.amount}")

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, type(self))
            and (
                f"${other.date}{other.attribute}{other.amount}{other.trans_type}"
                == f"${self.date}{self.attribute}{self.amount}{self.trans_type}"
            )
            and (self.attribute != "-" and other.attribute != "-")
        )

    def __ne__(self, other) -> bool:
        return (
            isinstance(other, type(self))
            and (
                f"${other.date}{other.attribute}{other.amount}{other.trans_type}"
                != f"${self.date}{self.attribute}{self.amount}{self.trans_type}"
            )
            and (self.attribute == "-" or other.attribute == "-")
        )


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
