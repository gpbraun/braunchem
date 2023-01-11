"""
Funções em LaTeX, Gabriel Braun, 2022

Todo:
    * Implementar a classe LaTeXDoc
"""

import re


def cmd(cmd_name: str, args: str = "", end: str = ""):
    # latex command
    if not args:
        return f"\\{cmd_name} " + end

    if isinstance(args, list):
        tex_args = "".join(f"{{{arg}}}" for arg in args)
        return f"\\{cmd_name}{tex_args}" + end

    return f"\\{cmd_name}{{{args}}}" + end


def key(args: dict):
    key_list = ",\n\t".join([f"{k}={{{v}}}" for k, v in args.items()])
    return f"[\n\t{key_list}\n]"


def env(env_name: str, content: str, keys=None):
    """Cria um ambiente em LaTeX.

    Atributos:
        end_name (str): Nome do ambiente.
        content (str): Conteúdo do ambiente.
        keys (dict): Parâmetros opcionais
    """
    if keys:
        begin = f'{cmd("begin", env_name)}{key(keys)}'
    else:
        begin = cmd("begin", env_name)

    end = cmd("end", env_name)

    return f"\n{begin}\n{content}\n{end}\n"


def document(preamble, body):
    # latex \begin{document} command
    return preamble + env("document", cmd("maketitle") + body)


def section(content, level=0, newpage=False, numbered=False):
    # latex section
    if not content:
        return ""

    newpage_cmd = cmd("newpage") if newpage else ""
    section_cmd = level * "sub" + ("section" if numbered else "section*")
    return newpage_cmd + cmd(section_cmd, [content], end="\n")


TEX_LEN = re.compile(r"\\\w+|[\w\d\+\-\=\%]|\d")


def latex_len(tex_str):
    count = 0
    for match in re.findall(TEX_LEN, tex_str):
        if match in ["=", "\\rightarrow"]:
            count += 2
        elif match in [",", "\\pu"]:
            count += 0
        elif match in ["\\frac", "_"]:
            count -= 1
        else:
            count += 1
    return count


def enum(name: str, items: list, cols=0, sep_cmd="item"):
    # latex enumerate
    cols = f"({cols})" if cols else ""
    content = "\n".join([cmd(sep_cmd) + i for i in items])
    return env(name, f"{cols}{content}")


def ce(arg):
    # mhchem
    return cmd("ce", arg)


class List:
    """Lista"""

    envname: str
    items: list[str]

    def __init__(self, envname, items):
        self.envname = envname
        self.items = items

    def __iter__(self):
        return iter(self.items)

    def display(self, cols=1) -> str:
        if not self.items:
            return ""

        x = "\n".join(f"\t\\item {item}" for item in self)
        return env(self.envname, x)


def tabular(cols: str, rows: list):
    """Tabela"""
    top_row = " & ".join(rows.pop(0))
    header = f"\t\\toprule\n\t{top_row} \\\\ \\midrule\n\t"

    body = " \\\\\n\t".join(" & ".join(col) for col in rows)
    return env("tabular", f"{{{cols}}}{header}{body} \\\\ \\bottomrule")


PU_CMD_REGEX = re.compile(r"\\pu\{\s*([\deE\,\.\+\-]*)\s*([\/\\\s\w\d\.\+\-\%]*)\s*\}")
UNIT_EXP_REGEX = re.compile(r"[\+\-]?\d+")


def qty(num_str: str, unit_str: str) -> str:
    """Retorna o comando no formato `siunitx` referente a um valor numérico e uma unidade."""
    # valor numérico sem unidades
    if not unit_str:
        return f"\\num{{{num_str}}}"

    formated_unit_str = re.sub(UNIT_EXP_REGEX, lambda x: f"^{{{x.group(0)}}}", unit_str)
    formated_unit_str = formated_unit_str.replace("\\mu", "\\micro")

    # unidades sem valor numérico
    if not num_str:
        return f"\\unit{{{formated_unit_str}}}"

    return f"\\qty{{{num_str}}}{{{formated_unit_str}}}"


def pu2qty(tex_str: str):
    """Converte todos os comandos `\pu` do mhchem aos equivalentes no formato `siunitx`."""
    return re.sub(PU_CMD_REGEX, lambda x: qty(x.group(1), x.group(2)), tex_str)


def main():
    la = List("itemize", ["a", "b", "c"])
    print(la.display())


if __name__ == "__main__":
    main()
