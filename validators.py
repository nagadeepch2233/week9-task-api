import re
from datetime import datetime

def validate_email(email):
    """Validate email format"""
    regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(regex, email) is not None

def validate_password(password, min_length=6):
    """Check password meets basic requirements"""
    return password and len(password) >= min_length

def validate_date(date_str, date_format="%Y-%m-%d"):
    """Validate date string format"""
    try:
        datetime.strptime(date_str, date_format)
        return True
    except (ValueError, TypeError):
        return False
