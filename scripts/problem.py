#
# PROBLEM CLASS
#

import os
import re
import csv
from pathlib import Path

from attr import frozen, Factory

from frontmatter import load

import convert
import latex

#
# DATA CLASS
#


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
    id: str
    mol: str
    state: str
    value: float
    unit: str
    name: str
    symbol: str

    def astex(self):
        # return data in sunitx format
        return f'${self.symbol} = {latex.qty(self.value, self.unit)}$'


@frozen
class DataSet:
    dataset: dict = Factory(dict)

    def append_csv(self):

        return self

    def filter(self, data_ids):
        return [self.dataset[i] for i in data_ids]


RE_DATA_MOL = re.compile(r'(.*)\((.*)\)')


def cell2data(id, datatype, datamol, value):
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

    return Data(id, datamol, state, value, unit, name, symbol)


def csv2dataset(csv_path):
    dataset = {}

    if not os.path.exists(csv_path):
        print(f"O diretório '{csv_path}' não existe!")
        return

    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            for prop in reader.fieldnames[1:]:
                if row[prop]:
                    id = f"{prop}-{row['id']}"
                    dataset[id] = cell2data(id, prop, row['id'], row[prop])

    return dataset


def get_datasets(db_path):
    dataset = {}

    for root, _, files in os.walk(db_path):
        for f in files:
            path = Path(os.path.join(root, f))
            if path.suffix == '.csv':
                dataset.update(csv2dataset(path))

    return dataset


DATA = DataSet(get_datasets('database/data'))


@frozen
class Problem:
    id: str
    statement: str
    solution: str = ''
    answer: list = Factory(list)
    data: list = Factory(list)
    prop: bool = False
    obj: int = -1
    choices: list = Factory(list)

    def is_obj(self):
        if self.obj == -1:
            return False
        return True

    def tex_statement(self):
        return convert.md2tex(self.statement) + self.tex_choices()

    def tex_data(self):
        # return data as tex list with header
        if not self.data:
            return ''
        dlist = latex.enum('datalist', [d.astex() for d in self.data])
        return latex.section('Dados', level=2, numbered=False) + dlist

    def tex_choices(self):
        # return choices as tex list
        if not self.is_obj():
            return ''
        tex_choices = [convert.md2tex(c) for c in self.choices]
        return latex.enum('choices', tex_choices, auto_cols=True)

    def tex_answer(self):
        if not self.answer:
            return '-'
        if self.is_obj():
            return latex.cmd('MiniBox', content=[chr(65 + self.obj)])
        if len(self.answer) == 1:
            return self.answer[0]
        return latex.enum('answers', self.answer)

    def astex(self):
        # return problem as tex
        p = self.tex_statement() + self.tex_data()
        return latex.env('problem', f'[{self.id}]{p}')


@frozen
class ProblemSet:
    title: str
    problems: list[Problem]

    def tex_statements(self):
        if not self.problems:
            return ''

        statements = '\n'.join([p.astex() for p in self.problems])
        return latex.section(self.title) + statements

    def tex_answers(self):
        if not self.problems:
            return ''

        header = latex.section(self.title, level=1)
        answers = [p.tex_answer() for p in self.problems]

        if all([p.is_obj() for p in self.problems]):
            return header + latex.enum('checks', answers, cols=5)

        return header + latex.enum('answers', answers)


