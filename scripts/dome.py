#
# DOME - Gabriel Braun, 2021
#

# TODO:
# - Gerar o "elements"
# - Usar o GitHub Actions para rodar esse script automaticamente


# REQUIREMENTS

import os
import re

import attr
from attr import frozen, field, Factory, asdict, fields

import csv
import pickle
from json import dump as json_dump

from sys import exit
from shutil import move, copy, SameFileError
from subprocess import run, DEVNULL
from pathlib import Path

from frontmatter import load
from bs4 import BeautifulSoup
from pypandoc import convert_text
from markdown import Markdown

#
# CONVERSION
#

MD = Markdown(extensions=['pymdownx.tasklist'])


def md2soup(content):
    return BeautifulSoup(MD.convert(content), 'html.parser')


def html2md(content):
    # convert md to html using pandoc and parse as soup
    return convert_text(content, 'md', format='html+tex_math_dollars+raw_tex')


def md2tex(content):
    # convert html string to tex using pandoc
    return convert_text(
        str(content), 'tex',
        format='markdown+tex_math_dollars+raw_tex',
    )


def tex2pdf(tex, filename, path=''):
    # convert tex string to pdf
    cwd = os.getcwd()
    os.chdir('template')

    with open('1A.tex', 'w') as f:
        f.write(tex)

    run(
        ['pdflatex', '-interaction=nonstopmode', f'{filename}.tex'],
        stdout=DEVNULL
    )

    # clear output files
    for ext in ['.tex', '.aux', '.log', '.out']:
        os.remove(filename + ext)

    os.chdir(cwd)

    move(
        os.path.join('template', f'{filename}.pdf'),
        os.path.join(path, f'{filename}.pdf')
    )


#
# LATEX INTEGRATION FUNCTIONS
#

PU_CMD = re.compile(r'\\pu\{\s*([\deE\,\.\+\-]*)\s*([\/\\\s\w\d\.\+\-]*)\s*\}')
UNIT_EXP = re.compile(r'[\+\-]\d+')


def qty(num, unit):
    # convert \pu command to \unit, \num or \qty
    if not unit:  # number only
        return tex_cmd('num', [num])

    formated_unit = re.sub(UNIT_EXP, lambda x: f'^{{{x.group(0)}}}', unit)

    if not num:  # unit ony
        return tex_cmd('unit', [formated_unit])

    return tex_cmd('qty', [num, formated_unit])


def pu2qty(content):
    # converts all \pu commands to \unit, \num or \qty
    return re.sub(PU_CMD, lambda x: qty(x.group(1), x.group(2)), content)


def tex_cmd(cmd, content=[]):
    if content:
        tex_args = ''.join(f'{{{arg}}}' for arg in content)
        return f'\\{cmd}{tex_args}'

    return f'\\{cmd}'


def tex_env(env, content):
    return f'\n\n\\begin{{{env}}}\n{content}\n\\end{{{env}}}\n'


def tex_section(content, level=0, newpage=False, numbered=True):
    if not content:
        return ''

    newpage_cmd = tex_cmd('newpage') if newpage else ''
    section_cmd = level*'sub' + ('section' if numbered else 'section*')
    return newpage_cmd + tex_cmd(section_cmd, [content]) + '\n'


TEX_LEN = re.compile(r'\\\w+|[\w\d\=\%]|\d')


def list2tex(env, items, cols=0, auto_cols=False):
    if auto_cols:
        max_length = max([len(re.findall(TEX_LEN, i)) for i in items])
        if max_length < 4:
            cols = 5
        elif max_length < 7:
            cols = 3
        elif max_length < 20:
            cols = 2

    cols = f'({cols})' if cols else ''
    content = '\n'.join([f'\\item {i}' for i in items])
    return tex_env(env, f'{cols}\n{content}')


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
        'Temperatura de fusão do ', 'T_\\text{fus}', '\degree C'
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
        return f'${self.symbol} = {qty(self.value, self.unit)}$'


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

