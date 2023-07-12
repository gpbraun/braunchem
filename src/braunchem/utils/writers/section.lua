-----------------------------------------------------------------
-- section.lua
--
-- Gabriel Braun, 2023
-----------------------------------------------------------------


local html_filters = require "src.braunchem.utils.writers.html"
local latex_filters = require "src.braunchem.utils.writers.latex"

local text = function(block)
    -- Converte um pandoc.Block em latex e html
    local doc = pandoc.Pandoc(block)
    local html_opts = {
        wrap_text = "none",
        html_math_method = "katex",
    }
    local latex_opts = {
        wrap_text = "none",
    }
    return {
        html = pandoc.write(doc:walk(html_filters), 'html', html_opts),
        latex = pandoc.write(doc:walk(latex_filters), 'latex', latex_opts),
    }
end


-----------------------------------------------------------------
-- Writer
-----------------------------------------------------------------


function Writer(doc, opts)
    local section_data = {
        _id     = doc.meta.id,
        date    = os.date("!%Y-%m-%dT%T"),
        content = text(doc.blocks)
    }
    return pandoc.json.encode(section_data)
end
