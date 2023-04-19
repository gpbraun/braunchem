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

-- Converte um Pandoc em latex e html
local text = function(doc, opts)
    return {
        html  = pandoc.write(doc, 'html', opts),
        latex = pandoc.write(doc:walk(latex_filters), 'latex', opts),
    }
end

function Writer(doc, opts)
    -- Converte as alternativas
    local choices = {}
    for _, block in ipairs(doc.meta.choices) do
        local choice_doc = pandoc.Pandoc(block)
        table.insert(choices, text(choice_doc, opts))
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
    local statement_doc = pandoc.Pandoc(statement)
    local solution_doc  = pandoc.Pandoc(solution)

    local problem_data  = {
        -- teste = doc.blocks,
        choices = choices,
        date = doc.meta.date,
        correct_choice = doc.meta.correct_choice,
        statement = text(statement_doc, opts),
        solution = text(solution_doc, opts)
    }
    return pandoc.json.encode(problem_data)
end
