#
# DOME - Gabriel Braun, 2021
#

import os

from attr import frozen, Factory, asdict, filters, fields

from json import dump as json_dump

from sys import exit
from pathlib import Path

from problem import Problem, ProblemSet, links2problemset, files2problemset
from multiprocessing import Pool

from frontmatter import load

import convert
import latex


@frozen
class Subtopic:
    id_: str
    title: str
    items: list[str]
    abilities: list[str]


@frozen
class Topic:
    id_: str
    area: str = ''
    title: str = 'Química'
    author: str = 'Gabriel Braun'
    affiliation: str = 'Colégio e Curso Pensi, Coordenação de Química'
    template: str = 'braun, twocolumn'
    problems: dict = Factory(dict)
    subtopics: list = Factory(list)

    def latex(self, answers=True, solution=False):
        # return tex file for compiling problem sheet as pdf
        preamble = latex.cmd(f'documentclass[{self.template}]', ['braun'])

        for prop in ['title', 'affiliation', 'author']:
            preamble += '\n' + latex.cmd(prop, [getattr(self, prop)])

        ans = latex.section('Gabarito', newpage=True)
        problems = '\n'
        for title, pset in self.problems.items():
            problems += pset.tex_statements(title, solution)
            ans += pset.tex_answers(title)

        body = latex.pu2qty(problems + ans if answers else problems)

        return preamble + latex.env('document', latex.cmd('maketitle') + body)

    def generate_pdf(self, name='', **kwargs):
        if not name:
            name = self.id_

        convert.tex2pdf(
            self.latex(**kwargs),
            name,
            tmp_path=f'temp/{self.area}',
            out_path=f'archive/{self.area}'
        )
        return f'{self.id_} PDF generated!'


def links2topic(cur, id_, links, **kwargs):
    # gera o simulado a partir dos dados
    print('Carregando problemas...')
    problem_set = links2problemset(cur, links)
    return Topic(id_, problems={'': problem_set}, **kwargs)


def file2topic(args):
    path, problemset = args
    kwargs = {}
    # get YAML data and contents
    id_ = path.stem
    kwargs['id_'] = id_
    kwargs['area'] = path.parent.stem

    tfile = load(path)
    soup = convert.md2soup(tfile.content)

    for p in ['title', 'author', 'affiliation', 'template']:
        if p in tfile:
            kwargs[p] = tfile[p]

    if 'problems' in tfile:
        kwargs['problems'] = {
            t: problemset.filter(ids) for t, ids in tfile['problems'].items()
        }

    # get subtopics items and abilities from HTML tags
    all_subtopics = soup.find_all('h1')
    all_items = soup.find_all('ol')
    all_abilities = soup.find_all('ul')

    kwargs['subtopics'] = []

    for index, subtopic in enumerate(all_subtopics):
        subtopic_id = f'{id_}.{index+1}'
        subtopic_title = subtopic.text
        subtopic_items = [
            convert.html2md(i) for i in all_items[index].find_all('li')
        ]
        subtopic_abilities = [
            convert.html2md(a) for a in all_abilities[index].find_all('li')
        ]

        kwargs['subtopics'].append(
            Subtopic(
                subtopic_id,
                subtopic_title,
                subtopic_items,
                subtopic_abilities
            )
        )

    return Topic(**kwargs)


def topic2pdf(topic):
    return topic.generate_pdf()


@frozen
class Arsenal:
    problems: ProblemSet
    topics: list[Topic] = Factory(list)

    def dump(self, path):
        # dump contents to json
        flter = filters.exclude(
            fields(Problem).path,
            fields(Arsenal).problems
        )

        json_file = os.path.join(path, 'arsenal.json')

        with open(json_file, 'w') as f:
            json_dump(
                asdict(self, filter=flter), f, indent=2, ensure_ascii=False
            )

    def generate_pdfs(self):
        pool = Pool()
        pool.map(topic2pdf, self.topics)


def get_file_paths(db_path):
    # get the path of all problems and topics
    problem_files = []
    topic_files = []

    for root, _, files in os.walk(os.path.join(db_path, 'problems')):
        for f in files:
            path = Path(os.path.join(root, f))
            # problems
            if path.suffix == '.md':
                problem_files.append(path)

    for root, _, files in os.walk(os.path.join(db_path, 'topics')):
        for f in files:
            path = Path(os.path.join(root, f))
            if path.suffix == '.md':
                topic_files.append(path)

    return problem_files, topic_files


def load_arsenal(path):
    # generate arsenal by walking on directory
    if not os.path.exists(path):
        exit(f"O diretório '{path}' não existe!")

    problem_files, topic_files = get_file_paths(path)

    print('Carregando base de dados com problemas...')
    problem_set = files2problemset(problem_files)

    print('Gerando tópicos...')
    pool = Pool()
    topics = pool.map(file2topic, [(t, problem_set) for t in topic_files])

    ars = Arsenal(problem_set, topics)

    ars.dump(path)

    return ars
