#
# DOME - Gabriel Braun, 2021
#

# TODO:
# - Gerar o "elements"
# - Usar o GitHub Actions para rodar esse script automaticamente
# - Automatic options with \pu{} regex


# IMPORTS

from enum import auto
import attr
from json import dump as json_dump
import sys
import os
import re
from shutil import move, copy, SameFileError
import pandas as pd
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
    html = MD.convert(content)
    return BeautifulSoup(html, 'html.parser')


def html2md(content):
    # convert md to html using pandoc and parse as soup
    return convert_text(
        content, 'md',
        format='html+tex_math_dollars+raw_tex',
    )


def md2latex(content):
    # convert html string to latex using pandoc
    return convert_text(
        str(content), 'latex',
        format='markdown+tex_math_dollars+raw_tex',
    ).replace('\\tightlist\n', '').rstrip()


def latex2pdf(tex, file_name):
    # convert tex string to pdf
    cwd = os.getcwd()
    os.chdir("template")

    with open('1A.tex', 'w') as f:
        f.write(tex)

    run(
        ["pdflatex", "-interaction=nonstopmode", f"{file_name}.tex"],
        stdout=DEVNULL
    )

    # clear output files
    for ext in ['.tex', '.aux', '.log', '.out']:
        os.remove(file_name + ext)

    move(f"{file_name}.pdf", f"../archive/{file_name}.pdf")

    os.chdir(cwd)


#
# LATEX INTEGRATION FUNCTIONS
#

PU_CMD = re.compile(r'\\pu\{\s*([\deE,.]*)\s*(.*)\s*\}')
UNIT_EXP = re.compile(r'[\+\-]\d+')


def pu2siunitx(match_obj):
    # convert \pu command to \unit, \num or \qty
    if match_obj.group(2) is None:  # number only
        return latex_cmd('num', [match_obj.group(1)])

    unit = re.sub(
        UNIT_EXP, lambda x: f"^{{{x.group(0)}}}", match_obj.group(2)
    )

    if match_obj.group(1) is None:  # dimension ony
        return latex_cmd('unit', [unit])

    return latex_cmd('qty', [match_obj.group(1), unit])


def latex_dim(content):
    # converts all \pu commands to \unit, \num or \qty
    return re.sub(PU_CMD, pu2siunitx, content)


def latex_cmd(cmd, content=[]):
    if content:
        latex_args = ''.join(f'{{{arg}}}' for arg in content)
        return f'\\{cmd}{latex_args}'

    return f'\\{cmd}'


def latex_env(env, content):
    return f'\\begin{{{env}}}\n{content}\n\\end{{{env}}}'


def latex_section(content, level=0, newpage=False):
    if not content:
        return ''

    newpage_cmd = latex_cmd('newpage') if newpage else ''
    return newpage_cmd + latex_cmd(level*'sub'+'section*', [content]) + '\n'


def list2latex(env, items, cols=1, auto_cols=False, resume=False):
    if auto_cols:
        min_length = min([len(i) for i in items])
        if min_length < 30:
            cols = 3

    resume = 'resume=true' if resume else ''
    content = '\n'.join([f'\\item {i}\n' for i in items])
    return latex_env(env, f'[{resume}]({cols}){content}')


#
# DATA CLASS
#


datasets = ['elements', 'thermochem']
frames = [pd.read_csv(
    f'database/data/{d}.csv', sep=';') for d in datasets]
DATA = pd.concat(frames)


@attr.s(frozen=True)
class Data(object):
    id: str = attr.ib()
    name: str = attr.ib(init=False)
    symbol: str = attr.ib(init=False)
    value: str = attr.ib(init=False)
    unit: str = attr.ib(init=False)

    def __attrs_post_init__(self):
        col = DATA.loc[DATA.id == self.id]

        if col.empty:
            print(f"O dado '{self.id}' não foi cadastrado!")
            sys.exit(f'Cadastre os dados necessários e tente denovo.')

        for prop in ['name', 'symbol', 'value', 'unit']:
            object.__setattr__(self, prop, col[prop].item().strip())

    def aslatex(self):
        # return data in sunitx format
        return f"${self.symbol} = {latex_cmd('qty', [self.value, self.unit])}$"

#
# PROBLEM CLASS
#


