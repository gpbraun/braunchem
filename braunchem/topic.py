#
# DOME - Gabriel Braun, 2021
#

import os

import dataclasses

from decimal import Decimal
from quantities import Table, Quantity, decimal_to_sci_string
from attr import frozen, Factory, asdict, filters, fields

import json

import sys
from pathlib import Path, PosixPath

from problem import Problem, ProblemSet, files2problemset
from multiprocessing import Pool

from frontmatter import load

import convert
import latex


@frozen
class Subtopic:
    id_: str
    title: str
    # items: list[str]
    # abilities: list[str]


@frozen
class Topic:
    id_: str
    area: str = ''
    title: str = 'Química'
    author: str = 'Gabriel Braun'
    affiliation: str = 'Colégio e Curso Pensi, Coordenação de Química'
    template: str = 'braun, twocolumn'
    contents: str = ''
    subtopics: list = Factory(list)
    problems: list = Factory(list)

    def __lt__(self, other):
        return self.id_ < other.id_

    def tex_data(self):
        constants = sum([p.tex_constants() for p in self.problems])
        elements = []
        for p in self.problems:
            if p.elements():
                elements += p.elements()

        if not constants.data and not elements:
            return ''

        header = latex.section('Dados', level=0)

        el_header = latex.section('Elementos', level=1, numbered=False)
        elements_table = el_header + latex.cmd(
            'MolTable', ','.join(elements)) if elements else ''

        const_header = latex.section('Constantes', level=1, numbered=False)
        constants_list = const_header \
            + constants.tex_display() if constants else ''

        return header + constants_list + elements_table + latex.cmd('bigskip')

    def tex_statements(self, print_solutions):
        # return statements in latex format
        if not self.problems:
            return ''

        if len(self.problems) == 1:
            # se há apenas um problemset, não coloca título
            pset = self.problems[0]
            problem_num = len(pset)
            if not problem_num:
                return ''

            points = 10/problem_num
            return pset.tex_statements(
                points=points, print_solutions=print_solutions
            )

        problem_num = sum([len(pset) for pset in self.problems])
        if not problem_num:
            return ''

        points = 10/problem_num
        statements = ''
        newpage = False
        for pset in self.problems:
            statements += pset.tex_statements(
                pset.title, problem_num, print_solutions,
                newpage=newpage
            )
            newpage = True

        return latex.pu2qty(statements)

    def tex_answers(self):
        # return statements in latex format
        header = latex.section('Gabarito', level=0, newpage=True)
        if len(self.problems) == 1:
            # se há apenas um problemset, não coloca título
            pset = self.problems[0]
            return header + pset.tex_answers()

        answers = ''.join([
            pset.tex_answers(pset.title) for pset in self.problems
        ])
        return header + latex.cmd('small') + answers

    def latex(self, print_level=1):
        # return tex file for compiling problem sheet as pdf
        preamble = latex.cmd(f'documentclass[{self.template}]', ['braun'])

        for prop in ['title', 'affiliation', 'author']:
            preamble += '\n' + latex.cmd(prop, [getattr(self, prop)])

        if not print_level:
            # print_level = 0: sem respostas e sem soluções
            data = self.tex_data()
            statements = self.tex_statements(print_solutions=False)
            return latex.document(preamble, latex.pu2qty(data + statements))

        answers = self.tex_answers()

        if print_level == 2:
            # print_level = 2: respostas e soluções
            statements = self.tex_statements(print_solutions=True)
            return latex.document(preamble, latex.pu2qty(answers + statements))

        # print_level = 1: apenas respostas ao final
        statements = self.tex_statements(print_solutions=False)
        return latex.document(preamble, latex.pu2qty(statements + answers))

    def generate_pdf(self, file_name='', print_level=1):
        if not file_name:
            file_name = self.id_

        convert.tex2pdf(
            self.latex(print_level),
            file_name,
            tmp_path=f'temp/{self.area}/{self.id_}',
            out_path=f'out/{self.area}'
        )


def topic2pdf(topic):
    return topic.generate_pdf()


