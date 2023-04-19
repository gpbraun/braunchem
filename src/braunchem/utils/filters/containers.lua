if FORMAT:match 'latex' then
    local gettitle = {
        Header = function(elem)
            local text = pandoc.utils.stringify(elem)
            if Title == "" then
                Title = text
                return {}
            else
                return pandoc.RawInline('latex', '\\subheader{' .. text .. '}')
            end
        end
    }

    function Div(elem)
        local class = elem.classes[1]

        Title = ""
        elem.content = elem.content:walk(gettitle)

        return {
            pandoc.RawInline('latex', '\\begin{' .. class .. '}{' .. Title .. '}'),
            elem,
            pandoc.RawInline('latex', '\\end{' .. class .. '}'),
        }
    end
end
