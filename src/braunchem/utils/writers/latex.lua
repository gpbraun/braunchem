-----------------------------------------------------------------
-- latex.lua
--
-- Gabriel Braun, 2023
-----------------------------------------------------------------

-----------------------------------------------------------------
-- Containers
-----------------------------------------------------------------

function Div(elem)
    local env_name = elem.classes[1]
    local env_title = ""

    elem.content = elem.content:walk(
        {
            Header = function(hdr)
                if env_title == "" then
                    env_title = hdr.content
                    return {}
                else
                    return pandoc.Plain({
                        pandoc.RawInline('latex', '\\subheader{'),
                        hdr.content,
                        pandoc.RawInline('latex', '}')
                    })
                end
            end
        }
    )

    return {
        pandoc.RawInline('latex', '\\begin{' .. env_name .. '}{'),
        env_title,
        pandoc.RawInline('latex', '}'),
        elem,
        pandoc.RawInline('latex', '\\end{' .. env_name .. '}'),
    }
end

-----------------------------------------------------------------
-- Tabelas
-----------------------------------------------------------------

ALIGNS = {
    ["AlignDefault"] = "l",
    ["AlignLeft"]    = "l",
    ["AlignCenter"]  = "c",
    ["AlignRight"]   = "r",
}


local function tableAlignment(colspecs)
    local table_alignment = {}
    for i, align in ipairs(colspecs) do
        table.insert(table_alignment, ALIGNS[align[1]])
    end
    return table.concat(table_alignment)
end


local function tableRow(row)
    local table_row = {}
    local cells = row.cells

    for i, cell in ipairs(cells) do
        -- Concatena `table_head` e `cell.content`
        for _, block in ipairs(cell.content) do
            table.insert(table_row, block.content[1])
        end
        if i < #cells then
            table.insert(table_row, pandoc.RawInline("latex", " & "))
        end
    end

    return table_row
end


local function tableHead(head)
    return tableRow(head.rows[1])
end


function Table(tbl)
    if tbl.caption ~= nil then
        Caption = tbl.caption
    end

    local buffer = {}
    table.insert(buffer, pandoc.RawInline("latex", "\\toprule"))
    table.insert(buffer, tableHead(tbl.head))
    table.insert(buffer, pandoc.RawInline("latex", "\\midrule"))
    table.insert(buffer, pandoc.RawInline("latex", "\\bottomrule"))
    table.insert(buffer, pandoc.RawInline("latex", "\\end{tabular}"))

    return {
        pandoc.RawInline("latex",
            "\\begin{tabular}{" .. tableAlignment(tbl.colspecs) .. "}"),
        pandoc.LineBlock(buffer)
    }
end

-----------------------------------------------------------------

return {
    Div = Div,
    Table = Table
}
