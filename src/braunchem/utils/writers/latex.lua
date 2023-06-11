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


local function tabularRow(row, bold)
    local tbl_row = {}
    local cells = row.cells

    for i, cell in ipairs(cells) do
        local cell_content = pandoc.utils.blocks_to_inlines(cell.contents)
        if bold == true then
            table.insert(tbl_row, pandoc.Strong(cell_content))
        else
            table.insert(tbl_row, pandoc.Span(cell_content))
        end
        if i < #cells then
            table.insert(tbl_row, latex " & ")
        end
    end

    return tbl_row
end


local function tabularHead(head)
    return tabularRow(head.rows[1], true)
end


local function tabularBody(body)
    local tbl_body = {}

    for _, row in ipairs(body.body) do
        table.insert(tbl_body, tabularRow(row))
    end

    return pandoc.LineBlock(tbl_body)
end


function Table(tbl)
    if #tbl.caption.long > 0 then
        -- Tabela com legenda: displaytable
        local env_header = pandoc.utils.blocks_to_inlines(tbl.caption.long)
        surround(env_header, '\\begin{displaytable}{', '}')

        return {
            env_header,
            latex('\\begin{tabular}{' .. tabularAlignment(tbl.colspecs) .. '}'),
            tabularHead(tbl.head),
            latex '\\\\ \\midrule',
            tabularBody(tbl.bodies[1]),
            latex '\\end{tabular}',
            block_latex('\\end{displaytable}'),
        }
    end

    -- Tabela normal
    return pandoc.Div {
        block_latex('\\begin{center}'),
        latex('\\begin{tabular}{' .. tabularAlignment(tbl.colspecs) .. '}'),
        latex '\\toprule',
        tabularHead(tbl.head),
        latex '\\\\ \\midrule',
        tabularBody(tbl.bodies[1]),
        latex '\\\\ \\bottomrule',
        latex '\\end{tabular}',
        block_latex('\\end{center}'),
    }
end

-----------------------------------------------------------------
-- Figuras
-----------------------------------------------------------------

-- function Figure(fig)
--     return {
--         latex(fig.attr.identifier),
--         fig,
--     }
-- end

-----------------------------------------------------------------
-- Filtro
-----------------------------------------------------------------

return {
    Table = Table,
    -- Div = Div,
}
