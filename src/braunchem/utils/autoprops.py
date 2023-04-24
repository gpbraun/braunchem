"""Gabriel Braun, 2022

Este módulo implementa funções para geração automática de distratores para problemas de múltipla escolha.
"""
import re
import random
from decimal import Decimal, Context
from itertools import permutations

from braunchem.utils.text import Text


def list_to_props(prop_list):
    html_str = ""
    tex_str = ""
    md_str = ""
    for i, prop in enumerate(prop_list):
        html_str += f"{prop}"
        tex_str += f"\\textbf{{{prop}}}"
        md_str += f"**{prop}**"
    if i < len(prop_list) - 1:
        sep = ", "
        html_str += sep
        tex_str += sep
        md_str += sep
    if i == len(prop_list) - 1:
        sep = " e "
        html_str += sep
        tex_str += sep
        md_str += sep
    return Text.parse_obj({"html": html_str, "md": md_str, "tex": tex_str})


def autoprops(true_props):
    """Cria as alternativas para problemas de V ou F."""
    if not true_props:
        choices = [
            list_to_props(["N"]),
            list_to_props([1]),
            list_to_props([2]),
            list_to_props([3]),
            list_to_props([4]),
        ]
        correct_choice = 0
    # Uma correta
    if true_props == [0]:  # 1
        choices = [
            list_to_props([1]),
            list_to_props([2]),
            list_to_props([1, 2]),
            list_to_props([1, 3]),
            list_to_props([1, 4]),
        ]
        correct_choice = 0
    if true_props == [1]:  # 2
        choices = [
            list_to_props([1]),
            list_to_props([2]),
            list_to_props([1, 2]),
            list_to_props([2, 3]),
            list_to_props([2, 4]),
        ]
        correct_choice = 1
    if true_props == [2]:  # 3
        choices = [
            list_to_props([2]),
            list_to_props([3]),
            list_to_props([1, 3]),
            list_to_props([2, 3]),
            list_to_props([3, 4]),
        ]
        correct_choice = 1
    if true_props == [3]:  # 4
        choices = [
            list_to_props([3]),
            list_to_props([4]),
            list_to_props([1, 4]),
            list_to_props([2, 4]),
            list_to_props([3, 4]),
        ]
        correct_choice = 1
    # Duas corretas
    if true_props == [0, 1]:  # 1 e 2
        choices = [
            list_to_props([1]),
            list_to_props([2]),
            list_to_props([1, 2]),
            list_to_props([1, 2, 3]),
            list_to_props([1, 2, 4]),
        ]
        correct_choice = 2
    if true_props == [0, 2]:  # 1 e 3
        choices = [
            list_to_props([1]),
            list_to_props([3]),
            list_to_props([1, 3]),
            list_to_props([1, 2, 3]),
            list_to_props([1, 3, 4]),
        ]
        correct_choice = 2
    if true_props == [0, 3]:  # 1 e 4
        choices = [
            list_to_props([1]),
            list_to_props([4]),
            list_to_props([1, 4]),
            list_to_props([1, 2, 4]),
            list_to_props([1, 3, 4]),
        ]
        correct_choice = 2
    if true_props == [1, 2]:  # 2 e 3
        choices = [
            list_to_props([2]),
            list_to_props([3]),
            list_to_props([2, 3]),
            list_to_props([1, 2, 3]),
            list_to_props([2, 3, 4]),
        ]
        correct_choice = 2
    if true_props == [1, 3]:  # 2 e 4
        choices = [
            list_to_props([2]),
            list_to_props([4]),
            list_to_props([2, 4]),
            list_to_props([1, 2, 4]),
            list_to_props([2, 3, 4]),
        ]
        correct_choice = 2
    if true_props == [2, 3]:  # 3 e 4
        choices = [
            list_to_props([3]),
            list_to_props([4]),
            list_to_props([3, 4]),
            list_to_props([1, 3, 4]),
            list_to_props([2, 3, 4]),
        ]
        correct_choice = 2
    # Três corretas
    if true_props == [0, 1, 2]:  # 1, 2 e 3
        choices = [
            list_to_props([1, 2]),
            list_to_props([1, 3]),
            list_to_props([2, 3]),
            list_to_props([1, 2, 3]),
            list_to_props([1, 2, 3, 4]),
        ]
        correct_choice = 3
    if true_props == [0, 1, 3]:  # 1, 2 e 4
        choices = [
            list_to_props([1, 2]),
            list_to_props([1, 4]),
            list_to_props([2, 4]),
            list_to_props([1, 2, 4]),
            list_to_props([1, 2, 3, 4]),
        ]
        correct_choice = 3
    if true_props == [0, 2, 3]:  # 1, 3 e 4
        choices = [
            list_to_props([1, 3]),
            list_to_props([1, 4]),
            list_to_props([3, 4]),
            list_to_props([1, 3, 4]),
            list_to_props([1, 2, 3, 4]),
        ]
        correct_choice = 3
    if true_props == [1, 2, 3]:  # 2, 3 e 4
        choices = [
            list_to_props([2, 3]),
            list_to_props([2, 4]),
            list_to_props([3, 4]),
            list_to_props([2, 3, 4]),
            list_to_props([1, 2, 3, 4]),
        ]
        correct_choice = 3
    # Todas corretas
    if true_props == [0, 1, 2, 3]:  # 1, 2, 3 e 4
        choices = [
            list_to_props([1, 2, 3]),
            list_to_props([1, 2, 4]),
            list_to_props([1, 3, 4]),
            list_to_props([2, 3, 4]),
            list_to_props([1, 2, 3, 4]),
        ]
        correct_choice = 4
    return choices, correct_choice


