-----------------------------------------------------------------
-- latex.lua
--
-- Gabriel Braun, 2023
-----------------------------------------------------------------

local latex = require("latex.latex")


local function Div(div)
    --
    -- Containers.
    --
    local identifier
    if div.identifier ~= nil then
        identifier = div.identifier
        div.content[1].identifier = identifier
        div.identifier = ""
    end

    if div.classes[1] == nil then
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
                latex.surround(env_subtitle, '\\step{', '}')
                return pandoc.Plain(env_subtitle)
            end
        end
    }

    return latex.env(env_name, env_title, div)
end

-----------------------------------------------------------------
-- Export
-----------------------------------------------------------------

return Div
