
import re


class DescriptionClassifier:
    def __init__(self, desc: str):
        self.desc = desc

    def mode_of_payment_finder(self) -> str | None:
        desc_upper = self.desc.upper()
        mode_patterns = {
            "UPI": r"UPI.*?(?=\s|$)",
            "IMPS": r"IMPS.*?(?=\s|$)",
            "NEFT": r"NEFT.*?(?=\s|$)",
            "CHQ": r"CHQ.*?(?=\s|$)",
            "RTGS": r"RTGS.*?(?=\s|$)|RTG.*?(?=\s|$)",
        }

        mode = next((key for key, pattern in mode_patterns.items() if re.search(pattern, desc_upper)), None)

        return mode

    def categorize_govt_entry(self, entry, trans_type: str, categories:dict):
        conditions = {
            "TDS": ["TDS"],
            "Grant": ["GRANT"],
            "Tax Refund": ["REFUND", "TAXDEPARTMENT"],
            "Advance Tax": ["ADVTAX", "ADVANCETAX", "PAID"],
            "EMI": ["EMI", "INST", "INSTALLMENT", "INSTALMENT"],
            "Closure": ["PF CLOSURE", "PENSION CLOSURE", "DEPOSIT CLOSURE", "CLOSURE", "TERMINATED"],
            "Interest": ["INT", "INTEREST", "INT RECEIVED", "INTEREST RECEIVED"],
        }

        for category, keywords in conditions.items():
            if any(keyword in self.desc for keyword in keywords):
                if category == "Interest":
                    new_interest = [
                        entry[0],
                        self.desc,
                        entry[2] if trans_type == "DR" else 0,
                        entry[2] if trans_type == "CR" else 0,
                    ]
                    categories["Interest"].append(new_interest)
                else:
                    categories[category].append(entry)

                break
