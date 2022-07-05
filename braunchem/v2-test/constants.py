"""Base de dados para dados termodinâmicos, Gabriel Braun, 2022

Esse módulo implementa uma API para propriedades termodinâmicas.
"""
import latex
import csv
import json
from dataclasses import dataclass, asdict
from decimal import Decimal, Context


@dataclass(frozen=True, slots=True)
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
        return f'Parameter({self.id_})'

    def create_qty(self, substance, value: str):
        """Fabrica `Quantity` a partir do `Parameter`, `Substance` e valor.

        Exemplo:
            >>> p = Parameter('H', 'entalpia', 'H', 'J')
            >>> s = Substance('C', 'carbono', 'C')
            >>> p.create_qty(s, '100')
            Quantity(H(C))
        """
        return Quantity(
            id_=f'{self.id_}({substance.id_})',
            name=preposition_join(self.name, substance.name),
            symbol=f'{self.symbol}({substance.symbol})',
            value=Context(prec=self.prec).create_decimal(value),
            unit=self.unit,
            prec=self.prec
        )

    @staticmethod
    def decoder(obj):
        clsname = obj.pop('__classname__', None)
        if clsname == 'Parameter':
            return Parameter(**obj)

        return obj


def preposition_join(parameter_name: str, substance_name: str):
    """Retorna os nomes unidos pela preposição do gênero correto.

    Olha o último caratere da primeira palavra no nome e
    retorna o nome com a preposição do gênero correto.

    Args:
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


@dataclass(frozen=True, slots=True)
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
    state: str = None

    def __repr__(self):
        return f'Substance({self.id_})'

    @property
    def symbol(self):
        """Retorna símbolo LaTeX da substância.

        Exemplo:
            >>> s = Substance('1', 'água', 'H2O', state='l')
            >>> s.symbol
            '\\ce{H2O,\\,\\text{l}}'
            >>> t = Substance('2', 'carbono', 'C')
            >>> t.symbol
            '\\ce{C}'
        """
        if not self.state:
            return latex.ce(self.formula)

        return latex.ce(f'{self.formula},\\,\\text{{{self.state}}}')


@dataclass(frozen=True, slots=True)
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
    value: Decimal = None
    unit: str = ''
    prec: int = 3

    def __repr__(self):
        return f'Quantity({self.id_})'

    def __float__(self):
        return float(self.value)

    def __lt__(self, other):
        """Comparação em ordem alfabética."""
        return self.name < other.name

    def to_sci_string(self):
        """Retorna o valor em notação científica."""
        return decimal_to_sci_string(self.value)

    def to_eng_string(self):
        """Retorna o valor em notação de engenharia."""
        return self.value.to_eng_string()

    @property
    def equation(self):
        """Retorna o dado termodinâmico como uma equação em LaTeX.

        Exemplo:
            >>> q = Quantity('1', 'Exemplo', 'e', Decimal(10), 'm')
            >>> q.equation
            'e = \\qty{10}{m}'
        """
        if self.value is None:
            return self.name

        value = self.to_sci_string()
        return f'${self.symbol} = {latex.qty(value, self.unit)}$'

    @property
    def display(self):
        """Retorna o nome do dado termodinâmico, seguido da equação em LaTeX.

        Exemplo:
            >>> q = Quantity('1', 'Exemplo', 'e', Decimal('10'), 'm')
            >>> q.display
            'Exemplo, e = \\qty{10}{m}'
        """
        if self.value is None:
            return self.name

        return ', '.join([self.name, self.equation])


def decimal_to_sci_string(value: Decimal, lower_bound=1e-3, upper_bound=1e4):
    """Retorna o valor em notação científica.

    Args:
        lower_bound (float): Limite inferior para notação científica.
        upper_bound (float): Limite superior para notação científica.
    """
    if not value:
        return '0'

    if abs(value) < lower_bound or abs(value) > upper_bound:
        return f'{value:e}'.replace('+', '')

    return f'{value:f}'


def csv2quantities(file, parameters):
    """Gerador para os dados termodinâmicos contidos em um `csv`.

    Gera:
        Quantity: o próximo dado termodinâmico no `csv`.
    """
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            substance_attrs = {attr: row.pop(attr, None)
                               for attr in ['id_', 'name', 'formula', 'state']}
            substance = Substance(**substance_attrs)

            for parameter_id, value in row.items():
                if not value:
                    continue
                parameter = parameters[parameter_id]
                yield parameter.create_qty(substance, value)


@dataclass(slots=True)
class Table:
    """Container para `Quantity`.

    Atributos:
        quantities (list): Lista de dados termodinâmicos.
    """
    quantities: list[Quantity]

    def __repr__(self):
        if len(self.quantities) == 1:
            return 'Table(1 item)'

        return f'Table({len(self.quantities)} items)'

    def __contains__(self, item):
        return item in self.quantities

    def __iter__(self):
        return iter(self.quantities)

    def __getitem__(self, key):
        return DATA.filter([key]).quantities[0]

    def append(self, qty: Quantity):
        self.quantities.append(qty)

    def filter(self, qty_ids: list):
        """Cria um subconjunto da lista de dados termodinâmicos.

        Retorna:
            Table: Subconjunto de dados com os `id_` selecionados.
        """
        filtered = [qty for qty in self if qty.id_ in qty_ids]
        return Table(filtered)

    def equation_list(self, sort=True):
        latex_list = latex.List('itemize', [x.equation for x in sorted(self)])
        return latex_list.display()

    def display_list(self, sort=True):
        latex_list = latex.List('itemize', [x.display for x in sorted(self)])
        return latex_list.display()

    def to_json(self, file):
        with open(file, 'w') as json_file:
            json.dump(self, json_file, cls=QuantityEncoder,
                      indent=4, ensure_ascii=False)

    def append_csv(self, file: str, parameters: dict):
        """Adiciona os dados em um `csv`.

        Args:
            file (str): Arquivo `csv`
            parameters (dict): `dict` com os parâmetros no header do `csv`.
        """
        for qty in csv2quantities(file, parameters):
            self.append(qty)

    @classmethod
    def from_json(cls, file):
        with open(file, 'r') as json_file:
            quantities = json.load(json_file, object_hook=Table.decoder)
            return cls(quantities)

    @staticmethod
    def decoder(obj):
        clsname = obj.pop('__classname__', None)

        if clsname == 'Quantity':
            value = obj.pop('value')
            prec = obj['prec']
            return Quantity(**obj, value=Context(prec).create_decimal(value))

        return obj


class QuantityEncoder(json.JSONEncoder):
    """Encoder para converter um `Table` em `json`."""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return decimal_to_sci_string(obj)

        if isinstance(obj, Table):
            return obj.quantities

        if isinstance(obj, Quantity):
            d = {'__classname__': type(obj).__name__}
            d.update(asdict(obj))
            return d

        return super(QuantityEncoder, self).default(obj)


DATA = Table.from_json('database/data/data.json')


def main():
    dt = Table.from_json('database/data/tables/constants.json')

    with open('database/data/parameters.json', 'r') as json_file:
        parameters = json.load(json_file, object_hook=Parameter.decoder)

    for table in ['inorganic', 'bonds']:
        dt.append_csv(f'database/data/tables/{table}.csv', parameters)

    dt.to_json('database/data/data.json')

    print(DATA['Hf(Ca+2,aq)'].value)


if __name__ == "__main__":
    main()
