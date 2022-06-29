"""Base de dados para dados termodinâmicos, Gabriel Braun, 2022

Esse módulo implementa uma API para propriedades termodinâmicas.
"""

import latex
from dataclasses import dataclass
from decimal import Decimal, Context

import csv
import json


@dataclass(frozen=True)
class Parameter:
    """Parâmetro termodinâmico.

    Atributos:
        id_ (str): Identificador único para acessar o tipo de parâmetro.
        name (int): Nome.
        symbol (str): Símbolo.
        unit (str, optional): Unidade.
        prec (int, optional): Número de algarismos significativos.
    """
    id_: str
    name: str
    symbol: str
    unit: str = ''
    prec: int = 3

    def __repr__(self):
        return f"Parameter('{self.id_}')"

    def latex(self, formula: str, state: str = ""):
        """Retorna o dado termodinâmico como uma equação em LaTeX.

        Atributos:
            formula (int): Fórmula molecular da substância.
            state (str, optional): Estado físico.

        Retorna:
            str: Equação em LaTeX.

        Exemplo:
            >>> dt = Parameter('H', 'entalpia', '\\Delta H', 'kJ')
            >>> dt.latex('H2O', 's')
            '\\Delta H(\\ce{H2O, {l}})'
        """
        chemformula = f'{formula}, {{{state}}}' if state else formula

        return self.symbol + f'({latex.cmd("ce", chemformula)})'


def ParameterDecoder(obj):
    """Decoder para converter um `json` em um `dict` de `Parameter`."""
    if '__type__' in obj and obj.pop('__type__') == 'Parameter':
        return Parameter(**obj)
    return obj


with open('database/data/datatypes.json', 'r') as json_file:
    PARAMETERS = json.load(json_file, object_hook=ParameterDecoder)
    """dict: `Parameters` para cada tipo de dado termodinâmico."""


@dataclass(frozen=True)
class Substance:
    """Substância.

    Atributos:
        id_ (str): Identificador para acessar a substância.
        name (str): Nome.
        formula (str, optional): Fórmula molecular.
        state (str, optional): Estado físico.
    """
    id_: str
    name: str
    formula: str
    state: str

    def __repr__(self):
        return f"Substance('{self.id_}')"


@dataclass(frozen=True)
class Quantity:
    """Dado termodinâmico.

    Atributos:
        id_ (str): Identificador único para acessar o dado termodinâmico.
        name (str): Nome.
        symbol (str, optional): Símbolo.
        value (Decimal, optional): Valor.
        unit (str, optional): Unidade.
            Exemplos: `kJ`, `mm2`, `J.s`, `kJ.mol-1`.
    """
    id_: str
    name: str
    symbol: str = ''
    value: Decimal = 0.0
    unit: str = ''

    def __repr__(self):
        return f"Quantity('{self.id_}')"

    def __float__(self):
        return float(self.value)

    def __lt__(self, other):
        """Comparação em ordem alfabética."""
        return self.name < other.name

    def equation(self):
        """Retorna o dado termodinâmico como uma equação em LaTeX.

        Exemplo:
            >>> pq = Quantity('1', 'Exemplo', 'e', Decimal(10), 'm')
            >>> pq.latex()
            'e = \\qty{10}{m}'
        """
        if not self.value:
            return self.name

        return f'${self.symbol} = {latex.qty(self.value, self.unit)}$'

    def display(self):
        """Retorna o nome do dado termodinâmico, seguido da equação em LaTeX.

        Exemplo:
            >>> q = Quantity('1', 'Exemplo', 'e', Decimal(10), 'm')
            >>> q.latex()
            'Exemplo, e = \\qty{10}{m}'
        """
        if not self.value:
            return self.name

        return f'${self.symbol} = {latex.qty(self.value, self.unit)}$'


def preposition_join(parameter_name: str, substance_name: str):
    """Retorna os nomes unidos pela preposição do gênero correto.

    Olha o último caratere da primeira palavra no nome e
    retorna o nome com a preposição do gênero correto.

    Atributos:
        parameter_name (str): Nome do parâmetro termodinâmico.
        substance_name (str): Nome da substância.

    Retorna:
        str: parametro do/da substância

    Exemplo:
        >>> add_preposition('entalpia', 'água')
        'entalpia da água'
        >>> add_preposition('entropia', 'sódio')
        'entropia do sódio'
    """
    last_char = substance_name.split(' ')[0][-1]

    if last_char == 'a':
        return f'{parameter_name} da {substance_name}'

    return f'{parameter_name} do {substance_name}'


def parse_pq(parameter: Parameter, substance: Substance, value: str):
    """Cria um `Quantity` a partir de um `Parameter` e um `Substance`.

    Exemplo:
        >>> p = Parameter('H', 'entalpia', 'H', 'J')
        >>> s = Substance('C', 'carbono', 'C')
        >>> parse_pq(p, s, Decimal(100))
        Quantity('H-C', 'entalpia do carbono', 'H(\\ce{C})', Decimal(100), 'J')
    """

    return Quantity(
        id_=f'{parameter.id_}-{substance.id_}',
        name=preposition_join(parameter.name, substance.name),
        symbol=parameter.latex(substance.formula, substance.state),
        value=Context(prec=parameter.prec).create_decimal(value),
        unit=parameter.unit
    )


@dataclass(frozen=True)
class DataTable:
    entries: dict


def main():

    with open('database/data/tables/inorganic.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        x = [row for row in reader][100]

        parameter = PARAMETERS['Hf']

        substance = Substance(x['id_'], x['name'], x['formula'], x['state'])

        pq = parse_pq(
            parameter, substance, x['Hf']
        )
        print(pq)


if __name__ == "__main__":
    main()
