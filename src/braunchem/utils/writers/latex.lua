-----------------------------------------------------------------
-- latex.lua
--
-- Gabriel Braun, 2023
-----------------------------------------------------------------

local function latex(text)
    return pandoc.RawInline('latex', text)
end


local function block_latex(text)
    return pandoc.RawBlock('latex', text)
end


local function surround(inlines, begin_str, end_str)
    table.insert(inlines, 1, latex(begin_str))
    table.insert(inlines, latex(end_str))
end

-----------------------------------------------------------------
-- Containers
-----------------------------------------------------------------

function Div(div)
    if div.classes == nil then
        return div
    end

    local env_name = div.classes[1]
    local env_title = {}

    div.content = div.content:walk {
        Header = function(hdr)
            if #env_title == 0 then
                env_title = hdr.content
                return {}
            else
                local env_subtitle = hdr.content
                surround(env_subtitle, '\\subheader{', '}')
                return pandoc.Plain(env_subtitle)
            end
        end
    }

    local env_header = env_title
    surround(env_header, '\\begin{' .. env_name .. '}{', '}')

    return pandoc.Div {
        pandoc.Plain(env_header),
        div,
        block_latex('\\end{' .. env_name .. '}'),
    }
end

-----------------------------------------------------------------
-- Tabelas
-----------------------------------------------------------------

local ALIGNS = {
    ["AlignDefault"] = "l",
    ["AlignLeft"]    = "l",
    ["AlignCenter"]  = "c",
    ["AlignRight"]   = "r",
}


local function tabularAlignment(colspecs)
    local table_alignment = {}
    for _, align in ipairs(colspecs) do
        table.insert(table_alignment, ALIGNS[align[1]])
    end
    return table.concat(table_alignment)
end


local function tabularRow(row)
    local tbl_row = {}
    local cells = row.cells

    for i, cell in ipairs(cells) do
        -- Concatena `table_row` e `cell.content`
        -- for _, block in ipairs(cell.content)
        -- table.insert(tbl_row, cell)
        -- end
        if i < #cells then
            table.insert(tbl_row, latex " & ")
        end
    end

    return tbl_row
end


local function tabularHead(head)
    return {
        tabularRow(head.rows[1]),
    }
end


local function tabularBody(tbl)
    return {
        latex('\\begin{tabular}{' .. tabularAlignment(tbl.colspecs) .. '}'),
        latex '\\toprule',
        tabularHead(tbl.head),
        latex '\\midrule',
        latex '\\bottomrule',
        latex '\\end{tabular}'
    }
end


local function tabular(tbl)
    return tabularBody(tbl)
end


function Table(tbl)
    if tbl.caption ~= nil then
        local env_header = pandoc.utils.blocks_to_inlines(tbl.caption.long)
        surround(env_header, '\\begin{displaytable}{', '}')

        return tabularHead(tbl.head)
        -- return pandoc.Div {
        --     pandoc.Plain(env_header),
        --     tabular(tbl),
        --     block_latex '\\end{displaytable}'
        -- }
    end
end

-----------------------------------------------------------------
-- Filtro
-----------------------------------------------------------------

return {
    Div = Div,
    Table = Table
}
