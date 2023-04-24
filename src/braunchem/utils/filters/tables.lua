if FORMAT:match 'latex' then
    function Table(elem)
        return pandoc.Str("olá")
    end
end
