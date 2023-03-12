"""Converte todos os comandos `\\pu` do `mhchem` aos equivalentes no formato `siunitx`."""
import re

import panflute as pf

PU_CMD_REGEX = re.compile(r"\\pu\{\s*([\deE\,\.\+\-]*)\s*([\/\\\s\w\d\.\+\-\%]*)\s*\}")
UNIT_EXP_REGEX = re.compile(r"[\+\-]?\d+")


def parse_fractions(unit_str: str):
    if not "//" in unit_str:
        return f"\\unit{{{unit_str}}}"

    numerator, denominator = unit_str.split("//", 1)
    numerator = f"\\unit{{{numerator}}}"
    return f"\\tfrac{{{numerator}}}{{{parse_fractions(denominator)}}}"


def qty(num_str: str, unit_str: str) -> str:
    """Retorna o comando no formato `siunitx` referente a um valor numérico e uma unidade."""
    # valor numérico sem unidades
    if not unit_str:
        return f"\\num{{{num_str}}}"

    formated_unit_str = re.sub(UNIT_EXP_REGEX, lambda x: f"^{{{x.group(0)}}}", unit_str)
    formated_unit_str = formated_unit_str.replace("\\mu", "\\micro")
    formated_unit_str = formated_unit_str.replace("\\Omega", "\\omh")
    formated_unit_str = parse_fractions(formated_unit_str)

    # unidades sem valor numérico
    if not num_str:
        return formated_unit_str

    return f"\\qty{{{num_str}}}{{{formated_unit_str}}}"


def pu2qty(text_str) -> str:
    """Converte todos os comandos `\\pu` do mhchem aos equivalentes no formato `siunitx`."""
    return re.sub(PU_CMD_REGEX, lambda x: qty(x.group(1), x.group(2)), text_str)


def filter_pu2qty(elem, doc, debug=False):
    """Converte todos os comandos `\\pu` do mhchem aos equivalentes no formato `siunitx` em um documento em PANDOC."""
    if isinstance(elem, pf.Math) and doc.format in ["latex", "beamer"]:
        elem.text = pu2qty(elem.text)

        return elem


def main(doc=None):
    return pf.run_filter(filter_pu2qty, doc=doc)


if __name__ == "__main__":
    main()