def file2topic(args):
    path, problemset = args
    kwargs = {}
    # get YAML data and contents
    id_ = path.stem
    kwargs['id_'] = id_
    kwargs['area'] = path.parent.stem

    tfile = load(path)
    kwargs['contents'] = tfile.content
    soup = convert.md2soup(tfile.content)

    for p in ['title', 'author', 'affiliation', 'template']:
        if p in tfile:
            kwargs[p] = tfile[p]

    if 'problems' in tfile:
        kwargs['problems'] = [
            problemset.filter(
                'id_', ids, title=t, id_=f'{id_}{i+1}'
            )
            for i, (t, ids) in enumerate(tfile['problems'].items())
        ]

    # get subtopics items and abilities from HTML tags
    all_subtopics = soup.find_all('h1')
    # all_items = soup.find_all('ol')
    # all_abilities = soup.find_all('ul')

    kwargs['subtopics'] = []

    for index, subtopic in enumerate(all_subtopics):
        subtopic_id = f'{id_}.{index+1}'
        subtopic_title = subtopic.text
        # subtopic_items = [
        #     convert.html2md(i) for i in all_items[index].find_all('li')
        # ]
        # subtopic_abilities = [
        #     convert.html2md(a) for a in all_abilities[index].find_all('li')
        # ]

        kwargs['subtopics'].append(
            Subtopic(
                subtopic_id,
                subtopic_title,
                # subtopic_items,
                # subtopic_abilities
            )
        )

    return Topic(**kwargs)


@frozen
class Arsenal:
    problems: ProblemSet
    topics: list[Topic] = Factory(list)

    def dump(self, path):
        # dump contents to json
        flter = filters.exclude(
            fields(Arsenal).problems
        )

        json_file = os.path.join(path, 'arsenal.json')

        with open(json_file, 'w') as f:
            json.dump(
                asdict(self, filter=flter), f, indent=2,
                ensure_ascii=False, cls=TopicEncoder
            )

    def generate_pdfs(self):
        pool = Pool()
        pool.map(topic2pdf, self.topics)


def get_file_paths(db_path):
    # get the path of all problems and topics
    problem_path = Path(os.path.join(db_path, 'problems'))
    topic_path = Path(os.path.join(db_path, 'topics'))

    problem_files = []
    topic_files = []

    for root, _, files in os.walk(problem_path):
        for f in files:
            path = Path(os.path.join(root, f))
            dir_ = Path(root).relative_to(problem_path).parent

            # problems
            if path.suffix == '.md':
                problem_files.append(path)

            elif path.suffix in ['.svg', '.png']:
                # figure
                convert.copy_r(
                    path,
                    f'database/images/{dir_}/{path.name}'
                )

            elif path.suffix == '.tex':
                # tikz figures
                dir_ = Path(root).relative_to(problem_path).parent
                convert.tikz2svg(
                    path,
                    tmp_path=f'temp/images/{dir_}/{path.stem}',
                    out_path=f'database/images/{dir_}'
                )

    for root, _, files in os.walk(topic_path):
        for f in files:
            path = Path(os.path.join(root, f))
            if path.suffix == '.md':
                topic_files.append(path)

    return problem_files, topic_files


class TopicEncoder(json.JSONEncoder):
    """Encoder para converter um `Table` em `json`."""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return decimal_to_sci_string(obj)

        if isinstance(obj, Table):
            return obj.quantities

        if isinstance(obj, Quantity):
            d = {'__classname__': type(obj).__name__}
            d.update(dataclasses.asdict(obj))
            return d

        if isinstance(obj, PosixPath):
            return str(obj)

        if isinstance(obj, Problem):
            d = {'__classname__': type(obj).__name__}
            d.update(dataclasses.asdict(obj))
            return d

        if isinstance(obj, ProblemSet):
            d = {'__classname__': type(obj).__name__}
            d.update(dataclasses.asdict(obj))
            return d

        return super(TopicEncoder, self).default(obj)


def load_arsenal(path):
    # generate arsenal by walking on directory
    if not os.path.exists(path):
        sys.exit(f"O diretório '{path}' não existe!")

    print('Carregando diretórios...')
    problem_files, topic_files = get_file_paths(path)

    print('Carregando base de dados com problemas...')
    problem_set = files2problemset(problem_files)

    print('Gerando tópicos...')
    pool = Pool()
    topics = pool.map(file2topic, [(t, problem_set) for t in topic_files])

    ars = Arsenal(problem_set, sorted(topics))

    ars.dump(path)

    return ars
