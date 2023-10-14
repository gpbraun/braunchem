-----------------------------------------------------------------
-- latex.lua
--
-- Gabriel Braun, 2023
-----------------------------------------------------------------

local function inline(text)
    return pandoc.RawInline('latex', text)
end

local function surround(inlines, begin_str, end_str)
    table.insert(inlines, 1, inline(begin_str))
    table.insert(inlines, inline(end_str))
end

local function env(name, title, body, opts)
    local env_header = title
    local env_footer = inline('\\end{' .. name .. '}')

    if opts == nil then
        surround(env_header, '\\begin{' .. name .. '}{', '}')
    else
        surround(env_header, '\\begin{' .. name .. '}[' .. opts .. ']{', '}')
    end

    return { env_header, body, env_footer }
end

-----------------------------------------------------------------
-- Export
-----------------------------------------------------------------

return {
    inline = inline,
    surround = surround,
    env = env,
}
