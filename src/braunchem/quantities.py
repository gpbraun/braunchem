"""Base de dados para dados termodinâmicos, Gabriel Braun, 2022

Esse módulo implementa uma API para propriedades termodinâmicas.
"""
import braunchem.utils.latex as latex

import os
import re
import csv
import logging
import importlib.resources
from pathlib import Path
from decimal import Decimal, Context

from pydantic import BaseModel


DB_PATH = importlib.resources.files("braunchem.data")
"""Diretório da base de dados."""


class Parameter(BaseModel):
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
    unit: str | None = None
    prec: int = 3

    def __repr__(self):
        return f"Parameter({self.id_})"

    def create_qty(self, substance, value: str):
        """Fabrica `Quantity` a partir do `Parameter`, `Substance` e valor.

        Exemplo:
            >>> p = Parameter('H', 'entalpia', 'H', 'J')
            >>> s = Substance('C', 'carbono', 'C')
            >>> p.create_qty(s, '100')
            Quantity(H(C))
        """
        return Quantity(
            id_=f"{self.id_}({substance.id_})",
            name=preposition_join(self.name, substance.name),
            symbol=f"{self.symbol}({substance.symbol})",
            value=Context(prec=self.prec).create_decimal(value),
            unit=self.unit,
            prec=self.prec,
        )


class ParameterSet(BaseModel):
    """Conjunto de parâmetros termodinâmicos."""

    parameters: list[Parameter]

    def __contains__(self, item):
        return item in self.parameters

    def __iter__(self):
        return iter(self.parameters)

    def __getitem__(self, key: str) -> Parameter:
        try:
            return [par for par in self if par.id_ == key][0]
        except IndexError:
            raise KeyError


PARAMETERS_DB_PATH = DB_PATH.joinpath("parameters.json")
"""Endereço da base de dados de parâmetros."""

PARAMETERS = ParameterSet.parse_file(PARAMETERS_DB_PATH)
"""Base de dados de parâmetros."""


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
    last_char = substance_name.split(" ")[0][-1]

    if last_char == "a":
        return f"{parameter_name} da {substance_name}"

    return f"{parameter_name} do {substance_name}"


class Substance(BaseModel):
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
    state: str | None = None

    def __repr__(self):
        return f"Substance({self.id_})"

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

        return latex.ce(f"{self.formula},\\,\\text{{{self.state}}}")


class Quantity(BaseModel):
    """Dado termodinâmico.

    Atributos:
        id_ (str): Identificador único para acessar o dado termodinâmico.
        name (str): Nome.
        symbol (str): Símbolo.
        value (Decimal): Valor.
        unit (str, optional): Unidade.
            Exemplos: `kJ`, `mm2`, `J.s`, `kJ.mol-1`.
    """

    id_: str
    name: str
    symbol: str | None = None
    value: Decimal | None = None
    unit: str | None = None
    prec: int = 3

    def __repr__(self):
        return f"Quantity({self.id_})"

    def __float__(self):
        return float(self.sci_string)

    @property
    def sci_string(self):
        """Retorna o valor em notação científica."""
        return decimal_to_sci_string(self.value)

    @property
    def eng_string(self):
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
            return latex.pu2qty(self.name)

        value = self.sci_string
        return f"${self.symbol} = {latex.qty(value, self.unit)}$"

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

        return ", ".join([self.name, self.equation])

    @classmethod
    def parse_string(cls, string: str):
        """Retorna o `Quantity` referente a string.

        Exemplo:
            >>> q = parse_string("Ka(NH4+)=5e-10")
        """
        match = re.match(QTY_STR_RE, string)

        if match:
            p_id = match.group(1)
            s_name = match.group(2)
            s_state = match.group(3)
            value = match.group(4)

            if p_id in PARAMETERS:
                p = PARAMETERS[p_id]
                s = Substance(
                    id_=s_name, name=f"\\ce{{{s_name}}}", formula=s_name, state=s_state
                )
                return p.create_qty(s, value)

        return cls(id_=string, name=string)