def file2problem(path):
    kwargs = {}
    # get YAML data and contents
    kwargs['id'] = path.stem

    pfile = load(path)
    soup = convert.md2soup(pfile.content)

    # get problem data
    if 'data' in pfile:
        kwargs['data'] = DATA.filter(pfile['data'])

    # change images direcory to images folder
    for img in soup.find_all('img'):
        img_name = os.path.basename(img['src'])
        img['src'] = os.path.join('images', img_name)

    solution = soup.find('blockquote')

    # problema objetivo: normal
    choice_list = soup.find('ul', class_='task-list')
    if choice_list:
        # get problem choices, obj and answer
        choices = []
        for index, item in enumerate(choice_list.find_all('li')):
            choice = convert.html2md(item)
            choices.append(choice)
            check_box = item.find('input').extract()
            if check_box.has_attr('checked'):
                kwargs['obj'] = index
                kwargs['answer'] = [choice]
        kwargs['choices'] = choices
        choice_list.decompose()

        if solution:
            kwargs['solution'] = convert.html2md(solution.extract())

        kwargs['statement'] = convert.html2md(soup)

        return Problem(**kwargs)

    # problema objetivo: V ou F
    prop_list = soup.find('ol', class_='task-list')
    if prop_list:
        true_props = []
        for index, item in enumerate(prop_list.find_all('li')):
            check_box = item.find('input').extract()
            if check_box.has_attr('checked'):
                true_props.append(index)
        kwargs['choices'], kwargs['answer'], kwargs['obj'] = \
            autoprops(true_props)

        if solution:
            kwargs['solution'] = convert.html2md(solution.extract())

        kwargs['statement'] = convert.html2md(soup)

        return Problem(**kwargs)

    # problema discursivo
    if solution:
        alist = solution.find('ul')
        if alist:
            answer = [convert.html2md(i) for i in alist.find_all('li')]
            kwargs['answer'] = answer
            alist.decompose()
        kwargs['solution'] = convert.html2md(solution.extract())

    kwargs['statement'] = convert.html2md(soup)

    return Problem(**kwargs)


def autoprops(true_props):
    # generate choices for T/F problems
    if not true_props:
        choices = [
            'Nenhuma'
            '1',
            '2',
            '3',
            '4',
        ]
        obj = 1
    if true_props == [0]:
        choices = [
            '1',
            '2',
            '1 e 2',
            '1, 2 e 3',
            '1, 2 e 3'
        ]
        obj = 1
    if true_props == [1]:
        choices = [
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3'
        ]
        obj = 1
    if true_props == [2]:
        choices = [
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3'
        ]
        obj = 1
    if true_props == [3]:
        choices = [
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3'
        ]
        obj = 1
    if true_props == [0, 1]:
        choices = [
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3'
        ]
        obj = 1
    if true_props == [0, 2]:
        choices = [
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3'
        ]
        obj = 1
    if true_props == [0, 3]:
        choices = [
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3'
        ]
        obj = 1
    if true_props == [1, 0]:
        choices = [
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3'
        ]
        obj = 1
    if true_props == [1, 2]:
        choices = [
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3'
        ]
        obj = 1
    if true_props == [1, 3]:
        choices = [
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3'
        ]
        obj = 1
    if true_props == [2, 0]:
        choices = [
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3'
        ]
        obj = 1
    if true_props == [2, 1]:
        choices = [
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3'
        ]
        obj = 1
    if true_props == [2, 3]:
        choices = [
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3'
        ]
        obj = 1
    if true_props == [3, 0]:
        choices = [
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3'
        ]
        obj = 1
    if true_props == [3, 1]:
        choices = [
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3'
        ]
        obj = 1
    if true_props == [3, 2]:
        choices = [
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3'
        ]
        obj = 1
    if true_props == [0, 1, 2]:
        choices = [
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2, 3 e 3'
        ]
        obj = 1
    if true_props == [1, 2, 4]:
        choices = [
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2, 3 e 3'
        ]
        obj = 1
    if true_props == [0, 2, 3]:
        choices = [
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2, 3 e 3'
        ]
        obj = 1
    if true_props == [1, 2, 3]:
        choices = [
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2 e 3',
            '1, 2, 3 e 3'
        ]
        obj = 1
    if true_props == [0, 1, 2, 3]:
        choices = [
            '1, 2 e 3',
            '1, 2 e 4',
            '1, 3 e 4',
            '2, 3 e 4',
            '1, 2, 3 e 3'
        ]
        obj = 4
    answer = choices[obj]
    return choices, answer, obj
