local math = require "math"

local choices = nil
local correct_choice = nil


local addChoice = function(choice)
    -- Adiciona uma alternativa na lista global.
    table.insert(choices, choice)
end


local addPropChoice = function(prop_choice_nums)
    -- Cria uma alternativa para proposições.
    if #prop_choice_nums == 0 then
        return pandoc.Plain("NDA")
    end
    local prop_choice = {}
    for i, prop_num in ipairs(prop_choice_nums) do
        table.insert(prop_choice, pandoc.Strong(tostring(prop_num)))
        if i < #prop_choice_nums - 1 then
            table.insert(prop_choice, pandoc.Str(","))
            table.insert(prop_choice, pandoc.Space())
        elseif i == #prop_choice_nums - 1 then
            table.insert(prop_choice, pandoc.Space())
            table.insert(prop_choice, pandoc.Str("e"))
            table.insert(prop_choice, pandoc.Space())
        end
    end
    addChoice(pandoc.Plain(prop_choice))
end


local autoPropChoices = function(elem)
    -- Cria distratores para um problema de avaliação de proposições.
    choices = {}
    local prop_choice_map = {
        [""]        = { {}, { 1 }, { 2 }, { 3 }, { 4 } },
        ["1"]       = { { 1 }, { 2 }, { 1, 2 }, { 1, 3 }, { 1, 4 } },
        ["2"]       = { { 1 }, { 2 }, { 1, 2 }, { 2, 3 }, { 2, 4 } },
        ["3"]       = { { 3 }, { 4 }, { 1, 3 }, { 2, 3 }, { 3, 4 } },
        ["4"]       = { { 3 }, { 4 }, { 1, 4 }, { 2, 4 }, { 3, 4 } },
        ["1,2"]     = { { 1 }, { 2 }, { 1, 2 }, { 1, 2, 3 }, { 1, 2, 4 } },
        ["1,3"]     = { { 1 }, { 3 }, { 1, 3 }, { 1, 2, 3 }, { 1, 3, 4 } },
        ["1,4"]     = { { 1 }, { 4 }, { 1, 4 }, { 1, 2, 4 }, { 1, 3, 4 } },
        ["2,3"]     = { { 2 }, { 3 }, { 2, 3 }, { 1, 2, 3 }, { 2, 3, 4 } },
        ["3,4"]     = { { 3 }, { 4 }, { 3, 4 }, { 1, 3, 4 }, { 2, 3, 4 } },
        ["1,2,3"]   = { { 1, 2 }, { 1, 3 }, { 2, 3 }, { 1, 2, 3 }, { 1, 2, 3, 4 } },
        ["1,2,4"]   = { { 1, 2 }, { 1, 4 }, { 2, 4 }, { 1, 2, 4 }, { 1, 2, 3, 4 } },
        ["1,3,4"]   = { { 1, 3 }, { 1, 4 }, { 3, 4 }, { 1, 3, 4 }, { 1, 2, 3, 4 } },
        ["2,3,4"]   = { { 2, 3 }, { 2, 4 }, { 3, 4 }, { 2, 3, 4 }, { 1, 2, 3, 4 } },
        ["1,2,3,4"] = { { 1, 2, 3 }, { 1, 2, 4 }, { 1, 3, 4 }, { 2, 3, 4 }, { 1, 2, 3, 4 } }
    }

    local correct_props = {}
    for i, choice in ipairs(elem.content) do
        local checkbox = pandoc.utils.stringify(table.remove(choice[1].content, 1))
        if checkbox == "☒" then
            table.insert(correct_props, i)
        end
        -- Remove o primeiro espaço
        table.remove(choice[1].content, 1)
    end

    -- Adiciona as cinco alternativas na lista
    local correct_props_str = table.concat(correct_props, ",")
    for i, prop_choice_nums in ipairs(prop_choice_map[correct_props_str]) do
        addPropChoice(prop_choice_nums)
        -- Procura a alternativa correta
        if table.concat(prop_choice_nums, ",") == correct_props_str then
            correct_choice = i
        end
    end
end


local formatValue = function(value)
    -- Converte um valor em uma string com formatação correta.
    local prec_value = string.format("%.2g", value)

    if math.abs(value) < 1e-3 or math.abs(value) > 1e4 then
        -- notação exponencial
        return string.format("%.1E", prec_value):gsub("E%+?0?(%d+)", "E%1"):gsub("%.", ",")
    end
    -- notação decimal
    return string.format("%.4f", prec_value):gsub("%.?0+$", ""):gsub("%.", ",")
end


local autoNumChoices = function(math_text)
    -- Cria distratores a partir de uma alternativa numérica.
    choices = {}
    math.randomseed(1234)
    correct_choice = math.random(1, 5)

    local _, _, correct_value_str = string.find(math_text, "(%d+[%.%,]?%d*[eE]?[+-]?%d*)")
    local correct_value = tonumber(tostring(string.gsub(correct_value_str, ",", ".")))

    local addNumChoice = function(value)
        -- Cria uma alternativa numérica a partir de seu valor.
        local math_choice_text = string.gsub(math_text, correct_value_str, formatValue(value))
        addChoice(pandoc.Plain(pandoc.Math("InlineMath", math_choice_text)))
    end

    ---@diagnostic disable-next-line: param-type-mismatch
    local scale = 1 + (math.abs(math.log(correct_value, 10)) + 1) / 5
    for i = 1, 5 do
        local value = correct_value * scale ^ (i - correct_choice)
        addNumChoice(value)
    end
end


local autoChoices = function(choice)
    -- Gera distratores a partir de uma alternativa correta.

    -- alternativa consiste apenas de uma equação
    if #choice[1].content == 1 and choice[1].content[1].tag == "Math" then
        -- gerar alternativas numéricas.
        autoNumChoices(choice[1].content[1].text)
    end
    -- gerar alternativas de ordenação
end


local taskBulletList = function(elem)
    -- Problema objetivo com alternativas.
    choices = {}
    for i, choice in ipairs(elem.content) do
        local checkbox = pandoc.utils.stringify(table.remove(choice[1].content, 1))
        if checkbox == "☒" then
            correct_choice = i
        end
        -- Remove o primeiro espaço
        table.remove(choice[1].content, 1)
        addChoice(choice)
    end
    if #choices > 1 and correct_choice ~= nil then
        -- problema com mais de uma alternativa, sendo uma correta
        return
    end
    -- problema com apenas uma alternativa (gerar as alternativas)
    autoChoices(choices[1])
end


local decompactifyItem = function(blocks)
    for i, blk in ipairs(blocks) do
        if blk.t == 'Plain' then
            blocks[i] = pandoc.Para(blk.content)
        end
    end
    return blocks
end


local decompactifyList = function(elem)
    elem.content = elem.content:map(decompactifyItem)
end


function OrderedList(elem)
    local frist = pandoc.utils.stringify(elem.content[1][1].content[1])
    if frist == "☒" or frist == "☐" then
        autoPropChoices(elem)
    end

    decompactifyList(elem)
    return elem
end

function BulletList(elem)
    local frist = pandoc.utils.stringify(elem.content[1][1].content[1])
    if frist == "☒" or frist == "☐" then
        taskBulletList(elem)
        -- remove a lista do enunciado
        return {}
    end

    decompactifyList(elem)
    return elem
end

function Meta(metadata)
    metadata.date = os.date("!%Y-%m-%dT%T")
    metadata.choices = choices
    metadata.correct_choice = correct_choice
    return metadata
end
