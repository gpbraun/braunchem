-----------------------------------------------------------------
-- section.lua
--
-- Gabriel Braun, 2023
-----------------------------------------------------------------

-----------------------------------------------------------------
-- Writer
-----------------------------------------------------------------

function Writer(doc)
    META = doc.meta
    package.path = package.path .. ";" .. META.writerpath .. "/?.lua"

    local text = require "lhtext"

    local section_data = {
        _id     = doc.meta.id,
        date    = os.date("!%Y-%m-%dT%T"),
        content = text.section(doc.blocks),
    }
    return pandoc.json.encode(section_data)
end
