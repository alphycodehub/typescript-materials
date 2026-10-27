import csv
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from validator import (check_age, check_country, check_email,  # noqa: E402
                       check_password, check_username, validate_record)
from run_checks import run  # noqa: E402


@pytest.mark.parametrize("value,expected", [
    ("abc", []),                      # lower boundary
    ("a" * 20, []),                   # upper boundary
    ("ab", ["USERNAME_LENGTH"]),
    ("a" * 21, ["USERNAME_LENGTH"]),
    ("bad name", ["USERNAME_CHARS"]),
    ("", ["USERNAME_LENGTH"]),
])
def test_username(value, expected):
    assert check_username(value) == expected


@pytest.mark.parametrize("value,expected", [
    ("a@b.com", []),
    ("first.last+tag@mail.example.co.ke", []),
    ("no-at-sign.com", ["EMAIL_FORMAT"]),
    ("a@b", ["EMAIL_FORMAT"]),
    ("", ["EMAIL_FORMAT"]),
])
def test_email(value, expected):
    assert check_email(value) == expected


@pytest.mark.parametrize("value,expected", [
    ("Passw0rd", []),                 # exactly 8 chars
    ("Pass0rd", ["PASSWORD_LENGTH"]),
    ("password1", ["PASSWORD_UPPER"]),
    ("PASSWORD1", ["PASSWORD_LOWER"]),
    ("Password", ["PASSWORD_DIGIT"]),
])
def test_password(value, expected):
    assert check_password(value) == expected


@pytest.mark.parametrize("value,expected", [
    ("18", []), ("120", []),
    ("17", ["AGE_RANGE"]), ("121", ["AGE_RANGE"]),
    ("abc", ["AGE_NOT_NUMBER"]), ("", ["AGE_NOT_NUMBER"]),
])
def test_age(value, expected):
    assert check_age(value) == expected


@pytest.mark.parametrize("value,expected", [
    ("Kenya", []), ("", ["COUNTRY_MISSING"]), ("   ", ["COUNTRY_MISSING"]),
])
def test_country(value, expected):
    assert check_country(value) == expected


def test_valid_record_has_no_errors():
    record = {"username": "alice_w", "email": "a@b.com", "password": "Passw0rdOK",
              "age": "29", "country": "Kenya"}
    assert validate_record(record) == []


def test_sample_input_matches_expected_output(tmp_path):
    actual = tmp_path / "actual.csv"
    summary = run(ROOT / "data" / "sample_input.csv", actual)
    with open(actual, newline="") as a, open(ROOT / "data" / "expected_output.csv", newline="") as e:
        assert list(csv.reader(a)) == list(csv.reader(e))
    assert summary == {"total": 14, "passed": 3, "failed": 11}