@attr.s()
class Problem(object):
    path = attr.ib()
    id: str = attr.ib(init=False)
    date: str = attr.ib(init=False)
    statement = attr.ib(init=False)
    answer: str = attr.ib(init=False)
    obj = attr.ib(default=-1)
    is_obj: bool = attr.ib(default=False)
    prop: bool = attr.ib(default=False)
    choices = attr.ib(factory=list)
    data = attr.ib(factory=list)

    def __attrs_post_init__(self):
        # get YAML data and contents
        object.__setattr__(self, 'id', self.path.stem)
        object.__setattr__(self, 'date', os.path.getmtime(self.path))
        pfile = load(self.path)
        soup = md2soup(pfile.content)

        for prop in ['answer']:
            if prop in pfile:
                object.__setattr__(self, prop, pfile[prop])

        if 'data' in pfile:
            self.data = [Data(i) for i in pfile['data']]

        # change images direcory to images folder
        for img in soup.find_all('img'):
            img['src'] = os.path.join(
                "./images/", os.path.basename(img['src']))

        # get problem choices and ansewer, if objective
        # FIXME: remove listitem tags (remendado com .text)
        task_list = soup.find('ul', class_='task-list')
        if task_list:
            self.is_obj = True
            for index, item in enumerate(task_list.find_all('li')):
                check_box = item.find('input').extract()
                if check_box.has_attr('checked'):
                    self.obj = index
                    object.__setattr__(self, 'answer', item.text.strip())
                self.choices.append(item.text.strip())
            task_list.decompose()

        # get problem answer
        # FIXME: remove blockquote tags (remendado com .text)
        answer = soup.find('blockquote')
        if answer:
            object.__setattr__(self, 'answer', html2md(answer.text))
            answer.decompose()

        # get problem statement
        self.statement = html2md(soup)

        return self

    def asdict(self):
        return attr.asdict(self)

    def latex_statement(self):
        return md2latex(self.statement)

    def latex_data(self):
        # return data as latex list with header
        if not self.data:
            return ''
        latex_datalist = list2latex('datalist',
                                    [d.aslatex() for d in self.data], cols=2
                                    )
        return latex_section('Dados', 1) + latex_datalist

    def latex_choices(self):
        # return choices as latex list
        if not self.is_obj:
            return ''
        return list2latex('choices', self.choices, auto_cols=True)

    def latex_answer(self):
        # return choices as latex list
        if self.is_obj:
            return latex_cmd('MiniBox', content=[chr(65 + self.obj)])
        else:
            return md2latex(self.answer)

    def aslatex(self):
        # return problem as latex
        p = self.latex_statement() + self.latex_choices() + self.latex_data()
        return latex_env('problem', p)


@attr.s(frozen=True)
class ProblemSet(object):
    title = attr.ib()
    problems = attr.ib()

    def latex_statements(self):
        if not self.problems:
            return ''

        statements = '\n'.join([p.aslatex() for p in self.problems])
        return latex_section(self.title) + statements

    def latex_answers(self):
        if not self.problems:
            return ''

        cols = 6 if all([p.is_obj for p in self.problems]) else 2
        answers = [p.latex_answer() for p in self.problems]
        return latex_section(self.title, level=1) + list2latex('answers', answers, cols=cols)

#
# TOPIC CLASS
#


@attr.s(frozen=True)
class Subtopic(object):
    id: str = attr.ib()
    title: str = attr.ib()
    items = attr.ib()
    abilities = attr.ib()


@attr.s(frozen=True)
class Topic(object):
    path = attr.ib()
    id: str = attr.ib(init=False)
    title: str = attr.ib(default="")
    subtopics = attr.ib(factory=list)
    problems = attr.ib(factory=list)

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

TOPIC_FILE = re.compile('\d[A-Z].md')
PROBLEM_FILE = re.compile('\d[A-Z]\d{2}.md')


def get_file_paths(db_path):
    # get the path of all problems and topics
    topic_files = []
    problem_files = []

    for root, _, files in os.walk(db_path):
        for f in files:
            path = Path(os.path.join(root, f))
            # problems
            if PROBLEM_FILE.match(path.name):
                problem_files.append(path)
            # topics
            elif TOPIC_FILE.match(path.name):
                topic_files.append(path)
            # images
            elif path.suffix in ['.jpg', '.jpeg', '.svg', '.pdf', '.tex']:
                try:
                    copy(path, os.path.join(db_path, 'images', path.name))
                except SameFileError:
                    pass

    return topic_files, problem_files


@attr.s(frozen=True)
class Arsenal(object):
    topics = attr.ib(factory=list)
    problems = attr.ib(factory=list)

    def read_dir(self, db_path):
        topic_files, problem_files = get_file_paths(db_path)

        for path in topic_files:
            self.topics.append(Topic(path))

        for path in problem_files:
            self.problems.append(Problem(path))

        json_file = os.path.join(db_path, 'problems.json')
        with open(json_file, 'w') as f:
            json_dump(self.asdict(), f, indent=2, ensure_ascii=False)

        return self

    def asdict(self):
        filters = attr.filters.exclude(
            attr.fields(Topic).path,
            attr.fields(Problem).path,
            attr.fields(Problem).date
        )
        return attr.asdict(self, filter=filters)

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
                latex2pdf(l.aslatex(), topic.id)


#
# PDF LIST CLASS
#

@attr.s(frozen=True)
class List(object):
    id: str = attr.ib()
    title: str = attr.ib()
    problem_sets = attr.ib()
    affiliation: str = attr.ib(default="Colégio e Curso Pensi, Química")
    author: str = attr.ib(default="Gabriel Braun")
    logo: str = attr.ib(default="pensi")

    def aslatex(self, template='braun, twocolumn, DIV=calc'):
        doc_class = latex_cmd(f'documentclass[{template}]', ['braun'])

        doc_config = latex_cmd('title', [self.title]) + latex_cmd('affiliation', [
            self.affiliation]) + latex_cmd('author', [self.author]) + latex_cmd('logo', [self.logo])

        doc_answers = latex_section('Gabarito', newpage=True)
        doc_problems = ''
        for pset in self.problem_sets:
            doc_problems += pset.latex_statements()
            doc_answers += pset.latex_answers()

        return doc_class + doc_config + latex_env('document', latex_cmd('maketitle') + latex_dim(doc_problems + doc_answers))


#
# MAIN
#


def main():
    data = Arsenal().read_dir("database")
    data.aspdf(['1A'])


if __name__ == "__main__":
    main()
