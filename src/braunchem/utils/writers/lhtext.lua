-----------------------------------------------------------------
-- text.lua
--
-- Gabriel Braun, 2023
-----------------------------------------------------------------
-----------------------------------------------------------------
-- Configurações HTML
-----------------------------------------------------------------

local html_filters = require "src.braunchem.utils.writers.html.html"

local HTML_OPTS = {
    wrap_text = "none",
    html_math_method = "katex"
}

local HTML_FILTERS = html_filters

local HTML_SIMPLE_FILTERS = html_filters

-----------------------------------------------------------------
-- Configurações LaTeX
-----------------------------------------------------------------

local latex_div = require "latex.latex_div"
local latex_image = require "latex.latex_image"
local latex_link = require "latex.latex_link"
local latex_span = require "latex.latex_span"
local latex_table = require "latex.latex_table"

local LATEX_OPTS = {
    wrap_text = "none",
}

local LATEX_SIMPLE_FILTERS = {
    Table = latex_table
}

local LATEX_FILTERS = {
    traverse = 'topdown',
    Div = latex_div,
    Image = latex_image,
    Link = latex_link,
    Span = latex_span,
    Table = latex_table
}

-----------------------------------------------------------------
-- Texto simples
-----------------------------------------------------------------

local function simple(block)
    --
    -- Converte um pandoc.Block em latex e html simples.
    --
    local doc = pandoc.Pandoc(block)

    return {
        html = pandoc.write(
            doc:walk(HTML_SIMPLE_FILTERS), 'html', HTML_OPTS
        ),
        latex = pandoc.write(
            doc:walk(LATEX_SIMPLE_FILTERS), 'latex', LATEX_OPTS
        ),
    }
end

-----------------------------------------------------------------
-- Texto para seções
-----------------------------------------------------------------

local function section(block)
    --
    -- Converte um pandoc.Block em latex e html para seções.
    --
    local doc = pandoc.Pandoc(block)

    return {
        html = pandoc.write(
            doc:walk(HTML_FILTERS), 'html', HTML_OPTS
        ),
        latex = pandoc.write(
            doc:walk(LATEX_FILTERS), 'latex', LATEX_OPTS
        ),
    }
end

-----------------------------------------------------------------
-- Export
-----------------------------------------------------------------

return {
    simple = simple,
    section = section
}
