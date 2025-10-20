
def is_valid_company_name(company_name) -> bool:
    return bool(company_name.strip()) and len(company_name) <= 100
