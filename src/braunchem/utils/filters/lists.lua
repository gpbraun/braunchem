local choices = nil
local correct_choice = nil


local taskOrderedList = function(elem)
    -- Problema objetivo com proposições (sempre gera as alternativas).
    choices = {}
    local prop_choice_map = {
        [""] = { {}, { 1 }, { 2 }, { 3 }, { 4 } },
        ["1"] = { { 1 }, { 2 }, { 1, 2 }, { 1, 3 }, { 1, 4 } },
        ["2"] = { { 1 }, { 2 }, { 1, 2 }, { 2, 3 }, { 2, 4 } },
        ["3"] = { { 3 }, { 4 }, { 1, 3 }, { 2, 3 }, { 3, 4 } },
        ["4"] = { { 3 }, { 4 }, { 1, 4 }, { 2, 4 }, { 3, 4 } },
        ["1,2"] = { { 1 }, { 2 }, { 1, 2 }, { 1, 2, 3 }, { 1, 2, 4 } },
        ["1,3"] = { { 1 }, { 3 }, { 1, 3 }, { 1, 2, 3 }, { 1, 3, 4 } },
        ["1,4"] = { { 1 }, { 4 }, { 1, 4 }, { 1, 2, 4 }, { 1, 3, 4 } },
        ["2,3"] = { { 2 }, { 3 }, { 2, 3 }, { 1, 2, 3 }, { 2, 3, 4 } },
        ["3,4"] = { { 3 }, { 4 }, { 3, 4 }, { 1, 3, 4 }, { 2, 3, 4 } },
        ["1,2,3"] = { { 1, 2 }, { 1, 3 }, { 2, 3 }, { 1, 2, 3 }, { 1, 2, 3, 4 } },
        ["1,2,4"] = { { 1, 2 }, { 1, 4 }, { 2, 4 }, { 1, 2, 4 }, { 1, 2, 3, 4 } },
        ["1,3,4"] = { { 1, 3 }, { 1, 4 }, { 3, 4 }, { 1, 3, 4 }, { 1, 2, 3, 4 } },
        ["2,3,4"] = { { 2, 3 }, { 2, 4 }, { 3, 4 }, { 2, 3, 4 }, { 1, 2, 3, 4 } },
        ["1,2,3,4"] = { { 1, 2, 3 }, { 1, 2, 4 }, { 1, 3, 4 }, { 2, 3, 4 }, { 1, 2, 3, 4 } }
    }

    local propChoice = function(prop_choice_nums)
        -- Cria uma alternativa.
        if #prop_choice_nums == 0 then
            return pandoc.Plain("NDA")
        end
        local prop_choice = {}
        for i, prop_num in ipairs(prop_choice_nums) do
            table.insert(prop_choice, pandoc.Strong(tostring(prop_num)))
            if i < #prop_choice_nums - 1 then
                table.insert(prop_choice, pandoc.Str(", "))
            elseif i == #prop_choice_nums - 1 then
                table.insert(prop_choice, pandoc.Str(" e "))
            end
        end
        return pandoc.Plain(prop_choice)
    end

    local correct_props = {}
    for i, block in ipairs(elem.content) do
        local tag = pandoc.utils.stringify(table.remove(block[1].content, 1))
        if tag == "☒" then
            table.insert(correct_props, i)
        end
    end

    -- Adiciona as cinco alternativas na lista.
    local correct_props_str = table.concat(correct_props, ",")
    for i, prop_choice_nums in ipairs(prop_choice_map[correct_props_str]) do
        table.insert(choices, propChoice(prop_choice_nums))
        -- Procura a alternativa correta.
        if table.concat(prop_choice_nums, ",") == correct_props_str then
            correct_choice = i - 1
        end
    end
end


local autoNumChoices = function(choice)
    -- Cria distratores a partir de uma alternativa numérica.
    return
end


local taskBulletList = function(elem)
    -- problema objetivo com alternativas.
    choices = {}
    for i, block in ipairs(elem.content) do
        local tag = pandoc.utils.stringify(table.remove(block[1].content, 1))
        if tag == "☒" then
            correct_choice = i - 1
        end
        table.insert(choices, block)
    end
    if #choices == 1 then
        -- problema com apenas uma alternativa (gerar as alternativas).

        table.insert(choices, choices[1])
        table.insert(choices, choices[1])
        table.insert(choices, choices[1])
        table.insert(choices, choices[1])
    end
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
    local frist_tag = pandoc.utils.stringify(elem.content[1][1].content[1])
    if frist_tag == "☒" or frist_tag == "☐" then
        taskOrderedList(elem)
        return {}
    end

    decompactifyList(elem)
    return elem
end

function BulletList(elem)
    local frist_tag = pandoc.utils.stringify(elem.content[1][1].content[1])
    if frist_tag == "☒" or frist_tag == "☐" then
        taskBulletList(elem)
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