#
# PROBLEM CLASS
#


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
        return md2tex(self.statement) + self.tex_choices()

    def tex_data(self):
        # return data as tex list with header
        if not self.data:
            return ''
        dlist = list2tex('datalist', [d.astex() for d in self.data])
        return tex_section('Dados', level=2, numbered=False) + dlist

    def tex_choices(self):
        # return choices as tex list
        if not self.is_obj():
            return ''
        tex_choices = [md2tex(c) for c in self.choices]
        return list2tex('choices', tex_choices, auto_cols=True)

    def tex_answer(self):
        if not self.answer:
            return '-'
        if self.is_obj():
            return tex_cmd('MiniBox', content=[chr(65 + self.obj)])
        if len(self.answer) == 1:
            return self.answer[0]
        return list2tex('answers', self.answer)

    def astex(self):
        # return problem as tex
        p = self.tex_statement() + self.tex_data()
        return tex_env('problem', f'[{self.id}]{p}')


@frozen
class ProblemSet:
    title: str
    problems: list[Problem]

    def tex_statements(self):
        if not self.problems:
            return ''

        statements = '\n'.join([p.astex() for p in self.problems])
        return tex_section(self.title) + statements

    def tex_answers(self):
        if not self.problems:
            return ''

        header = tex_section(self.title, level=1)
        answers = [p.tex_answer() for p in self.problems]

        if all([p.is_obj() for p in self.problems]):
            return header + list2tex('checks', answers, cols=5)

        return header + list2tex('answers', answers)


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


def file2problem(path):
    props = {}
    # get YAML data and contents
    props['id'] = path.stem

    pfile = load(path)
    soup = md2soup(pfile.content)

    # get problem data
    if 'data' in pfile:
        props['data'] = DATA.filter(pfile['data'])

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
            choice = html2md(item)
            choices.append(choice)
            check_box = item.find('input').extract()
            if check_box.has_attr('checked'):
                props['obj'] = index
                props['answer'] = [choice]
        props['choices'] = choices
        choice_list.decompose()

        if solution:
            props['solution'] = html2md(solution.extract())

        props['statement'] = html2md(soup)

        return Problem(**props)

    # problema objetivo: V ou F
    prop_list = soup.find('ol', class_='task-list')
    if prop_list:
        true_props = []
        for index, item in enumerate(prop_list.find_all('li')):
            check_box = item.find('input').extract()
            if check_box.has_attr('checked'):
                true_props.append(index)
        props['choices'], props['answer'], props['obj'] = autoprops(true_props)

        if solution:
            props['solution'] = html2md(solution.extract())

        props['statement'] = html2md(soup)

        return Problem(**props)

    # problema discursivo
    if solution:
        alist = solution.find('ul')
        if alist:
            props['answer'] = [html2md(i) for i in alist.find_all('li')]
            alist.decompose()
        props['solution'] = html2md(solution.extract())

    props['statement'] = html2md(soup)

    return Problem(**props)


#
# TOPIC CLASS
#


@frozen
class Subtopic:
    id: str
    title: str
    items: list[str]
    abilities: list[str]


@frozen
class Topic:
    path: str
    id: str = field(init=False)
    title: str = field(init=False)
    problems: dict = field(init=False)
    subtopics: list = Factory(list)

    def __attrs_post_init__(self):
        # get YAML data and contents
        object.__setattr__(self, 'id', self.path.stem)
        tfile = load(self.path)
        soup = md2soup(tfile.content)

        for prop in ['title', 'problems']:
            if prop in tfile:
                object.__setattr__(self, prop, tfile[prop])

        # get subtopics items and abilities from HTML tags
        all_subtopics = soup.find_all('h1')
        all_items = soup.find_all('ol')
        all_abilities = soup.find_all('ul')

        for index, subtopic in enumerate(all_subtopics):
            subtopic_id = f'{self.id}.{index+1}'
            subtopic_title = subtopic.text
            subtopic_items = [
                html2md(i) for i in all_items[index].find_all('li')
            ]
            subtopic_abilities = [
                html2md(a) for a in all_abilities[index].find_all('li')
            ]

            self.subtopics.append(
                Subtopic(subtopic_id, subtopic_title,
                         subtopic_items, subtopic_abilities)
            )

        return self


