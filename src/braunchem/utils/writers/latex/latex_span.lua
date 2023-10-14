-----------------------------------------------------------------
-- latex_span.lua
--
-- Gabriel Braun, 2023
-----------------------------------------------------------------

function Span(span)
    --
    -- Referências em equações.
    --
    local child = span.content[1]

    if span.identifier ~= "" and child.tag == "Math" then
        if child.mathtype == "DisplayMath" then
            local eq_label = "\\eqlabel{" .. span.identifier .. "}"
            child.text = eq_label .. child.text
            return child
        end
    end

    return child
end

-----------------------------------------------------------------
-- Export
-----------------------------------------------------------------

return Span
