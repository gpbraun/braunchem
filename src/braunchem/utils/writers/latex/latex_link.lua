-----------------------------------------------------------------
-- latex_ref.lua
--
-- Gabriel Braun, 2023
-----------------------------------------------------------------

local latex = require("latex.latex")


local function startsWith(str, start)
    return str:sub(1, #start) == start
end

local function Link(link)
    --
    -- Referências cruzadas.
    --
    local latex_target = string.sub(link.target, 2)

    if startsWith(link.target, "#tbl") then
        return latex.inline("\\tblref{" .. latex_target .. "}")
    end
    if startsWith(link.target, "#eq") then
        return latex.inline("\\eqref{" .. latex_target .. "}")
    end
    if startsWith(link.target, "#sec") then
        return latex.inline("\\secref{" .. latex_target .. "}")
    end
    if startsWith(link.target, "#fig") then
        return latex.inline("\\figref{" .. latex_target .. "}")
    end

    return link
end

-----------------------------------------------------------------
-- Export
-----------------------------------------------------------------

return Link
