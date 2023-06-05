local gettitle = {
    Header = function(elem)
        local header_text = pandoc.utils.stringify(elem) -- mudar!
        if EnvTitle == "" then
            EnvTitle = header_text
            return {}
        else
            local header_env_name = EnvName .. '-subheader'
            Header_env_index = Header_env_index + 1
            return pandoc.RawInline('html',
                '<' .. header_env_name ..
                ' index="' .. Header_env_index .. '"' ..
                '>' ..
                header_text ..
                '</' .. header_env_name .. '>'
            )
        end
    end
}

Filters = {
    Div = function(elem)
        EnvName = elem.classes[1]

        EnvTitle = ""
        Header_env_index = 0

        elem.content = elem.content:walk(gettitle)

        return {
            pandoc.RawInline('html',
                '<' .. EnvName ..
                ' title="' .. EnvTitle .. '"' ..
                '>'
            ),
            elem,
            pandoc.RawInline('html',
                '</' .. EnvName .. '>'
            ),
        }
    end,
}

return Filters
