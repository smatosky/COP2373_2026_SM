"""
input_validator.py

A simple console application that uses regular expressions to validate
a U.S. phone number, a Social Security number (SSN), and a ZIP code.
The user enters each value and the program reports whether each one is
valid. Running the file with the argument --test runs a built-in set of
valid and invalid test cases against each validation function.
"""

import re
import sys

# Phone: optional +1/1 country code, area code (with or without
# parentheses) and exchange that start with 2-9, then four digits.
# Separators may be a dash, dot, or space (or none at all).
PHONE_PATTERN = re.compile(
    r"(?:\+?1[-. ]?)?"
    r"(?:\([2-9]\d{2}\)\s?|[2-9]\d{2}[-. ]?)"
    r"[2-9]\d{2}[-. ]?\d{4}"
)

# SSN: format XXX-XX-XXXX. The area cannot be 000, 666, or 900-999,
# the group cannot be 00, and the serial cannot be 0000.
SSN_PATTERN = re.compile(r"(?!000|666|9\d{2})\d{3}-(?!00)\d{2}-(?!0000)\d{4}")

# ZIP: five digits, optionally followed by a dash and four digits.
ZIP_PATTERN = re.compile(r"\d{5}(?:-\d{4})?")


def validate_phone(phone):
    """
    Check whether a string is a valid U.S. phone number.

    Accepts formats such as 555-234-5678, (555) 234-5678,
    555.234.5678, 5552345678, and +1 555 234 5678. The area code and
    exchange must start with a digit from 2 to 9.

    Args:
        phone (str): the phone number text entered by the user.

    Returns:
        bool: True if the whole string matches, otherwise False.
    """
    return PHONE_PATTERN.fullmatch(phone) is not None


def validate_ssn(ssn):
    """
    Check whether a string is a valid Social Security number.

    The format must be XXX-XX-XXXX. The first group cannot be 000, 666,
    or 900-999, the middle group cannot be 00, and the last group cannot
    be 0000.

    Args:
        ssn (str): the Social Security number text entered by the user.

    Returns:
        bool: True if the whole string matches, otherwise False.
    """
    return SSN_PATTERN.fullmatch(ssn) is not None


def validate_zip(zip_code):
    """
    Check whether a string is a valid U.S. ZIP code.

    Accepts a 5-digit ZIP code (12345) or a ZIP+4 code (12345-6789).

    Args:
        zip_code (str): the ZIP code text entered by the user.

    Returns:
        bool: True if the whole string matches, otherwise False.
    """
    return ZIP_PATTERN.fullmatch(zip_code) is not None


def display_result(label, value, is_valid):
    """
    Display whether one entered value is valid.

    Args:
        label (str): the name of the value, such as "Phone number".
        value (str): the text the user entered.
        is_valid (bool): the result of the validation.

    Returns:
        None
    """
    # If statement: choose the wording based on the validation result
    if is_valid:
        status = "VALID"
    else:
        status = "INVALID"

    print(f"{label} '{value}' is {status}.")


def run_tests():
    """
    Test each validation function with valid and invalid examples.

    Each test case is (function, input text, expected result). The
    function prints PASS or FAIL for every case and a final summary.

    Returns:
        bool: True if every test case passed, otherwise False.
    """
    test_cases = [
        # Phone numbers - valid
        (validate_phone, "555-234-5678", True),
        (validate_phone, "(555) 234-5678", True),
        (validate_phone, "(555)234-5678", True),
        (validate_phone, "555.234.5678", True),
        (validate_phone, "555 234 5678", True),
        (validate_phone, "5552345678", True),
        (validate_phone, "+1 555-234-5678", True),
        (validate_phone, "1-555-234-5678", True),
        # Phone numbers - invalid
        (validate_phone, "123-456-7890", False),
        (validate_phone, "555-123-4567", False),
        (validate_phone, "555-034-5678", False),
        (validate_phone, "555-234-567", False),
        (validate_phone, "555-234-56789", False),
        (validate_phone, "555-abc-5678", False),
        (validate_phone, "(555 234-5678", False),
        (validate_phone, "", False),
        # Social Security numbers - valid
        (validate_ssn, "123-45-6789", True),
        (validate_ssn, "078-05-1120", True),
        (validate_ssn, "899-99-9999", True),
        # Social Security numbers - invalid
        (validate_ssn, "000-12-3456", False),
        (validate_ssn, "666-12-3456", False),
        (validate_ssn, "900-12-3456", False),
        (validate_ssn, "123-00-4567", False),
        (validate_ssn, "123-45-0000", False),
        (validate_ssn, "123456789", False),
        (validate_ssn, "12-345-6789", False),
        (validate_ssn, "123-45-678", False),
        (validate_ssn, "abc-de-fghi", False),
        # ZIP codes - valid
        (validate_zip, "34285", True),
        (validate_zip, "00501", True),
        (validate_zip, "34285-1234", True),
        # ZIP codes - invalid
        (validate_zip, "3428", False),
        (validate_zip, "342851", False),
        (validate_zip, "34285-123", False),
        (validate_zip, "34285 1234", False),
        (validate_zip, "ABCDE", False),
        (validate_zip, "", False),
    ]

    # Accumulators: count the test cases that passed and failed
    passed = 0
    failed = 0

    # Loop through every test case and compare the result to expected
    for function, text, expected in test_cases:
        actual = function(text)
        if actual == expected:
            passed += 1
            result = "PASS"
        else:
            failed += 1
            result = "FAIL"
        print(f"{result}  {function.__name__}({text!r}) -> {actual}")

    print(f"\n{passed} passed, {failed} failed, {len(test_cases)} total.")
    return failed == 0


def main():
    """Get a phone number, SSN, and ZIP code and report if each is valid."""
    print("Input Validator")
    print("Enter a phone number, Social Security number, and ZIP code.\n")

    again = "y"

    # Loop until the user chooses to stop
    while again == "y":
        phone = input("Phone number: ").strip()
        ssn = input("Social Security number (XXX-XX-XXXX): ").strip()
        zip_code = input("ZIP code: ").strip()

        print()
        display_result("Phone number", phone, validate_phone(phone))
        display_result("Social Security number", ssn, validate_ssn(ssn))
        display_result("ZIP code", zip_code, validate_zip(zip_code))

        again = input("\nCheck another set? (y/n): ").strip().lower()
        print()

    print("Goodbye!")


# Run the tests with "--test", otherwise run the interactive program
if __name__ == "__main__":
    if "--test" in sys.argv:
        run_tests()
    else:
        main()
