def is_valid_contract_amount(amount_str: str) -> bool:
    try:
        amount = float(amount_str)
        return amount >= 0
    except ValueError:
        return False


def is_valid_contract_amount_due(amount_due_str: str) -> bool:
    try:
        amount_due = float(amount_due_str)
        return amount_due >= 0
    except ValueError:
        return False
