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

    suffix = '^' + superscript + '_' + subscript

    return prefix + state + suffix


DATATYPES = {
    # ORGANIC/INORGANIC
    'Hf': DataType(
        'Entalpia de formação do ',
        state('H', sub='f'),
        'kJ.mol-1'
    ),
    'Gf': DataType(
        'Entalpia livre de formação do ',
        state('G', sub='f'),
        'kJ.mol-1'
    ),
    'CP': DataType(
        'Capacidade calorífica do ',
        'C_P',
        'J.K-1.mol-1'
    ),
    'S':  DataType(
        'Entropia do ',
        state('S', delta=False),
        'J.K-1.mol-1'
    ),
    'Hc': DataType(
        'Entalpia de combustão do ',
        state('Hc', sub='c'),
        'kJ.mol-1'
    ),
    # BONDS
    'HL': DataType(
        'Entalpia da ligação ',
        state('H', sub='L'),
        'kJ.mol-1'
    ),
    # SOLVENTS
    'd': DataType(
        'Densidade do ',
        latex.cmd('rho'),
        'g.cm^{-3}'
    ),
    'Hvap': DataType(
        'Entalpia de vaporização do ',
        state('H', sub='vap'),
        'kJ.mol-1'
    ),
    'Hfus': DataType(
        'Entalpia de fusão do ',
        state('H', sub='fus'),
        'kJ.mol-1'
    ),
    'Hsub': DataType(
        'Entalpia de sublimação do ',
        state('H', sub='sub'),
        'kJ.mol-1'
    ),
    'Tf': DataType(
        'Temperatura de fusão do ',
        state('T', delta=False, sub='fus', std=False),
        'K'
    ),
    'Te': DataType(
        'Temperatura de ebulição do ',
        state('T', delta=False, sub='eb', std=False),
        'K'
    ),
    'Pvap': DataType(
        'Pressão de vapor ',
        state('P', delta=False, sub='vap'),
        'mmHg'
    ),
    # ELEMENTS
    'Phi': DataType(
        'Função trabalho do ',
        latex.cmd('Phi'),
        'eV'
    ),
}


@frozen
class Data:
    id_: str
    mol: str
    state: str
    value: float
    unit: str
    name: str
    symbol: str

    def astex(self):
        # return data in sunitx format
        return f'${self.symbol} = {latex.qty(self.value, self.unit)}$'


RE_DATA_MOL = re.compile(r'(.*)\((.*)\)')


@frozen
class DataSet:
    data: dict = Factory(dict)

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
                            self.append(id_, prop, datamol, row[prop])

        return self

    def append(self, id_, datatype, datamol, value):
        # return data object from csv cell
        dt = DATATYPES[datatype]

        value = value.replace('.', ',')
        unit = dt.unit

        mol_match = re.match(RE_DATA_MOL, datamol)
        if mol_match:
            mol, state = mol_match.group(1), mol_match.group(2)
            name = dt.name + f'\\ce{{{mol}}} ({state})'
            symbol = dt.symbol + f'(\\ce{{{mol}, {{{state}}}}})'
        else:
            state = ''
            name = dt.name + f'\\ce{{{datamol}}}'
            symbol = dt.symbol + f'(\\ce{{{datamol}}})'

        self.data[id_] = Data(id_, datamol, state, value, unit, name, symbol)

        return self

    def filter(self, data_ids):
        filtered_data = []
        for id_ in data_ids:
            try:
                filtered_data.append(self.data[id_])
            except KeyError:
                print(f"Dado '{id_}' não encontrado!")
        return filtered_data


def read_datasets(db_path):
    dataset = DataSet()

    for f in os.listdir(db_path):
        path = Path(os.path.join(db_path, f))
        if path.suffix == '.csv':
            dataset.append_csv(path)

    return dataset


def main():
    DATA = read_datasets('database/data')
    print(DATA.filter(['Hf-octano(l)']))


if __name__ == "__main__":
    main()
