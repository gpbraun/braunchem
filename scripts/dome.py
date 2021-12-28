#
# DOME - Gabriel Braun, 2021
#

# TODO:
# - Gerar o "elements"
# -

# IMPORTS

from enum import auto
import attr
from json import dump as json_dump
import sys
import os
import re
import pandas as pd
from subprocess import run, DEVNULL
from pathlib import Path
from frontmatter import load
from bs4 import BeautifulSoup
from pypandoc import convert_text
from markdown import Markdown
from markdownify import markdownify


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

    os.replace(f"{file_name}.pdf", f"../archive/{file_name}.pdf")

    os.chdir(cwd)


#
# LATEX INTEGRATION FUNCTIONS
#

PU_CMD = re.compile(r'\\pu\{\s*([\deE,.]*)\s*(.*)\s*\}')
DIM_EXP = re.compile(r'[\+\-]\d+')


def pu2siunitx(match_obj):
    # convert \pu command to \unit, \num or \qty
    if match_obj.group(2) is None:  # number only
        return f'\\num{{{match_obj.group(1)}}}'

    dimension = re.sub(
        DIM_EXP, lambda x: f"^{{{x.group(0)}}}", match_obj.group(2)
    )

    if match_obj.group(1) is None:  # dimension ony
        return f'\\unit{{{dimension}}}'

    return f'\\qty{{{match_obj.group(1)}}}{{{dimension}}}'


def latex_dim(content):
    # converts all \pu commands to \unit, \num or \qty
    return re.sub(PU_CMD, pu2siunitx, content)


def latex_cmd(content, cmd):
    return f'\\{cmd}{{{content}}}'


def latex_env(content, env):
    return f'\\begin{{{env}}}\n{content}\n\\end{{{env}}}'


def latex_section(content, level=0):
    return f"\\{'sub'*level}section*{{{content}}}\n" if content else ''


def list2latex(items, env, cols=1, auto_cols=False, resume=False):
    if auto_cols:
        min_length = min([len(item) for item in items])
        if min_length < 30:
            cols = 3

    resume = 'resume=true' if resume else ''

    content = '\n'.join([f'\\item {item}\n' for item in items])
    return f'\\begin{{{env}}}[{resume}]({cols})\n{content}\n\\end{{{env}}}'


#
# DATA CLASS
#


data = ['elements', 'thermochem']
frames = [pd.read_csv(
    f'database/data/{dataset}.csv', sep=';') for dataset in data]
DATA = pd.concat(frames)


@attr.s()
class Data(object):
    id: str = attr.ib()
    name: str = attr.ib(init=False)
    symbol: str = attr.ib(init=False)
    value: str = attr.ib(init=False)
    unit: str = attr.ib(init=False)

    def __attrs_post_init__(self):
        col = DATA.loc[DATA.id == self.id]

        if col.empty:
            print(f'O dado "{self.id}" não foi cadastrado!')
            sys.exit(f'Cadastre os dados necessários e tente denovo.')

        for prop in ['name', 'symbol', 'value', 'unit']:
            object.__setattr__(self, prop, col[prop].item().strip())

    def aslatex(self):
        # print data in sunitx format
        return f"${self.symbol} = \\qty{{{self.value}}}{{{self.unit}}}$"

#
# PROBLEM CLASS
#


@attr.s()
class Problem(object):
    id: str = attr.ib()
    path: str = attr.ib(default="")
    statement = attr.ib(default="")
    answer: str = attr.ib(default="")
    obj: int = attr.ib(default=-1)
    is_obj: int = attr.ib(default=False)
    choices = attr.ib(factory=list)
    data = attr.ib(default=[])

    def read_file(self, root_path):
        # get YAML data and contents
        problem_path = os.path.join(root_path, f'{self.id}.md')
        problem_file = load(problem_path)
        soup = md2soup(problem_file.content)

        for prop in ['answer']:
            if prop in problem_file:
                object.__setattr__(self, prop, problem_file[prop])

        if 'data' in problem_file:
            self.data = [Data(data_id) for data_id in problem_file['data']]

        # change images direcory to images folder
        for img in soup.find_all('img'):
            img['src'] = os.path.join(
                "./images/", os.path.basename(img['src']))

        # get problem choices and ansewer, if objective
        # TODO: remove listitem tags
        task_list = soup.find('ul', class_='task-list')
        if task_list:
            self.is_obj = True
            for index, item in enumerate(task_list.find_all('li')):
                check_box = item.find('input').extract()
                if check_box.has_attr('checked'):
                    self.obj = index
                    self.answer = item.text.lstrip()
                self.choices.append(item.text.lstrip())
            task_list.decompose()

        # get problem answer
        # TODO: remove blockquote tags
        answer = soup.find('blockquote')
        if answer:
            self.answer = html2md(answer)
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
        data = list2latex(
            [data.aslatex() for data in self.data], 'datalist', cols=2
        )
        return latex_section('Dados', 1) + data

    def latex_choices(self):
        # return choices as latex list
        if not self.is_obj:
            return ''
        return list2latex(self.choices, 'choices', auto_cols=True)

    def latex_answer(self):
        # return choices as latex list
        if self.is_obj:
            return latex_cmd(chr(65 + self.obj), 'MiniBox')
        else:
            return md2latex(self.answer)

    def aslatex(self):
        # return problem in latex format
        p = self.latex_statement() + self.latex_choices() + self.latex_data()
        return latex_env(p, 'problem')


