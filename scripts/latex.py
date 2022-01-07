import re


# LATEX INTEGRATION FUNCTIONS
#


def cmd(name, content=[]):
    if content:
        tex_args = ''.join(f'{{{arg}}}' for arg in content)
        return f'\\{name}{tex_args}'

    return f'\\{name}'


def env(env, content):
    return f'\n\n\\begin{{{env}}}\n{content}\n\\end{{{env}}}\n'


def section(content, level=0, newpage=False, numbered=True):
    if not content:
        return ''

    newpage_cmd = cmd('newpage') if newpage else ''
    section_cmd = level*'sub' + ('section' if numbered else 'section*')
    return newpage_cmd + cmd(section_cmd, [content]) + '\n'


TEX_LEN = re.compile(r'\\\w+|[\w\d\=\%]|\d')


def enum(name, items, cols=0, auto_cols=False):
    if auto_cols:
        max_length = max([len(re.findall(TEX_LEN, i)) for i in items])
        if max_length < 4:
            cols = 5
        elif max_length < 7:
            cols = 3
        elif max_length < 20:
            cols = 2

    cols = f'({cols})' if cols else ''
    content = '\n'.join([f'\\item {i}' for i in items])
    return env(name, f'{cols}\n{content}')


PU_CMD = re.compile(r'\\pu\{\s*([\deE\,\.\+\-]*)\s*([\/\\\s\w\d\.\+\-]*)\s*\}')
UNIT_EXP = re.compile(r'[\+\-]\d+')


def qty(num, unit):
    # convert \pu command to \unit, \num or \qty
    if not unit:  # number only
        return cmd('num', [num])

    formated_unit = re.sub(UNIT_EXP, lambda x: f'^{{{x.group(0)}}}', unit)

    if not num:  # unit ony
        return cmd('unit', [formated_unit])

    return cmd('qty', [num, formated_unit])


def pu2qty(content):
    # converts all \pu commands to \unit, \num or \qty
    return re.sub(PU_CMD, lambda x: qty(x.group(1), x.group(2)), content)
