if FORMAT:match 'latex' then
    local title

    local gettitle = {
        Header = function(elem)
            local text = elem.content
            if title == nil then
                title = text
                return {}
            else
                return pandoc.RawInline('latex', '\\subheader{' .. text .. '}')
            end
        end
    }

    function Div(elem)
        local class = elem.classes[1]

        title = nil
        elem.content = elem.content:walk(gettitle)

        if title == nil then
            return {
                pandoc.RawInline('latex', '\\begin{' .. class .. '}{}'),
                elem,
                pandoc.RawInline('latex', '\\end{' .. class .. '}'),
            }
        end
        return {
            pandoc.RawInline('latex', '\\begin{' .. class .. '}{' .. title .. '}'),
            elem,
            pandoc.RawInline('latex', '\\end{' .. class .. '}'),
        }
    end
end
