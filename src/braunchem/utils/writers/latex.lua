local gettitle = {
    Header = function(elem)
        local header_text = pandoc.utils.stringify(elem) -- mudar!
        if EnvTitle == "" then
            EnvTitle = header_text
            return {}
        else
            return pandoc.RawInline('latex', '\\subheader{' .. header_text .. '}')
        end
    end
}

Filters = {
    Div = function(elem)
        local env_name = elem.classes[1]

        EnvTitle = ""
        elem.content = elem.content:walk(gettitle)

        return {
            pandoc.RawInline('latex', '\\begin{' .. env_name .. '}{' .. EnvTitle .. '}'),
            elem,
            pandoc.RawInline('latex', '\\end{' .. env_name .. '}'),
        }
    end
}

return Filters
