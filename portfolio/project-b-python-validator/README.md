# Registration Data Validator: Python Test Automation Sample

> **Portfolio project.** Uses made-up sample data only. No real users or systems.

## What it does
Reads a CSV of user registration records, checks every record against a fixed set of
rules, and writes a PASS/FAIL result with machine-readable error codes for each one.
A pytest suite verifies the rules (including boundary values) and checks the real output
against a hand-written expected file.

## Rules
| Field | Rule | Error code(s) |
|---|---|---|
| username | 3-20 characters | USERNAME_LENGTH |
| username | letters, digits, underscore only | USERNAME_CHARS |
| email | valid `name@domain.tld` shape | EMAIL_FORMAT |
| password | at least 8 characters | PASSWORD_LENGTH |
| password | contains an uppercase letter | PASSWORD_UPPER |
| password | contains a lowercase letter | PASSWORD_LOWER |
| password | contains a digit | PASSWORD_DIGIT |
| age | whole number | AGE_NOT_NUMBER |
| age | between 18 and 120 inclusive | AGE_RANGE |
| country | not empty | COUNTRY_MISSING |

## Run it
```bash
pip install -r requirements.txt
python src/run_checks.py          # writes data/actual_output.csv
diff data/actual_output.csv data/expected_output.csv
python -m pytest -v               # full test suite
```

## Files
- `src/validator.py`: the rules
- `src/run_checks.py`: CSV in, CSV out, summary line
- `data/sample_input.csv`: 14 sample records (3 valid, 11 invalid, with boundary cases 18 and 120)
- `data/expected_output.csv`: expected results, written by hand from the rules above
- `data/actual_output.csv`: real output from the last run
- `data/test_summary.txt`: real pytest output from the last run
- `tests/test_validator.py`: 27 tests

## Results (last run)
- Sample run: 14 records, 3 passed, 11 failed, as expected
- `diff` of actual vs expected output: identical
- pytest: **27 passed, 0 failed**

## Design notes
- Every failing record reports *all* its errors, not just the first (see record 12).
- Boundary values (username 3/20, age 18/120, password length 8) have their own tests.
- Expected output was written independently of the code, so the comparison test is a
  genuine check rather than the code agreeing with itself.