QTY_STR_RE = re.compile(r"([\w\d]*)\(([\w\d]*),?(.*)\)\=([\d\.Ee\+\-]*)")
"""Expressão em REGEX para converter uma string em um `Quantity`"""


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


def csv2quantities(file):
    """Gerador para os dados termodinâmicos contidos em um `csv`.

    Gera:
        Quantity: o próximo dado termodinâmico no `csv`.
    """
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            s = {
                attr: row.pop(attr, None)
                for attr in ["id_", "name", "formula", "state"]
            }
            substance = Substance.parse_obj(s)

            for parameter_id, value in row.items():
                if not value:
                    continue
                parameter = PARAMETERS[parameter_id]
                yield parameter.create_qty(substance, value)


class Table(BaseModel):
    """Container para `Quantity`.

    Atributos:
        quantities (list): Lista de dados termodinâmicos.
    """

    quantities: list[Quantity]

    def __repr__(self):
        qtys = ", ".join(q.id_ for q in self)
        return f"Table({qtys})"

    def __len__(self):
        return len(self.quantities)

    def __contains__(self, item):
        return item in self.quantities

    def __iter__(self):
        return iter(self.quantities)

    def __getitem__(self, key):
        try:
            return [qty for qty in self if qty.id_ == key][0]
        except IndexError:
            raise KeyError

    def append(self, qty: Quantity):
        self.quantities.append(qty)

    def filter(self, qty_ids: list):
        """Cria um subconjunto da lista de dados termodinâmicos.

        Args:
            ids (list): Lista com os `id_` desejados.

        Retorna:
            Table: Subconjunto de dados com os `id_` selecionados.
        """
        qtys = []
        for qty_id_ in qty_ids:
            try:
                qtys.append(self[qty_id_])
            except KeyError:
                qty = Quantity.parse_string(qty_id_)
                qtys.append(qty)

        return Table(quantities=sorted(qtys, key=lambda qty: qty.name))

    def equation_list(self):
        if not self.quantities:
            return

        latex_list = latex.List("datalist", [x.equation for x in self])
        return latex_list.display()

    def display_list(self):
        if not self.quantities:
            return

        latex_list = latex.List("datalist", [x.display for x in self])
        return latex_list.display()

    def append_csv(self, csv_file: str | Path):
        """Adiciona os dados de um `csv`.

        Args:
            csv_file (str | Path): Arquivo `csv`
        """
        for qty in csv2quantities(csv_file):
            self.append(qty)

    def append_csvs(self, csv_files: list[str] | list[Path]):
        """Adiciona os dados de uma lista de `csv`.

        Args:
            csv_files (list[str] | list[Path]): Arquivo `csv`
        """
        for csv in csv_files:
            self.append_csv(csv)


def get_table_paths(table_db_path: str | Path):
    """Retorna a lista com todas as tabelas em `.csv` no diretório."""
    table_files = []

    for root, _, files in os.walk(table_db_path):
        for f in files:
            path = Path(os.path.join(root, f))

            # problems
            if path.suffix == ".csv":
                # problem = Problem.parse_file(path)
                table_files.append(path)

    return table_files


QUANTITIES_DB_PATH = DB_PATH.joinpath("quantities.json")
"""Endereço da base de dados de problemas."""

QUANTITIES = Table.parse_file(QUANTITIES_DB_PATH)
"""Base de dados termodinâmicos."""


def qty(qty_id: str) -> Quantity:
    """Retorna um dado termodiâmico da base de dados."""
    return QUANTITIES[qty_id]


def qtys(qty_ids: list[str]) -> list[Quantity]:
    """Retorna um conjunto de dados termodiâmicos da base de dados."""
    return QUANTITIES.filter(qty_ids)


def main():
    logging.basicConfig(level=logging.DEBUG)

    constants_path = DB_PATH.joinpath("constants.json")
    dt = Table.parse_file(constants_path)

    paths = get_table_paths("data/quantities")

    dt.append_csvs(paths)

    with open(QUANTITIES_DB_PATH, "w", encoding="utf-8") as json_file:
        json_file.write(dt.json(indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
