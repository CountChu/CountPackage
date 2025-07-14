
-- Usage:
--  osascript 03-insert-rows-args.applescript "test_data/A.numbers" 1 2 4
--

on run argv
    if (count of argv) > 0 then
        set docPath to item 1 of argv
        set sheetIndex to item 2 of argv as integer
        set rowCount to item 3 of argv as integer
        set baseRow to item 4 of argv as integer
    end if

    #display dialog sheetIndex

    tell application "Numbers"
        -- Open the document
        open docPath
        delay 1 -- Give time for the document to fully load

        tell document 1
            tell sheet sheetIndex
                tell table 1
                    set lastRowIndex to row count
                    set lastRow to row lastRowIndex
                    set baseRow to row baseRow
                    
                    repeat rowCount times
                        -- Add a new row below the current last row
                        set newRow to add row below lastRow
                        
                        -- Copy formatting and formulas from lastRow to newRow
                        repeat with i from 1 to (count of cells of lastRow)
                            -- set value of cell i of newRow to value of cell i of baseRow
                            try
                                set cellFormat to format of cell i of baseRow
                                -- display dialog cellFormat
                                set format of cell i of newRow to cellFormat
                            end try                        
                            try
                                set cellFormula to formula of cell i of baseRow
                                set formula of cell i of newRow to cellFormula
                            end try
                        end repeat
                        
                        -- Update lastRow reference to the new one for next loop
                        set lastRow to newRow
                    end repeat
                end tell
            end tell
        end tell
    end tell


end run
