-----------------------------------------------------------------
-- latex_table.lua
--
-- Gabriel Braun, 2023
-----------------------------------------------------------------

local latex = require("latex.latex")

-----------------------------------------------------------------
-- Elementos das tabelas
-----------------------------------------------------------------

local ALIGNS = {
    ["AlignDefault"] = "l",
    ["AlignLeft"]    = "l",
    ["AlignCenter"]  = "c",
    ["AlignRight"]   = "r",
}

local function tblrAlignment(colspecs)
    --
    -- Parâmetros de alinhamento de tabela.
    --
    local tbl_alignment = {}
    for i, colspec in ipairs(colspecs) do
        local cell_align = ALIGNS[colspec[1]]
        local cell_width = 1.0

        if colspec[2] ~= nil then
            cell_width = colspec[2]
        end

        table.insert(tbl_alignment,
            "X[" .. cell_width .. "," .. cell_align .. "]"
        )
    end

    return table.concat(tbl_alignment)
end

local function tblrRow(row)
    --
    -- Linha da tabela.
    --
    local tbl_row = pandoc.List()

    for i, cell in ipairs(row.cells) do
        tbl_row = tbl_row:__concat(cell.contents[1].content)
        if i < #row.cells then
            tbl_row:insert(latex.inline " & ")
        end
    end

    return tbl_row
end

local function tblrBody(head, body, colspecs)
    --
    -- Corpo da tabela.
    --
    local tbl_body = {}

    table.insert(tbl_body, tblrRow(head.rows[1]))
    for _, row in ipairs(body.body) do
        table.insert(tbl_body, tblrRow(row))
    end

    table.insert(tbl_body[1], 1,
        latex.inline('\\begin{tblr}{' .. tblrAlignment(colspecs) .. '}\n')
    )
    table.insert(tbl_body[#tbl_body],
        latex.inline("\n\\end{tblr}")
    )

    return pandoc.LineBlock(tbl_body)
end

-----------------------------------------------------------------
-- Table
-----------------------------------------------------------------

function Table(tbl)
    --
    -- Tabela e tabulado.
    --
    if #tbl.caption.long > 0 then
        -- Tabela com legenda: table
        local tbl_title = pandoc.utils.blocks_to_inlines(tbl.caption.long)
        local tbl_body = tblrBody(tbl.head, tbl.bodies[1], tbl.colspecs)

        if tbl.identifier == nil then
            return latex.env(
                "table", tbl_title, tbl_body
            )
        end

        return latex.env(
            "table", tbl_title, tbl_body, "label=" .. tbl.identifier
        )
    end

    -- tabular simples
    return tblrBody(tbl.head, tbl.bodies[1], tbl.colspecs)
end

-----------------------------------------------------------------
-- Export
-----------------------------------------------------------------

return Table
