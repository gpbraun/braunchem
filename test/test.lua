GeneratePermutations = function(n, items)
    -- Usa o algorítimo de Heap para gerar permutações da lista.
    if n == 0 then
        print(table.concat(items, ","))
        -- addChoice(items)
    else
        for i = 1, n do
            GeneratePermutations(n - 1, items)
            local swapIndex = n % 2 == 0 and i or 1
            items[swapIndex], items[n] = items[n], items[swapIndex]
        end
    end
end

local t = { 1, 2, 3, 4 }
print(t)
GeneratePermutations(3, t)
