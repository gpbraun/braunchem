-----------------------------------------------------------------
-- row_width.lua
--
-- Gabriel Braun, 2023
-----------------------------------------------------------------

local re = require "re"


function Table(tbl)
    local head_row = tbl.head.rows[1]

    if head_row == nil then
        return tbl
    end

    for i, colspec in ipairs(tbl.colspecs) do
        colspec[2] = 1

        local cell = head_row.cells[i].contents[1]
        if cell.content[1].tag == "Str" then
            local match = re.match(cell.content[1].text, "'['{%d+}']'")
            if match ~= nil then
                colspec[2] = match
                table.remove(cell.content, 1)
            end
        end
    end

    return tbl
end

-----------------------------------------------------------------
-- Export
-----------------------------------------------------------------

return {
    { Table = Table }
}
