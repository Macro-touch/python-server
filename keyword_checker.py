import re


class KeywordChecker:
    def __init__(self, desc: str):
        self.desc = desc

    def contains_keyword(self) -> str | None:
        # Compile the regex pattern for keywords
        keywords = [
            "tax",
            "ibrtgs",
            "ACCOUNT",
            "neft",
            "upi",
            "imps",
            "chq",
            "rtgs",
            "atm",
            "coll",
            "vps",
            "transfer",
            "paytm",
            "transferee",
            "to",
            "from",
            "by",
            "depo",
            "clearing",
            "withdrawal",
            "NEWCARDISSUE",
            "impbill",
            "trf",
            "payment",
            "chrgs",
            "remit",
            "bank",
            "ecom",
            "pos",
            "apbs",
            "chg",
            "cash",
            "cheque",
            "dd",
            "eft",
            "swift",
            "web",
            "net",
            "liq",
            "mobile",
            "tfr",
            "wdl",
            "dep",
            "deposit",
            "tds",
            "grant",
            "emi",
            "inst",
            "installment",
            "int",
            "interest",
            "pf",
            "pension",
            "closure",
            "terminated",
            "ins",
            "insurance",
            "refund",
            "advtax",
            "advancetax",
            "bill",
        ]
        keyword_list = "|".join(keywords)
        key_pattern = re.compile(
            r"\\b(?:" + keyword_list + r")\\b", flags=re.IGNORECASE
        )

        pattern = re.compile(
            r"(?=.*[a-zA-Z]{3,})(?=.*\d{3,})[a-zA-Z\d.]+@[a-zA-Z]{3,}"
        )
        match = re.findall(pattern, self.desc)

        if not match:
            pattern = re.compile(r"\b[a-zA-Z@\s]{6,}\d*\b")
            match = re.findall(pattern, self.desc)

        if len(match) > 0 and "WITHDRAWAL TRANSFER" in match[0]:
            return match[0].replace("WITHDRAWAL TRANSFER ", "")

        else:
            for string in match:
                pattern_result = key_pattern.search(string)
                if not bool(pattern_result):
                    return string

        return None

    def contains_non_alphabet_substring(self) -> str | None:
        charge_keyword = [
            "CHARGES",
            "CHG",
            "BG CHARGES",
            "CHRGS",
            "FEE",
            "MISC",
            "MISC-REMIT",
            "BULK",
        ]

        for substring in charge_keyword:
            pattern = re.compile(
                rf"(?<![a-zA-Z]){re.escape(substring)}(?![a-zA-Z])", re.IGNORECASE
            )
            if pattern.search(self.desc.upper()):
                return substring
        return None


    def deduction_checker(self) -> bool:
        deduct_keywords = [
            "INS",
            "INSURANCE",
            "LIFE",
            "HEALTH",
            "PROVI",
            "FUND",
            "PF",
            "PF",
            "SCHL",
            "SCHOOL",
            "CLG",
            "COLLEGE",
            "UNIVERSITY",
            "EDUCATIONAL INSTITUTE",
            "EDU INST",
            "STAMP DUTY",
            "REGISTRATION FEES",
            "STAMP",
            "REGISTRAR OFFICE",
            "PENSION",
            "MONEY",
            "MUTUAL",
            "FUND",
            "ASSET",
            "FINAN",
            "LIFE",
            "MEDI",
            "HOSP",
            "HOSPITAL",
            "CHECKUP",
            "BODYCHECKUP",
            "SCAN",
            "INT",
            "EDU",
            "FINAN",
            "INSTITU",
            "CHARITAB",
            "DONATION",
            "DONA",
            "TRUST",
            "HOME",
            "RENT",
            "INT",
            "HOUSE LOAN",
            "INTEREST",
            "INTREST",
            "ELECTRIC",
            "VEHICLE",
            "POLITICAL",
            "PARTY",
        ]
        deduct_keyword_list = "|".join(deduct_keywords)
        deduct_key_pattern = re.compile(
            r"\b(?:" + deduct_keyword_list + r")\b", flags=re.IGNORECASE
        )

        return bool(deduct_key_pattern.search(self.desc.upper()))
