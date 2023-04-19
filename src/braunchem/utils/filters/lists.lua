local choices = nil
local correct_choice = nil

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
    if FORMAT:match 'latex' then
        decompactifyList(elem)
    end
    return elem
end

function BulletList(elem)
    if FORMAT:match 'problem' then
        local frist_tag = pandoc.utils.stringify(elem.content[1][1].content[1])
        if frist_tag == "☒" or frist_tag == "☐" then
            choices = {}
            for i, block in ipairs(elem.content) do
                local tag = pandoc.utils.stringify(table.remove(block[1].content, 1))
                if tag == "☒" then
                    correct_choice = i - 1
                end
                table.insert(choices, block)
            end
            return {}
        else
            decompactifyList(elem)
            return elem
        end
    end
end

function Meta(metadata)
    metadata.choices = choices
    metadata.correct_choice = correct_choice
    metadata.date = os.date("!%Y-%m-%dT%T")
    return metadata
end
