#
# FILENAME.
#       test2.py - Test2 Python App.
#
# FUNCTIONAL DESCRIPTION.
#       The app tests functions.
#
# NOTICE.
#       Author: visualge@gmail.com (CountChu)
#       Created on 2025/3/11
#       Created on 2025/3/11
#

from pathlib import Path

from Count import cnt_config
from Count.cnt_ft import Database, FileTable

br = breakpoint

test_p = Path(__file__).parent / "../InvestForge/InvDatabase"
cfg = cnt_config.load(test_p / "config.yaml")


def test_get_files_1():
    db = Database(cfg)
    ft = db.build_file_table("history")
    ft.load()

    filter = {
        "date": "2025-07-08",
    }
    file_p_ls = ft.get_files(filter)
    assert len(file_p_ls) == 56

    filter = {
        "date": "2025-07-08",
        "stockId": "0050.TW",
    }
    file_p_ls = ft.get_files(filter)
    assert len(file_p_ls) == 1


def test_get_files_2():
    db = Database(cfg)
    ft = db.build_file_table("history")
    ft.load()

    filter = {
        "date": "2025-07-08",
        "stockId": ["0050.TW", "0056.TW"],
    }
    file_p_ls = ft.get_files(filter)
    assert len(file_p_ls) == 2

    filter = {
        "date": "2025-07-08",
        "stockId": ["0050.TW", "XXXX.TW"],
    }
    file_p_ls = ft.get_files(filter)
    assert len(file_p_ls) == 1


def test_get_files_3():
    db = Database(cfg)
    ft = db.build_file_table("history")
    ft.load()

    filter = {
        "stockId": ["0050.TW", "0056.TW"],
    }
    last = "date"
    file_p_ls = ft.get_files(filter, last)
    assert len(file_p_ls) == 2


def test_get_one_file():
    db = Database(cfg)
    ft = db.build_file_table("history")
    ft.load()

    filter = {
        "date": "2025-07-08",
        "stockId": "0050.TW",
    }
    file_p = ft.get_one_file(filter)
    print(f"file_p: {file_p}")


def test_build_file_p():
    db = Database(cfg)
    ft = db.build_file_table("history")

    columns = {
        "date": "2025-07-09",
        "stockId": "0050.TW",
    }
    file_p = ft.build_file_p(columns)
    print(f"file_p: {file_p}")

    columns = {
        "date": "2025-07-09",
    }
    file_p = ft.build_file_p(columns)
    assert file_p is None


def test_load_json_as_array():
    db = Database(cfg)
    ft = db.build_file_table("history")
    ft.load()

    filter = {
        "date": "2025-07-08",
    }
    file_p_ls = ft.get_files(filter)

    data = FileTable.load_json_as_array(file_p_ls)
    assert len(data) == 56


def test_get_last_value():
    db = Database(cfg)
    ft = db.build_file_table("history")
    ft.load()

    date = ft.get_last_value("date")
    print(f"date: {date}")
