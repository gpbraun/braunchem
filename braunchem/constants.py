import latex
from dataclasses import dataclass
from decimal import Decimal, Context

import csv
import json


with open('database/data/datatypes.json', 'r') as json_file:
    DATA_TYPES = json.load(json_file)
    """
    Constante com os parâmetros para cada tipo de dado termodinâmico.
    """


@dataclass(frozen=True)
class PhysicalQuantity:
    id_: str
    name: str
    symbol: str = ''
    value: Decimal = 0.0
    unit: str = ''

    def __lt__(self, other):
        # order quantity collections alphabetically
        return self.name < other.name

    def latex(self):
        # Formato siunitx
        if not self.value:
            return self.name

        return f'${self.symbol} = {latex.qty(self.value, self.unit)}$'


def prefixed_name(name: str):
    """
    Retorna nome com prefixo do gênero correto.

    Olha o último caratére da primeira palavra no nome e
    retorna o nome com o prefixo do gênero correto.

    Examples
    ----------
    >>> prefixed_name('água')
    ' da água'
    >>> prefixed_name('sódio')
    ' do sódio'
    """

    last_char = name.split(' ')[0][-1]

    if last_char == 'a':
        return f' da {name}'

    return f' do {name}'


def create_symbol(dt: dict, formula: str, state: str):

    prefix = latex.cmd('Delta') if dt['delta'] else ''

    symbol = dt['symbol']

    sup = latex.cmd('circ') if dt['standard'] else dt['superscript']
    sub = latex.cmd('mathrm', dt['subscript'])

    suffix = f'^{{{sup}}}_{{{sub}}}'
    formula = latex.cmd('ce', f'{formula}, {{{state}}}' if state else formula)

    return prefix + symbol + suffix + f'({formula})'


def parse_pq(data_type: str, data_id: str, name: str, formula: str,
             state: str, value: str, prec: int = 3):
    """
    Creates physical quantity
    """

    dt = DATA_TYPES[data_type]

    return PhysicalQuantity(
        id_=f'{data_type}-{data_id}',
        value=Context(prec).create_decimal(value),
        name=dt['name'] + prefixed_name('água'),
        symbol=create_symbol(dt, formula, state),
        unit=dt['unit']
    )


@dataclass(frozen=True)
class DataType:
    name: str
    symbol: str
    sub: str = ''
    sup: str = ''
    delta: bool = False
    std: bool = False
    unit: str = ''

    def symbol(self):
        # Thermochemical state notation in latex format
        prefix = latex.cmd('Delta') if self.delta else ''

        superscript = latex.cmd("circ") if self.std else '' + self.sup
        subscript = latex.cmd("mathrm", [self.sub]) if self.sub else ''

        suffix = f'^{{{superscript}}}' + f'_{{{subscript}}}'

        return prefix + self.symbol + suffix


def main():

    with open('database/data/inorganic-2.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        x = [row for row in reader][100]

        pq = parse_pq(
            'Hf', x['id'], x['name'], x['formula'], x['state'], x['Hf']
        )
        print(pq)


if __name__ == "__main__":
    main()
