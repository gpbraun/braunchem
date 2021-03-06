"""
Funções em LaTeX, Gabriel Braun, 2022

Todo:
    * Implementar a classe LaTeXDoc
"""

from dataclasses import dataclass
import re


def key(args):
    return ','.join([f'{k}={{{v}}}' for k, v in args.items()])


def cmd(name, args='', end=''):
    # latex command
    if not args:
        return f'\\{name} ' + end

    if isinstance(args, list):
        tex_args = ''.join(f'{{{arg}}}' for arg in args)
        return f'\\{name}{tex_args}' + end

    return f'\\{name}{{{args}}}' + end


def env(env, content):
    # latex environment
    return f'\n\n\\begin{{{env}}}\n{content}\n\\end{{{env}}}\n'


def document(preamble, body):
    # latex \begin{document} command
    return preamble + env('document', cmd('maketitle') + body)


def section(content, level=0, newpage=False, numbered=True):
    # latex section
    if not content:
        return ''

    newpage_cmd = cmd('newpage') if newpage else ''
    section_cmd = level*'sub' + ('section' if numbered else 'section*')
    return newpage_cmd + cmd(section_cmd, [content], end='\n')


TEX_LEN = re.compile(r'\\\w+|[\w\d\+\-\=\%]|\d')


def latex_len(tex_str):
    count = 0
    for match in re.findall(TEX_LEN, tex_str):
        if match in ['=', '\\rightarrow']:
            count += 2
        elif match in [',', '\\pu']:
            count += 0
        elif match in ['\\frac', '_']:
            count -= 1
        else:
            count += 1
    return count


def enum(name, items, cols=0, auto_cols=False, sep_cmd='item'):
    # latex enumerate
    if auto_cols:
        max_length = max([latex_len(i) for i in items])
        if max_length < 4:
            cols = 5
        elif max_length < 7:
            cols = 3
        elif max_length < 20:
            cols = 2

    cols = f'({cols})' if cols else ''
    content = '\n'.join([cmd(sep_cmd) + i for i in items])
    return env(name, f'{cols}{content}')


PU_CMD = re.compile(
    r'\\pu\{\s*([\deE\,\.\+\-]*)\s*([\/\\\s\w\d\.\+\-\%]*)\s*\}'
)
UNIT_EXP = re.compile(r'[\+\-]?\d+')


def ce(arg):
    # mhchem
    return cmd('ce', arg)


def qty(num, unit):
    # siunitx
    if not unit:  # number only
        return cmd('num', [num])

    formated_unit = re.sub(UNIT_EXP, lambda x: f'^{{{x.group(0)}}}', unit)
    formated_unit = formated_unit.replace('\\mu', '\\micro')

    if not num:  # unit ony
        return cmd('unit', [formated_unit])

    return cmd('qty', [num, formated_unit])


def pu2qty(content):
    # converts all \pu commands to \unit, \num or \qty
    return re.sub(PU_CMD, lambda x: qty(x.group(1), x.group(2)), content)


@dataclass(slots=True)
class List:
    """Lista
    """
    envname: str
    items: list[str]

    def __iter__(self):
        return iter(self.items)

    def display(self):
        if not self.items:
            return

        x = '\n'.join(f'\t\\item {item}' for item in self)
        return env(self.envname, x)


def tabular(cols: str, rows: list):
    """Tabela
    """
    top_row = ' & '.join(rows.pop(0))
    header = f'\t\\toprule\n\t{top_row} \\\\ \\midrule\n\t'

    body = ' \\\\\n\t'.join(' & '.join(col) for col in rows)
    return env('tabular', f'{{{cols}}}{header}{body} \\\\ \\bottomrule')


def main():
    la = List('itemize', ['a', 'b', 'c'])
    print(la.display())


if __name__ == "__main__":
    main()