@attr.s(frozen=True)
class ProblemSet(object):
    problems = attr.ib()

    def latex_statements(self, header=''):
        if not self.problems:
            return ''

        statements = '\n'.join(
            [problem.aslatex() for problem in self.problems]
        )
        return latex_section(header) + statements

    def latex_answers(self, header=''):
        if not self.problems:
            return ''

        cols = 6 if all([problem.is_obj for problem in self.problems]) else 2

        answers = [problem.latex_answer() for problem in self.problems]

        return latex_section(header, level=1) + list2latex(answers, 'answers', cols=cols)

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
    id: str = attr.ib()
    title: str = attr.ib(default="")
    subtopics = attr.ib(factory=list)
    N1 = attr.ib(factory=list)
    N2 = attr.ib(factory=list)
    N3 = attr.ib(factory=list)

    def read_file(self, topic_path):
        # get YAML data and contents
        problem_path = os.path.join(topic_path, f'{self.id}.md')
        problem_file = load(problem_path)
        soup = md2soup(problem_file.content)

        for prop in ['title', 'N1', 'N2', 'N3']:
            if prop in problem_file:
                object.__setattr__(self, prop, problem_file[prop])

        # get subtopics items and abilities from HTML tags
        all_subtopics = soup.find_all('h1')
        all_items = soup.find_all('ol')
        all_abilities = soup.find_all('ul')

        for i, subtopic in enumerate(all_subtopics):
            subtopic_id = f'{self.id}.{i+1}'
            subtopic_title = subtopic.text
            subtopic_items = [
                html2md(item) for item in all_items[i].find_all('li')
            ]
            subtopic_abilities = [
                html2md(ability) for ability in all_abilities[i].find_all('li')
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


def get_file_paths(directory):
    # get the path of all problems and topics
    topic_files = []
    problem_files = []

    for root, _, files in os.walk(directory):
        for filename in files:
            if TOPIC_FILE.match(filename):
                topic_files.append((Path(filename).stem, root))
            elif PROBLEM_FILE.match(filename):
                problem_files.append((Path(filename).stem, root))
            # TODO: copy images to "images" folder

    return topic_files, problem_files


@attr.s(frozen=True)
class Arsenal(object):
    topics = attr.ib(factory=list)
    problems = attr.ib(factory=list)

    def read_dir(self, db_path):
        topic_files, problem_files = get_file_paths(db_path)

        for topic_id, path in topic_files:
            self.topics.append(Topic(topic_id).read_file(path))

        for problem_id, path in problem_files:
            self.problems.append(Problem(problem_id).read_file(path))

        json_file = os.path.join(db_path, 'problems.json')
        with open(json_file, 'w') as f:
            json_dump(self.asdict(), f, indent=2, ensure_ascii=False)

        return self

    def asdict(self):
        return attr.asdict(self)

    def filter(self, problem_ids):
        # get ProblemSet from list of ids
        if not problem_ids:
            return ProblemSet([])

        problems = sorted([
            problem for problem in self.problems if problem.id in problem_ids
        ], key=lambda p: problem_ids.index(p.id))

        return ProblemSet(problems)

    def aspdf(self, topic_ids):
        # compile list pdf for lists with id in topic_ids
        for topic in self.topics:
            if topic.id in topic_ids:

                N1 = self.filter(topic.N1)
                N2 = self.filter(topic.N2)
                N3 = self.filter(topic.N3)

                l = List(topic.id, topic.title, N1=N1, N2=N2, N3=N3)

                latex2pdf(l.aslatex(), topic.id)


#
# PDF LIST CLASS
#

@attr.s(frozen=True)
class List(object):
    id: str = attr.ib()
    title: str = attr.ib()
    affiliation: str = attr.ib(default="Colégio e Curso Pensi, Química")
    author: str = attr.ib(default="Gabriel Braun")
    logo: str = attr.ib(default="pensi")
    N1 = attr.ib(default=ProblemSet([]))
    N2 = attr.ib(default=ProblemSet([]))
    N3 = attr.ib(default=ProblemSet([]))

    def aslatex(self):
        return latex_dim(f'''\\documentclass[braun, twocolumn]{{braun}}
\\braunsetup{{DIV=calc}}
\\title{{{self.title}}}
\\affiliation{{{self.affiliation}}}
\\author{{{self.author}}}
\\logo{{{self.logo}}}
\\begin{{document}}
\\maketitle[botrule=false]
{self.N1.latex_statements('Nível I')}
{self.N2.latex_statements('Nível II')}
{self.N3.latex_statements('Nível III')}
{latex_section('Gabarito')}
{self.N1.latex_answers('Nível I')}
{self.N2.latex_answers('Nível II')}
{self.N3.latex_answers('Nível III')}
\\end{{document}}''')


#
# MAIN
#


def main():
    data = Arsenal().read_dir("database")
    data.aspdf(['1A'])
    #tex = ProblemSet(data, ['1A01', '1A02', '1A03']).document()
    #latex2pdf(tex, '1A')


if __name__ == "__main__":
    main()