#
# ARSENAL CLASS
#

@frozen
class Arsenal:
    path: str
    topics: list[Topic] = Factory(list)
    problems: list[Problem] = Factory(list)

    def dump(self):
        # dump contents to pickle
        pickle_file = os.path.join(self.path, 'arsenal.p')
        with open(pickle_file, 'wb') as f:
            pickle.dump(self, f)

        # dump contents to json
        filters = attr.filters.exclude(
            fields(Topic).path,
        )

        json_file = os.path.join(self.path, 'arsenal.json')
        with open(json_file, 'w') as f:
            json_dump(
                asdict(self, filter=filters), f, indent=2, ensure_ascii=False
            )

    def filter(self, title, problem_ids):
        # get ProblemSet from list of ids
        problems = sorted([
            problem for problem in self.problems if problem.id in problem_ids
        ], key=lambda p: problem_ids.index(p.id))

        return ProblemSet(title, problems)

    def aspdf(self, topic_ids):
        # compile list pdf for lists with id in topic_ids
        for topic in self.topics:
            if topic.id in topic_ids:
                psets = [self.filter(t, p) for t, p in topic.problems.items()]

                l = List(topic.id, topic.title, psets)
                print('compiling latex list')
                tex2pdf(l.astex(), topic.id, path='archive')


def copyr(loc, dest):
    try:
        copy(loc, dest)
    except SameFileError:
        pass


def get_file_paths(db_path):
    # get the path of all problems and topics
    topic_files = []
    problem_files = []

    for root, _, files in os.walk(os.path.join(db_path, 'topics')):
        for f in files:
            path = Path(os.path.join(root, f))
            if path.suffix == '.md':
                topic_files.append(path)

    for root, _, files in os.walk(os.path.join(db_path, 'problems')):
        for f in files:
            path = Path(os.path.join(root, f))
            # problems
            if path.suffix == '.md':
                problem_files.append(path)
            # topics
            elif path.suffix in ['.jpg', '.jpeg', '.svg', '.pdf', '.tex']:
                copyr(path, os.path.join(db_path, 'images', path.name))

    return topic_files, problem_files


def load_arsenal(path):
    # generate arsenal by walking on directory
    if not os.path.exists(path):
        exit(f"O diretório '{path}' não existe!")

    topic_files, problem_files = get_file_paths(path)

    topics = [Topic(t) for t in topic_files]
    problems = [file2problem(p) for p in problem_files]

    ars = Arsenal(path, topics, problems)

    ars.dump()

    # pickle_file = os.path.join(path, 'arsenal.p')
    # if os.path.exists(pickle_file):
    #     with open(pickle_file, 'rb') as f:
    #         print("Arquivo '%s' carregado" % pickle_file)
    #         return pickle.load(f)
    return ars

#
# PDF LIST CLASS
#


@frozen
class List:
    id: str
    title: str
    problem_sets: dict
    affiliation: str = "Colégio e Curso Pensi, Coordenação de Química"
    author: str = "Gabriel Braun"
    logo: str = "pensi"

    def astex(self, template='braun, twocolumn'):
        # return tex file for compiling list as pdf
        doc_preamble = tex_cmd(f'documentclass[{template}]', ['braun'])
        for prop in ['title', 'affiliation', 'author', 'logo']:
            doc_preamble += '\n' + tex_cmd(prop, [getattr(self, prop)])

        doc_preamble += '\n' + tex_cmd('dbpath', ['../database'])

        doc_answers = tex_section('Gabarito', newpage=False)
        doc_problems = '\n'
        for pset in self.problem_sets:
            doc_problems += pset.tex_statements()
            doc_answers += pset.tex_answers()

        return doc_preamble + tex_env('document', tex_cmd('maketitle') + pu2qty(doc_problems + doc_answers))


#
# MAIN
#


def main():
    data = load_arsenal('database')
    data.aspdf(['1A'])


if __name__ == "__main__":
    main()
