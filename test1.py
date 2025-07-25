#
# FILENAME.
#       test1.py - Test1 Python App.
#
# FUNCTIONAL DESCRIPTION.
#       The app tests functions.
#
# NOTICE.
#       Author: visualge@gmail.com (CountChu)
#       Created on 2025/3/11
#       Created on 2025/3/11
#

import pytest
from pathlib import Path

from Count import cnt_numbers
from Count import cnt_script

br = breakpoint

# Test cnt_numbers


@pytest.mark.parametrize(
    "col, exp",
    [
        (1, "A"),
        (2, "B"),
        (26, "Z"),
        (27, "AA"),
        (28, "AB"),
        (52, "AZ"),
        (53, "BA"),
        (54, "BB"),
        (702, "ZZ"),
        (703, "AAA"),
        (704, "AAB"),
    ],
)
def test_get_column_letter(col, exp):
    assert cnt_numbers.get_column_letter(col) == exp


@pytest.mark.parametrize(
    "letter, exp",
    [
        ("A", 1),
        ("B", 2),
        ("Z", 26),
        ("AA", 27),
        ("AB", 28),
        ("AZ", 52),
        ("BA", 53),
        ("BB", 54),
        ("ZZ", 702),
        ("AAA", 703),
        ("AAB", 704),
    ],
)
def test_get_column_index(letter, exp):
    assert cnt_numbers.get_column_index(letter) == exp


# Test cnt_script


def test_numbers_add_rows():
    fn_p = Path("test_data/投資 - 下單.numbers")
    assert fn_p.exists(), f"File {fn_p} does not exist."
    sheet_index = 1
    row_count = 3
    base_row = 4
    br()
    cnt_script.numbers_add_rows(fn_p, sheet_index, row_count, base_row)
