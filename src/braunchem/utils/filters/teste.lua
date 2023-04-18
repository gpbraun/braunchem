if FORMAT:match 'latex' then
  local compactifyItem = function(blocks)
    for i, blk in ipairs(blocks) do
      if blk.t == 'Plain' then
        blocks[i] = pandoc.Para(blk.content)
      end
    end
    return blocks
  end

  local getItems = function(elem)
    local items
    for i, item in ipairs(elem.content) do
      items[i] = pandoc.Para(item.content)
    end
    return items
  end

  local compactifyList = function(elem)
    elem.content = elem.content:map(compactifyItem)
  end

  function BulletList(elem)
    compactifyList(elem)
    return elem
  end

  function OrderedList(elem)
    compactifyList(elem)

    if elem.style == "LowerAlpha" then
      return {
        pandoc.RawInline('latex', '\\begin{tasks}'),
        elem,
        pandoc.RawInline('latex', '\\end{taks}')
      }
    end
  end
end

-- if FORMAT:match 'latex' then
--   function OrderedList (elem)
--     if elem.style == "LowerAlpha" then
--       return {
--         pandoc.RawInline('latex', '\\begin{tasks}'),
--         {table.unpack(elem.contents)},
--         pandoc.RawInline('latex', '\\end{taks}')
--       }
--     else
--       return elem
--     end
--   end
-- end
