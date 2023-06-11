-----------------------------------------------------------------
-- problem.lua
--
-- Gabriel Braun, 2023
-----------------------------------------------------------------

local math = require "math"

local html_filters = require "src.braunchem.utils.writers.html"
local latex_filters = require "src.braunchem.utils.writers.latex"

local text = function(block)
    -- Converte um pandoc.Block em latex e html
    local doc = pandoc.Pandoc(block)
    local html_opts = {
        wrap_text = "none",
        html_math_method = "katex"
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
-- Geração automática de alternativas
-----------------------------------------------------------------


local choices
local correct_choice = 0


local function addChoice(choice)
    -- Adiciona uma alternativa na lista global.
    table.insert(choices, choice)
end


-----------------------------------------------------------------
-- Geração automática de alternativas numéricas
-----------------------------------------------------------------


local function formatValue(value)
    -- Converte um valor em uma string com formatação correta.
    local prec_value = string.format("%.2g", value)

    if math.abs(value) < 1e-3 or math.abs(value) > 1e4 then
        -- notação exponencial
        return string.format("%.1E", prec_value):gsub("E%+?0?(%d+)", "E%1"):gsub("%.", ",")
    end
    -- notação decimal
    return string.format("%.4f", prec_value):gsub("%.?0+$", ""):gsub("%.", ",")
end


local function autoNumChoices(math_text)
    -- Cria distratores a partir de uma alternativa numérica.
    local _, _, correct_value_str = string.find(math_text, "(%d+[%.%,]?%d*[eE]?[+-]?%d*)")
    local correct_value = tonumber(tostring(string.gsub(correct_value_str, ",", ".")))

    local function addNumChoice(value)
        -- Cria uma alternativa numérica a partir de seu valor.
        local choice_value_str = formatValue(value)
        local math_choice_text = string.gsub(math_text, correct_value_str, choice_value_str)
        addChoice(text(pandoc.Plain(pandoc.Math("InlineMath", math_choice_text))))
    end

    ---@diagnostic disable-next-line: param-type-mismatch
    local scale = 1 + (math.abs(math.log(correct_value, 10)) + 1) / 5
    for i = 1, 5 do
        local value = correct_value * scale ^ (i - correct_choice)
        addNumChoice(value)
    end
end


-----------------------------------------------------------------
-- Geração de alternativas de V ou F
-----------------------------------------------------------------


local PROP_CHOICES_MAP = {
    [""] = {
        {},
        { 1 },
        { 2 },
        { 3 },
        { 4 }
    },
    ["1"] = {
        { 1 },
        { 2 },
        { 1, 2 },
        { 1, 3 },
        { 1, 4 }
    },
    ["2"] = {
        { 1 },
        { 2 },
        { 1, 2 },
        { 2, 3 },
        { 2, 4 }
    },
    ["3"] = {
        { 3 },
        { 4 },
        { 1, 3 },
        { 2, 3 },
        { 3, 4 }
    },
    ["4"] = {
        { 3 },
        { 4 },
        { 1, 4 },
        { 2, 4 },
        { 3, 4 }
    },
    ["1,2"] = {
        { 1 },
        { 2 },
        { 1, 2 },
        { 1, 2, 3 },
        { 1, 2, 4 }
    },
    ["1,3"] = {
        { 1 },
        { 3 },
        { 1, 3 },
        { 1, 2, 3 },
        { 1, 3, 4 }
    },
    ["1,4"] = {
        { 1 },
        { 4 },
        { 1, 4 },
        { 1, 2, 4 },
        { 1, 3, 4 }
    },
    ["2,3"] = {
        { 2 },
        { 3 },
        { 2, 3 },
        { 1, 2, 3 },
        { 2, 3, 4 }
    },
    ["3,4"] = {
        { 3 },
        { 4 },
        { 3, 4 },
        { 1, 3, 4 },
        { 2, 3, 4 }
    },
    ["1,2,3"] = {
        { 1, 2 },
        { 1, 3 },
        { 2, 3 },
        { 1, 2, 3 },
        { 1, 2, 3, 4 }
    },
    ["1,2,4"] = {
        { 1, 2 },
        { 1, 4 },
        { 2, 4 },
        { 1, 2, 4 },
        { 1, 2, 3, 4 }
    },
    ["1,3,4"] = {
        { 1, 3 },
        { 1, 4 },
        { 3, 4 },
        { 1, 3, 4 },
        { 1, 2, 3, 4 }
    },
    ["2,3,4"] = {
        { 2, 3 },
        { 2, 4 },
        { 3, 4 },
        { 2, 3, 4 },
        { 1, 2, 3, 4 }
    },
    ["1,2,3,4"] = {
        { 1, 2, 3 },
        { 1, 2, 4 },
        { 1, 3, 4 },
        { 2, 3, 4 },
        { 1, 2, 3, 4 }
    }
}


local function addPropChoice(prop_choice_nums)
    -- Cria uma alternativa para proposições.
    local prop_choice = {}
    if #prop_choice_nums == 0 then
        table.insert(prop_choice, pandoc.Str("NDA"))
    else
        for i, prop_num in ipairs(prop_choice_nums) do
            table.insert(prop_choice, pandoc.Strong(tostring(prop_num)))
            if i < #prop_choice_nums - 1 then
                -- separator do meio
                table.insert(prop_choice, pandoc.Str(","))
                table.insert(prop_choice, pandoc.Space())
            elseif i == #prop_choice_nums - 1 then
                -- último separador
                table.insert(prop_choice, pandoc.Space())
                table.insert(prop_choice, pandoc.Str("e"))
                table.insert(prop_choice, pandoc.Space())
            end
        end
    end
    addChoice(text(pandoc.Plain(prop_choice)))
end


local function autoPropChoices(elem)
    -- Cria distratores para um problema de avaliação de proposições.
    choices = {}

    local correct_props = {}
    for i, choice in ipairs(elem.content) do
        local checkbox = choice[1].content:remove(1).text
        if checkbox == "☒" then
            table.insert(correct_props, i)
        end
        -- Remove o primeiro espaço
        choice[1].content:remove(1)
    end

    -- adiciona as cinco alternativas na lista
    local correct_props_str = table.concat(correct_props, ",")
    for i, prop_choice_nums in ipairs(PROP_CHOICES_MAP[correct_props_str]) do
        addPropChoice(prop_choice_nums)
        -- procura a alternativa correta
        if table.concat(prop_choice_nums, ",") == correct_props_str then
            correct_choice = i
        end
    end
end

-----------------------------------------------------------------
-- Geração automática de alternativas de ordenação
-----------------------------------------------------------------


local ORDER_CHOICES_MAP = {
    [3] = {
        { 1, 3, 2 },
        { 2, 1, 3 },
        { 2, 3, 1 },
        { 3, 1, 2 }
    },
    [4] = {
        { 1, 2, 4, 3 },
        { 1, 4, 2, 3 },
        { 2, 3, 1, 4 },
        { 2, 4, 3, 1 }
    },
    [5] = {
        { 1, 2, 3, 5, 4 },
        { 1, 4, 5, 2, 3 },
        { 2, 3, 4, 1, 5 },
        { 2, 5, 4, 3, 1 }
    },
    [6] = {
        { 1, 2, 4, 3, 5, 6 },
        { 1, 5, 4, 2, 3, 6 },
        { 2, 3, 5, 6, 4, 1 },
        { 2, 6, 5, 4, 3, 1 }
    },
}


local function trimBlockContentSpaces(content)
    -- Remove espaços em volta de um bloco.
    if content[1].tag == "Space" then
        table.remove(content, 1)
    end
    if content[#content].tag == "Space" then
        table.remove(content, #content)
    end
end


local function autoOrderChoices(choice_content)
    -- Cria distratores a partir de uma alternativa numérica.
    local items = {}
    local separator = nil

    local item = {}
    for _, block in ipairs(choice_content) do
        local block_str = block.text

        if block_str == ";" or block_str == ">" or block_str == "<" then
            separator = block_str
            trimBlockContentSpaces(item)
            table.insert(items, item)
            addChoice(item)
            item = {}
        else
            table.insert(item, block)
        end
    end
    trimBlockContentSpaces(item)
    table.insert(items, item)
    addChoice(item)

    local function addOrderChoice(order_choice_nums)
        local order_choice = {}
        for i, order_choice_num in ipairs(order_choice_nums) do
            -- Concatena `order_choice` e `items[order_choice_num]`
            for _, block in ipairs(items[order_choice_num]) do
                table.insert(order_choice, block)
            end
            if i < #order_choice_nums then
                table.insert(order_choice, pandoc.Space())
                table.insert(order_choice, pandoc.Str(separator))
                table.insert(order_choice, pandoc.Space())
            end
        end
        addChoice(pandoc.Plain(order_choice))
    end

    for _, order_choice_nums in ipairs(ORDER_CHOICES_MAP[#items]) do
        addOrderChoice(order_choice_nums)
    end
end


-----------------------------------------------------------------
-- Listas dos problemas
-----------------------------------------------------------------


local function autoChoices(choice)
    -- Gera distratores a partir de uma alternativa correta.
    if #choice ~= 1 then
        return
    end

    choices = {}
    local choice_content = choice[1].content

    correct_choice = math.random(1, 5)

    -- alternativa consiste apenas de uma equação
    if #choice_content == 1 and choice_content[1].tag == "Math" then
        -- gerar alternativas numéricas.
        autoNumChoices(choice_content[1].text)
        return
    end
    -- gerar alternativas de ordenação
    autoOrderChoices(choice_content)
end


local function taskBulletList(elem)
    -- Problema objetivo com alternativas.
    choices = {}

    for i, choice in ipairs(elem.content) do
        local checkbox = choice[1].content:remove(1).text
        if checkbox == "☒" then
            correct_choice = i
        end
        -- Remove o primeiro espaço
        choice[1].content:remove(1)
        addChoice(choice)
    end

    if #choices == 1 then
        -- problema com apenas uma alternativa (gerar as alternativas)
        autoChoices(choices[1])
    end
end


local function decompactifyItem(blocks)
    for i, bolck in ipairs(blocks) do
        if bolck.tag == 'Plain' then
            blocks[i] = pandoc.Para(bolck.content)
        end
    end
    return blocks
end


local function decompactifyList(elem)
    elem.content = elem.content:map(decompactifyItem)
end


local problemLists = {
    OrderedList = function(elem)
        local frist = elem.content[1][1].content[1].text
        if frist == "☒" or frist == "☐" then
            autoPropChoices(elem)
        end

        decompactifyList(elem)
        return elem
    end,
    BulletList = function(elem)
        local frist = elem.content[1][1].content[1].text
        if frist == "☒" or frist == "☐" then
            taskBulletList(elem)
            -- remove a lista do enunciado
            return {}
        end

        decompactifyList(elem)
        return elem
    end
}


-----------------------------------------------------------------
-- Writer
-----------------------------------------------------------------


function Writer(doc, opts)
    -- Tratamento das listas
    if doc.meta.seed ~= nil then
        math.randomseed(doc.meta.seed)
    end
    doc = doc:walk(problemLists)

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
        _id            = doc.meta.id,
        date           = os.date("!%Y-%m-%dT%T"),
        choices        = choices,
        correct_choice = correct_choice - 1,
        statement      = text(statement),
        solution       = text(solution),
    }
    return pandoc.json.encode(problem_data)
end
