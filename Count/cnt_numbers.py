#
# FILENAME.
#       cnt_numbers.py - Count Numbers Python Module.
#
# FUNCTIONAL DESCRIPTION.
#       The module provides functions to get data from a Numbers file.
#
# NOTICE.
#       Author: visualge@gmail.com (CountChu)
#       Created on 2024/10/1
#       Updated on 2024/10/1
#

import os
import re

import pandas as pd
from numbers_parser import Document

br = breakpoint

def find_col(rows, title, checked=False, next=None):
    assert type(rows) == list

    out = None
    for y, row in enumerate(rows):
        assert type(row) == list
        
        for x, cell in enumerate(row):
            type_name = str(type(cell))
            assert type_name in [ \
                "<class 'numbers_parser.cell.EmptyCell'>", \
                "<class 'numbers_parser.cell.TextCell'>", \
                "<class 'numbers_parser.cell.MergedCell'>", \
                ], type_name

            if cell.value == None:
                continue

            if cell.value == title:
                if next != None:
                    if next < x:
                        out = x
                        break
                else:
                    out = x
                    break
        
        if out != None:
            break

    if checked:
        if out == None:
            raise ValueError(f'Cannot find column: {title}')

    return out

def get_column_letter(col):
    """
    Convert a column index (1-based) to a column letter (e.g., 1 -> 'A', 2 -> 'B').
    
    :param col: Column index (1-based)
    :return: Column letter
    """
    letter = ''
    while col > 0:
        col, remainder = divmod(col - 1, 26)
        letter = chr(65 + remainder) + letter
    return letter

def get_column_index(letter):
    """
    Convert a column letter (e.g., 'A' -> 1, 'B' -> 2) to a column index (1-based).
    
    :param letter: Column letter
    :return: Column index (1-based)
    """
    col = 0
    for i, c in enumerate(reversed(letter)):
        col += (ord(c) - 64) * (26 ** i)
    return col

def find_col_by_appscript(rows, title, checked=False, next=None):
    assert type(rows) == list

    out = None
    for y, row in enumerate(rows):
        assert str(type(row)) == "<class 'appscript.reference.Reference'>"
        
        for x, cell in enumerate(row.cells()):
            if cell.value == None:
                continue

            if str(cell.value.get()) == title:
                if next != None:
                    next_index = get_column_index(next) - 1 
                    if next_index < x:
                        out = get_column_letter(x+1)
                        break
                else:
                    out = get_column_letter(x+1)
                    break
        
        if out != None:
            break

    if checked:
        if out == None:
            raise ValueError(f'Cannot find column: {title}')

    return out


def find_row(rows, title, y0=0, x0=0):
    y = None
    out = None

    for y, row in enumerate(rows):
        if y < y0:
            continue

        if row[x0].value == None:
            continue

        if str(row[x0].value) == title:
            out = row
            break

    return y, out

def find_right_value(row, start):
    out = None, -1

    for i in range(start+1, len(row)):
        if row[i].value != None:
            out = (row[i], i)
            break

    return out

def collect_sheet_names(doc):
    out = []

    for sheet_obj in reversed(doc.sheets):
        name = sheet_obj.name
        #if len(name.split('/')) != 3:
        #    continue

        out.append(name)

    return out

def load_doc(fn):
    bn = os.path.basename(fn)
    #print(bn)
    doc = Document(fn)
    #br()

    return doc

def find_sheet(doc, sheet_name):
    for sheet_obj in doc.sheets:
        if sheet_obj.name == sheet_name:
            return sheet_obj 

    return None

def find_table(sheet_obj, table_name):
    for table_obj in sheet_obj.tables:
        if table_obj.name == table_name:
            return table_obj

    return None

def ____find_row(rows, date):
    out = None

    for row in rows:
        if row[0].value == None:
            continue

        if str(row[0].value)[:10] == date:
            out = row
            break

    return out

def get_rows(doc, sheet):
    sheet_obj = find_sheet(doc, sheet)
    assert sheet_obj != None

    assert(len(sheet_obj.tables) == 1)

    table = sheet_obj.tables[0]

    rows = table.rows()
    return rows

#
# get a location in a text. 
# E.g., AA3 -> AA, 3, A3 -> A, 3
#

def get_location(text):
    pattern = re.compile(r'(\w+)(\d+)')
    res = pattern.match(text)
    x = res.group(1)
    y = int(res.group(2)) 
    return x, y

def load_df(fn):
    doc = Document(fn)
    sheets = doc.sheets
    table = sheets[0].tables[0]
    data = table.rows(values_only=True)

    df = pd.DataFrame(data[1:], columns=data[0])
    return df