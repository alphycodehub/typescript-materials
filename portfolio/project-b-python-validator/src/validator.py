"""Registration record validator.

Each rule returns a list of error codes. An empty list means the record passed.
"""
import re

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}$")
USERNAME_RE = re.compile(r"^[A-Za-z0-9_]+$")


def check_username(username: str) -> list[str]:
    errors = []
    if not 3 <= len(username) <= 20:
        errors.append("USERNAME_LENGTH")
    if username and not USERNAME_RE.match(username):
        errors.append("USERNAME_CHARS")
    return errors


def check_email(email: str) -> list[str]:
    return [] if EMAIL_RE.match(email) else ["EMAIL_FORMAT"]


def check_password(password: str) -> list[str]:
    errors = []
    if len(password) < 8:
        errors.append("PASSWORD_LENGTH")
    if not any(c.isupper() for c in password):
        errors.append("PASSWORD_UPPER")
    if not any(c.islower() for c in password):
        errors.append("PASSWORD_LOWER")
    if not any(c.isdigit() for c in password):
        errors.append("PASSWORD_DIGIT")
    return errors


def check_age(age: str) -> list[str]:
    try:
        value = int(age)
    except (ValueError, TypeError):
        return ["AGE_NOT_NUMBER"]
    return [] if 18 <= value <= 120 else ["AGE_RANGE"]


def check_country(country: str) -> list[str]:
    return [] if country and country.strip() else ["COUNTRY_MISSING"]


def validate_record(record: dict) -> list[str]:
    """Run all rules in a fixed order and return every error code found."""
    return (
        check_username(record.get("username", ""))
        + check_email(record.get("email", ""))
        + check_password(record.get("password", ""))
        + check_age(record.get("age", ""))
        + check_country(record.get("country", ""))
    )
