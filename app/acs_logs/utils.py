import re


def date_validation(date_str):
    pattern = r'^20\d{6}$'
    
    if not re.match(pattern, date_str):
        return False
    
    year = int(date_str[:4])
    month = int(date_str[4:6])
    day = int(date_str[6:])
    
    if month < 1 or month > 12:
        return False
    if day < 1 or day > 31:
        return False
    
    return True
