import re

def is_valid_name(name: str) -> bool:
    """
    Validate name format.
    name must be 3-20 characters long, can contain letters, numbers,
    underscores, and hyphens. It cannot start or end with an underscore or hyphen.
    """
    pattern = r"^(?!.*[_-]{2})(?![-_])[a-zA-Z0-9_-]{3,20}(?<![-_])$"
    return re.fullmatch(pattern, name) is not None


def is_valid_email(email: str) -> bool:
    """
    Validate email format according to RFC 5322.
    """
    pattern = (
        r"^(?!.*\.\.)([a-zA-Z0-9][a-zA-Z0-9._%+-]{0,63})@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    )
    return re.fullmatch(pattern, email) is not None


def is_valid_password(password: str) -> bool:
    """Password must be at least 8 characters long,
    contain at least 1 uppercase letter, 1 lowercase letter, 1 number,
    and 1 special character (can be any non-alphanumeric character).
    No spaces are allowed.
    """
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_])\S{8,}$"
    return re.fullmatch(pattern, password) is not None
