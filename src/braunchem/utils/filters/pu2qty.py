"""Converte todos os comandos `\\pu` do `mhchem` aos equivalentes no formato `siunitx`."""
import re

import panflute as pf

PU_CMD_REGEX = re.compile(r"\\pu\{\s*([\deE\,\.\+\-]*)\s*([\/\\\s\w\d\.\+\-\%]*)\s*\}")
UNIT_EXP_REGEX = re.compile(r"[\+\-]?\d+")


def parse_fractions(unit_str: str):
    try:
        numerator, denominator = unit_str.split("//", 1)
        return f"\\tfrac{{{numerator}}}{{{parse_fractions(denominator)}}}"
    except ValueError:
        return unit_str


def qty(num_str: str, unit_str: str) -> str:
    """Retorna o comando no formato `siunitx` referente a um valor numérico e uma unidade."""
    # valor numérico sem unidades
    if not unit_str:
        return f"\\num{{{num_str}}}"

    formated_unit_str = re.sub(UNIT_EXP_REGEX, lambda x: f"^{{{x.group(0)}}}", unit_str)
    formated_unit_str = formated_unit_str.replace("\\mu", "\\micro")
    formated_unit_str = parse_fractions(formated_unit_str)

    # unidades sem valor numérico
    if not num_str:
        return f"\\unit{{{formated_unit_str}}}"

    return f"\\qty{{{num_str}}}{{{formated_unit_str}}}"


def pu2qty(elem, doc, debug=False):
    """Converte todos os comandos `\\pu` do mhchem aos equivalentes no formato `siunitx`."""
    if isinstance(elem, pf.Math) and doc.format == "latex":
        elem.text = re.sub(
            PU_CMD_REGEX, lambda x: qty(x.group(1), x.group(2)), elem.text
        )

        return elem


def main(doc=None):
    return pf.run_filter(pu2qty, doc=doc)


if __name__ == "__main__":
    main()