PU_CMD_REGEX = re.compile(
    r"\\pu\{\s*([\+\-]{1})?([\d\,\.]*)([eE]{1}(?:[+-])?\d+)?\s*([\/\\\s\w\d\.\+\-\%]+)?\s*\}"
)


def decimal_to_sci_string(value: Decimal, lower_bound=1e-3, upper_bound=1e4) -> str:
    """Retorna o valor em notação científica.

    Args:
        lower_bound (float): Limite inferior para notação científica.
        upper_bound (float): Limite superior para notação científica.
    """
    if not value:
        return "0"

    if abs(value) < lower_bound or abs(value) > upper_bound:
        return f"{value:E}".replace("+", "")

    return f"{value:f}"


class PhyisicalUnit:
    """Valor com unidade."""

    def __init__(
        self,
        value: Decimal | None = None,
        unit: str | None = None,
        sign: str = None,
        sci: bool = False,
    ):
        self.value = value
        self.unit = unit
        self.sign = sign
        self.sci = sci

    def to_pu(self):
        if not self.unit:
            return f"\\pu{{{self.value_string()}}}"
        return f"\\pu{{{self.value_string()} {self.unit}}}"

    def to_qty(self):
        if not self.unit:
            return f"\\num{{{self.value_string()}}}"
        return f"\\qty{{{self.value_string()}}}{{{self.unit}}}"

    def to_text(self):
        return Text.parse_obj(
            {
                "html": f'<span class="math inline">\\({self.to_pu()}\\)</span>',
                "tex": f"\\({self.to_qty()}\\)",
                "md": f"${self.to_pu()}$",
            }
        )

    def value_string(self):
        sign = self.sign if self.sign else ""

        if self.sci:
            value = f"{self.value:E}".replace("+", "").replace(".", ",")
        else:
            value = f"{self.value:f}".replace(".", ",")

        return sign + value

    def scale(self, scale: Decimal):
        """Retorna um novo `Physical Unit` com o valor multiplicado pela escala."""
        new_value = Context(prec=2).create_decimal(self.value * scale)
        return PhyisicalUnit(new_value, self.unit, self.sign, self.sci)

    @classmethod
    def parse_string(cls, string):
        match = re.search(PU_CMD_REGEX, string)

        if not match:
            return

        sign = match.group(1)
        num = match.group(2).replace(",", ".")
        exp = match.group(3)
        unit = match.group(4)

        value = Context(prec=3).create_decimal(num + exp if exp else num)

        return cls(value, unit, sign, bool(exp))


def numerical_choices(answer: str, seed: int | str = None):
    """Gera múltilplas escolhas para problemas com resposta numérica."""
    if seed:
        random.seed(seed)
    try:
        correct_choice = random.randint(0, 4)

        pu = PhyisicalUnit.parse_string(answer)

        scale = 1 + (abs(pu.value.log10()) + 1) / 5

        choices = [
            pu.scale(scale ** (index - correct_choice)).to_text() for index in range(5)
        ]

        return choices, correct_choice
    except AttributeError:
        raise AttributeError(f"Erro com seed {seed}")


def ordering_choices(
    answer: str, seed: int | str = None, path=None
) -> tuple[list, int]:
    """Gera múltilplas escolhas para problemas com resposta numérica."""
    if seed:
        random.seed(seed)

    correct_choice = random.randint(0, 4)

    answer_list = [x.strip() for x in answer.split(";")]
    answer = "; ".join(answer_list)

    if len(answer_list) < 3:
        raise Exception(f"Erro com seed {seed} (menos de três itens na lista)")

    # TODO: esse algorítimo é horroroso! melhorar urgente!
    choices = []
    choices_raw = [answer]

    while len(choices) < 4:
        distractor_list = list(answer_list)
        random.shuffle(distractor_list)
        distractor = "; ".join(distractor_list)
        if distractor not in choices_raw:
            choices_raw.append(distractor)
            choices.append(Text.parse_html(distractor + ".", path))

    choices.insert(correct_choice, Text.parse_html(answer + ".", path))

    return choices, correct_choice


def main():
    print(ordering_choices("1; 2; 3; 4; 5; 6; 7", seed=1234567))


if __name__ == "__main__":
    main()
