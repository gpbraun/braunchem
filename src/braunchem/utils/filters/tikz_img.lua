-----------------------------------------------------------------
-- tikz_img.lua
--
-- Gabriel Braun, 2023
-----------------------------------------------------------------
-----------------------------------------------------------------
-- Extrair metadados
-----------------------------------------------------------------

local meta

local function Meta(doc_meta)
    meta = doc_meta
    return doc_meta
end

-----------------------------------------------------------------
-- Create figure
-----------------------------------------------------------------

local latex_doc_template = [[
\documentclass{braunfig}
\begin{document}
%s
\end{document}
]]

local function latexmk(doc_path, out_path)
    local commands = {
        "latexmk",
        "-quiet",
        "-lualatex",
        "-e \"ensure_path('TEXINPUTS', '" .. meta.texinputs .. "//')\"",
        "-shell-escape",
        "-interaction=nonstopmode",
        "-file-line-error",
        "-cd",
        doc_path .. ">" .. out_path,
    }
    local cmd_str = table.concat(commands, " ")
    os.execute(cmd_str)
end

local function tex2image(src, filename)
    local dir_path = meta.path .. "/" .. filename .. "/"
    local doc_path = dir_path .. filename .. ".tex"
    local out_path = dir_path .. filename .. ".out"

    os.execute("mkdir -p " .. dir_path)

    local f = io.open(doc_path, 'w')
    if f == nil then
        return
    end

    f:write(latex_doc_template:format(src))
    f:close()

    latexmk(doc_path, out_path)
end

-----------------------------------------------------------------
-- Image
-----------------------------------------------------------------

local function Image(elem)
    --
    -- Substituir um .tex referente a um .svg.
    --
    if string.sub(elem.src, -4) ~= ".svg" then
        return elem
    end

    local filename = string.sub(elem.src, 1, -5)

    local f = io.open(meta.path .. "/" .. filename .. ".tex", "r")
    if not f then
        return elem
    end

    local text = f:read("*a")
    tex2image(text, filename)

    return pandoc.RawInline("latex", text)
end

-----------------------------------------------------------------
-- CodeBlock
-----------------------------------------------------------------

local fig_num = 0

local function CodeBlock(elem)
    --
    -- Cria uma figura em latex.
    --
    if elem.classes[1] ~= "latex" then
        return elem
    end

    fig_num = fig_num + 1

    local filename = meta.id .. "img" .. string.format("%02d", fig_num)
    tex2image(elem.text, filename)

    return pandoc.Para {
        pandoc.Image({}, filename .. ".svg")
    }
end

-----------------------------------------------------------------
-- Export
-----------------------------------------------------------------

return {
    { Meta = Meta },
    { Image = Image },
    { CodeBlock = CodeBlock }
}
