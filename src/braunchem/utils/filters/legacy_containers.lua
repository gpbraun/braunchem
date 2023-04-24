if FORMAT:match 'latex' then
    function Div(elem)
        local class = elem.classes[1]
        return {
            pandoc.RawInline('latex', '\\begin{' .. class .. '}'),
            elem,
            pandoc.RawInline('latex', '\\end{' .. class .. '}'),
        }
    end
end
