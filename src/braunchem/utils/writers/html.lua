-----------------------------------------------------------------
-- html.lua
--
-- Gabriel Braun, 2023
-----------------------------------------------------------------

-----------------------------------------------------------------
-- Containers
-----------------------------------------------------------------


function Div(elem)
    local env_name = elem.classes[1]
    local env_title = ""
    local header_env_index = 0

    elem.content = elem.content:walk(
        {
            Header = function(hdr)
                local header_text = pandoc.utils.stringify(hdr) -- mudar!
                if env_title == "" then
                    env_title = header_text
                    return {}
                else
                    local header_env_name = env_name .. '-subheader'
                    header_env_index = header_env_index + 1
                    return pandoc.RawInline('html',
                        '<' .. header_env_name ..
                        ' index="' .. header_env_index .. '"' ..
                        '>' ..
                        header_text ..
                        '</' .. header_env_name .. '>'
                    )
                end
            end
        }
    )

    return {
        pandoc.RawInline('html',
            '<' .. env_name ..
            ' title="' .. env_title .. '"' ..
            '>'
        ),
        elem,
        pandoc.RawInline('html',
            '</' .. env_name .. '>'
        ),
    }
end

-----------------------------------------------------------------
-- Tabelas
-----------------------------------------------------------------

function Table(tbl)
    if tbl.caption ~= nil then
        -- Tabela com legenda
        local caption = tbl.caption
        return {
            pandoc.RawInline('html',
                '<display-table' ..
                -- ' title="' .. tbl.caption .. '"' ..
                '>'
            ),
            tbl,
            pandoc.RawInline('html',
                '</display-table>'
            ),
        }
    end
    return tbl
end

-----------------------------------------------------------------

return {
    Div = Div,
    Table = Table
}
