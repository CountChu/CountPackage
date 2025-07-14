#
# FILENAME.
#       cnt_scripts.py - Count Scripts Python Module.
#
# FUNCTIONAL DESCRIPTION.
#       The module provides functions for Apple Scripts.
#
# NOTICE.
#       Author: visualge@gmail.com (CountChu)
#       Created on 2025/3/11
#       Updated on 2025/3/11
#

import subprocess
from pathlib import Path

br = breakpoint


MODULE_P = Path(__file__)
SCRIPT_P = MODULE_P.parent / 'scripts'

def numbers_add_rows(numbers_fn, sheet_index, row_count, base_row):
    script_fn = str(SCRIPT_P / 'numbers_add_rows.applescript')
    cmd = ["osascript", script_fn, numbers_fn, str(sheet_index), str(row_count), str(base_row)]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("Script output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error running AppleScript:", e.stderr)

    pass

def numbers_add_rows_(fn, sheet_index, count):
    lines = ''
    for i in range(count):
        lines += 'add row below row rowCount\n'

    script = f'''
    tell application "Numbers"
        -- Open the document
        set docPath to "{fn}"
        open docPath
        delay 1 -- Give time for the document to open

        -- Get the first document
        tell document 1
            -- Get the sheet by sheet_index
            tell sheet {sheet_index}
                -- Get the first table
                tell table 1
                    -- Get the total number of rows
                    set rowCount to row count
                    
                    -- Add a new row at the bottom
                    {lines}
                end tell
            end tell
        end tell
    end tell
    '''

    subprocess.run(["osascript", "-e", script])