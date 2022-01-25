#
# DOME - Gabriel Braun, 2021
#

import os
import re
import csv
from pathlib import Path

from attr import frozen, Factory

import latex


@frozen
class DataType:
    name: str
    symbol: str
    unit: str


def state(state, sub='', sup='', delta=True, std=True):
    # Thermochemical state notation in latex format
    prefix = latex.cmd('Delta') if delta else ''

    superscript = latex.cmd("circ") if std else '' + sup
    subscript = latex.cmd("mathrm", [sub]) if sub else ''

    suffix = f'^{{{superscript}}}' + f'_{{{subscript}}}'

    return prefix + state + suffix


@frozen
class Data:
    id_: str
    name: str
    symbol: str = ''
    value: float = 0.0
    unit: str = ''

    def __lt__(self, other):
        return self.name < other.name

    def astex(self):
        # return data in sunitx format
        if not self.id_:
            return self.name

        return f'${self.symbol} = {latex.qty(self.value, self.unit)}$'

    def tex_display(self):
        if not self.id_:
            return self.name

        # return data in sunitx format
        header = f'{self.name}'
        eqtn = f'${self.symbol} = {latex.qty(self.value, self.unit)}$'
        return header + ' ' + eqtn


RE_DATA_MOL = re.compile(r'(.*)\((.*)\)')


@frozen
class DataSet:
    data: list = Factory(list)

    def __len__(self):
        return len(self.data)

    def __add__(self, other):
        new_data = sorted(list(set([*self.data, *other.data])))
        return DataSet(new_data)

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def sorted(self):
        data = sorted(self.data)
        return data

    def asdict(self, attr):
        return {getattr(p, attr): p for p in self.data}

    def filter(self, attr, data_attrs):
        p_dict = self.asdict(attr)
        filtered_data = []
        for a in data_attrs:
            try:
                filtered_data.append(p_dict[a])
            except KeyError:
                filtered_data.append(Data(0, a))
        return DataSet(sorted(filtered_data))

    def astex(self):
        # return data as tex list
        if not self.data:
            return ''

        return latex.enum('datalist', [d.astex() for d in self.data])

    def tex_display(self):
        # return data as tex list
        if not self.data:
            return ''

        return latex.enum('datalist', [d.tex_display() for d in self.data])

    def append_csv(self, csv_path):
        if not os.path.exists(csv_path):
            print(f"O diretório '{csv_path}' não existe!")
            return self

        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                for prop in reader.fieldnames[1:]:
                    if row[prop]:
                        mol_names = row['id'].split(',')
                        for mol in mol_names:
                            datamol = mol.strip()
                            id_ = f"{prop}-{datamol}"
                            self.append_cell(id_, prop, datamol, row[prop])

        return self

    def append_cell(self, id_, datatype, datamol, value):
        # return data object from csv cell
        dt = DATATYPES[datatype]

        value = value.replace('.', ',')
        unit = dt.unit

        mol_match = re.match(RE_DATA_MOL, datamol)
        if mol_match:
            mol, state = mol_match.group(1), mol_match.group(2)
            name = dt.name + ' ' + latex.cmd('ce', mol) + f'({state})'
            symbol = dt.symbol + \
                '(' + latex.cmd('ce', mol + f', {{{state}}}') + ')'
        else:
            state = ''
            name = dt.name + ' ' + latex.cmd('ce', datamol)
            symbol = dt.symbol + '(' + latex.cmd('ce', datamol) + ')'

        self.data.append(Data(id_, name, symbol, value, unit))

        return self


def read_datasets(db_path):
    dataset = DataSet()

    for f in os.listdir(db_path):
        path = Path(os.path.join(db_path, f))
        if path.suffix == '.csv':
            dataset.append_csv(path)

    return dataset


CONSTANTS = DataSet([
    Data(
        'g',
        'Aceleração da gravidade',
        'g',
        '9,8067',
        'm.s-2',
    ),
    Data(
        'G',
        'Constante gravitacional',
        'G',
        '6,67384e11',
        'm3.kg.s-2',
    ),
    Data(
        'c',
        'Velocidade da luz no vácuo',
        'c',
        '2,99792458e8',
        'm.s-1',
    ),
    Data(
        'e',
        'Carga elementar',
        'e',
        '1,602176634e-19',
        'C',
    ),
    Data(
        'me',
        'Massa do elétron',
        'm_e',
        '9,1093837015e-31',
        'kg',
    ),
    Data(
        'h',
        'Constante de Planck',
        'h',
        '6,62607015e-34',
        'J.s',
    ),
    Data(
        'Kw',
        'Constante de autoprotólise da água',
        'K_\\mathrm{w}',
        '1e-14',

    ),
    Data(
        'R',
        'Constante dos Gases',
        'R',
        '8,314462',
        'J.K-1.mol-1'

    ),
    Data(
        'Patm',
        'Pressão atmosférica',
        '1 \\pu{atm}',
        '1,01325e5',
        'Pa'

    )
])


DATATYPES = {
    # ORGANIC/INORGANIC
    'Hf': DataType(
        'Entalpia de formação do',
        state('H', sub='f'),
        'kJ.mol-1'
    ),
    'Gf': DataType(
        'Entalpia livre de formação do',
        state('G', sub='f'),
        'kJ.mol-1'
    ),
    'CP': DataType(
        'Capacidade calorífica do',
        'C_P',
        'J.K-1.mol-1'
    ),
    'S':  DataType(
        'Entropia do ',
        state('S', delta=False),
        'J.K-1.mol-1'
    ),
    'Hc': DataType(
        'Entalpia de combustão do',
        state('Hc', sub='c'),
        'kJ.mol-1'
    ),
    # BONDS
    'HL': DataType(
        'Entalpia da ligação',
        state('H', sub='L'),
        'kJ.mol-1'
    ),
    # SOLVENTS
    'd': DataType(
        'Densidade do',
        latex.cmd('rho'),
        'g.cm^{-3}'
    ),
    'Hvap': DataType(
        'Entalpia de vaporização do',
        state('H', sub='vap'),
        'kJ.mol-1'
    ),
    'Hfus': DataType(
        'Entalpia de fusão do',
        state('H', sub='fus'),
        'kJ.mol-1'
    ),
    'Hsub': DataType(
        'Entalpia de sublimação do',
        state('H', sub='sub'),
        'kJ.mol-1'
    ),
    'Tf': DataType(
        'Temperatura de fusão do',
        state('T', delta=False, sub='fus', std=False),
        'K'
    ),
    'Te': DataType(
        'Temperatura de ebulição do',
        state('T', delta=False, sub='eb', std=False),
        'K'
    ),
    'Pvap': DataType(
        'Pressão de vapor',
        state('P', delta=False, sub='vap'),
        'mmHg'
    ),
    # ELEMENTS
    'Phi': DataType(
        'Função trabalho do',
        latex.cmd('Phi'),
        'eV'
    ),
}