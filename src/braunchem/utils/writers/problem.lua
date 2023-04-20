local gettitle = {
    Header = function(elem)
        local text = pandoc.utils.stringify(elem)
        if EnvTitle == "" then
            EnvTitle = text
            return {}
        else
            return pandoc.RawInline('latex', '\\subheader{' .. text .. '}')
        end
    end
}

local latex_filters = {
    Div = function(elem)
        local env_name = elem.classes[1]

        EnvTitle = ""
        elem.content = elem.content:walk(gettitle)

        return {
            pandoc.RawInline('latex', '\\begin{' .. env_name .. '}{' .. EnvTitle .. '}'),
            elem,
            pandoc.RawInline('latex', '\\end{' .. env_name .. '}'),
        }
    end
}

-- Converte um pandoc.Block em latex e html
local text = function(block, opts)
    local doc = pandoc.Pandoc(block)
    return {
        html  = pandoc.write(doc, 'html', opts),
        latex = pandoc.write(doc:walk(latex_filters), 'latex', opts),
    }
end

function Writer(doc, opts)
    -- Converte as alternativas
    local choices = nil
    local correct_choice = nil
    if doc.meta.choices ~= nil then
        choices = {}
        for _, block in ipairs(doc.meta.choices) do
            table.insert(choices, text(block, opts))
        end
        correct_choice = doc.meta.correct_choice
    end

    -- Separa o enunciado da solução.
    local in_solution = false
    local solution = {}
    local statement = {}

    for _, block in ipairs(doc.blocks) do
        if block.t == "HorizontalRule" then
            in_solution = true
        elseif in_solution == true then
            table.insert(solution, block)
        else
            table.insert(statement, block)
        end
    end

    local problem_data = {
        -- teste          = doc.meta.choices,
        date           = doc.meta.date,
        choices        = choices,
        correct_choice = correct_choice,
        statement      = text(statement, opts),
        solution       = text(solution, opts)
    }
    return pandoc.json.encode(problem_data)
end
