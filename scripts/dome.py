#
# DOME - Gabriel Braun, 2021
#

# TODO:
# Gabarito do nível 1 em n=5 columas.
# Gerar o "elements"
# adicionar guard clauses

# IMPORTS

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
# TEXT CLASS
#

MD = Markdown(extensions=['pymdownx.tasklist'])


def md2soup(content):
    html = MD.convert(content)
    return BeautifulSoup(html, 'html.parser')


# def html2md(content):
#     return markdownify(str(content)).rstrip()

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
    # TODO: convert \pu to \unit and \qty fom siunitx!

def pu2si(content):
    pu_command = re.compile(r'\\pu\{\s*([\deE,.]*)\s*(.*)\s*\}')

    return 


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


def dataset2latex(dataset):
    # return data array to latex list
    datalist = '\n'.join([f'\\item {data.aslatex()}\n' for data in dataset])
    return f'\\begin{{itemize}}\n{datalist}\\end{{itemize}}'


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
        # TODO: automatic choices
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

    def latex_data(self):
        # return data as latex list with header
        if not self.data:
            return ''
        return f'\\subsubsection*{{Dados}}\n{dataset2latex(self.data)}'

    def latex_choices(self):
        # return choices as latex list
        if not self.is_obj:
            return ''
        choices = '\n'.join([f'\\item {choice}' for choice in self.choices])
        return f'\\begin{{choices}}\n{choices}\n\\end{{choices}}'

    def latex_answer(self):
        # return choices as latex list
        if self.is_obj:
            return f'\MiniBox{{{chr(65 + self.obj)}}}'
        else:
            return self.answer

    def aslatex(self):
        # return problem in latex format
        return f'''\\begin{{problem}}
{md2latex(self.statement)}
{self.latex_choices()}
{self.latex_data()}
\\end{{problem}}'''


@attr.s(frozen=True)
class ProblemSet(object):
    problems = attr.ib()

    def latex_statements(self, header_title=''):
        if not self.problems:
            return ''

        # empty header title removes \section (for lists without levels)
        head = f'\section*{{{header_title}}}\n' if header_title else ''

        statements = '\n'.join(
            [problem.aslatex() for problem in self.problems]
        )
        return f'{head}\n{statements}'

    def latex_answers(self, header_title=''):
        if not self.problems:
            return ''

        # empty header title removes \section (for lists without levels)
        head = f'\subsection*{{{header_title}}}\n' if header_title else ''

        cols = 5 if all([problem.is_obj for problem in self.problems]) else 2

        answers = '\n'.join(
            [f'\\item {problem.latex_answer()}' for problem in self.problems]
        )
        return f'{head}\\begin{{itemize}}({cols})\n{answers}\n\\end{{itemize}}'

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


def get_file_paths(directory):
    # get the path of all problems and topics
    topic_files = []
    problem_files = []

    topic_regex = re.compile('\d[A-Z].md')
    problem_regex = re.compile('\d[A-Z]\d{2}.md')

    for root, _, files in os.walk(directory):
        for filename in files:
            if topic_regex.match(filename):
                topic_files.append((Path(filename).stem, root))
            elif problem_regex.match(filename):
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

    def aspdf(self, topic_ids):
        for topic in self.topics:
            if topic.id in topic_ids:
                N1_problems = []
                N2_problems = []
                N3_problems = []
                for problem in self.problems:
                    if problem.id in topic.N1:
                        N1_problems.append(problem)
                    elif topic.N2 and problem.id in topic.N2:
                        N2_problems.append(problem)
                    elif topic.N3 and problem.id in topic.N3:
                        N3_problems.append(problem)

                N1 = ProblemSet(N1_problems)
                N2 = ProblemSet(N2_problems)
                N3 = ProblemSet(N3_problems)

                l = List(topic.id, topic.title, N1=N1, N2=N2, N3=N3)

                print(l.aslatex())
                latex2pdf(l.aslatex(), topic.id)


#
#
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
        return f'''\\documentclass[braun, twocolumn]{{braun}}
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
\\section*{{Gabarito}}
{self.N1.latex_answers('Nível I')}
{self.N2.latex_answers('Nível II')}
{self.N3.latex_answers('Nível III')}
\\end{{document}}'''


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
