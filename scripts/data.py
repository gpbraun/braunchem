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


DATATYPES = {
    # ORGANIC/INORGANIC
    'Hf': DataType(
        'Entalpia de formação do ', '\\Delta H_\\text{f}',  'kJ.mol-1'
    ),
    'Gf': DataType(
        'Entalpia livre de formação do ', '\\Delta G_\\text{f}', 'kJ.mol-1'
    ),
    'CP': DataType(
        'Capacidade calorífica do ', 'C_P', 'J.K-1.mol-1'
    ),
    'S':  DataType(
        'Entropia do ', 'S', 'J.K-1.mol-1'
    ),
    'Hc': DataType(
        'Entalpia de combustão do ', '\\Delta H_\\text{c}', 'kJ.mol-1'
    ),
    # BONDS
    'HL': DataType(
        'Entalpia da ligação ', '\\Delta H_\\text{L}', 'kJ.mol-1'
    ),
    # SOLVENTS
    'd': DataType(
        'Densidade do ', '\\rho',  'g.cm^{-3}'
    ),
    'Hvap': DataType(
        'Entalpia de vaporização do ', '\\Delta H_\\text{vap}',  'kJ.mol-1'
    ),
    'Hfus': DataType(
        'Entalpia de fusão do ', '\\Delta H_\\text{fus}',  'kJ.mol-1'
    ),
    'Hsub': DataType(
        'Entalpia de sublimação do ', '\\Delta H_\\text{sub}',  'kJ.mol-1'
    ),
    'Tf': DataType(
        'Temperatura de fusão do ', 'T_\\text{fus}',  'K'
    ),
    'Te': DataType(
        'Temperatura de ebulição do ', 'T_\\text{eb}',  'K'
    ),
    'Pvap': DataType(
        'Pressão de vapor ', 'P_\\text{vap}',  'mmHg'
    ),
    # ELEMENTS
    'Tfus': DataType(
        'Temperatura de fusão do ', 'T_\\text{fus}', '\\degree C'
    ),
    'Phi': DataType(
        'Função trabalho do ', '\\Phi', 'eV'
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
