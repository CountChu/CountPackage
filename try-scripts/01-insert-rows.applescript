tell application "Numbers"
    -- Open the document
    set docPath to "/Users/visualge/Dropbox/2-Areas-I/CountPackage/test_data/投資 - 下單.numbers"
    open docPath
    delay 1 -- Give time for the document to fully load

    tell document 1
        tell active sheet
            tell table 1
                set lastRowIndex to row count
                set lastRow to row lastRowIndex
                set baseRow to row 4
                
                repeat 2 times
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
