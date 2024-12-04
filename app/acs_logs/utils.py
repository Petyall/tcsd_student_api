import re


def date_validation(date: str) -> bool:
    pattern = r'^20\d{6}$'
    
    if not re.match(pattern, date):
        return False
    
    year = int(date[:4])
    month = int(date[4:6])
    day = int(date[6:])
    
    if month < 1 or month > 12:
        return False
    if day < 1 or day > 31:
        return False
    
    return True
