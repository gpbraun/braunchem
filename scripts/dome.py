#
# DOME - Gabriel Braun, 2021
#

# IMPORTS

import attr
import json
import os
import frontmatter
from pathlib import Path
import pypandoc
from bs4 import BeautifulSoup

#
# TEXT CLASS
#


def md2soup(content):
    # convert md to html using pandoc and parse as soup
    pandoc_html = pypandoc.convert_text(
        content, 'html',
        format='markdown-tex_math_dollars-raw_tex',
        # extra_args=['--katex']
    )
    return BeautifulSoup(pandoc_html, 'html.parser')


def html2md(content):
    # convert html string to markdown using pandoc
    return pypandoc.convert_text(
        content, 'md',
        format='html+tex_math_dollars-raw_tex',
    ).rstrip()


def html2tex(content):
    # convert html string to latex using pandoc
    return pypandoc.convert_text(
        content, 'latex',
        format='html+tex_math_dollars-raw_tex',
    ).replace('\\tightlist\n','').rstrip()
    # TODO: convert \pu to \unit and \qty fom siunitx!


@attr.s(frozen=True)
class Text(object):
    html: str = attr.ib(converter=str)
    md: str = attr.ib(init=False)
    tex: str = attr.ib(init=False)

    def __attrs_post_init__(self):
        object.__setattr__(self, "md", html2md(self.html))
        object.__setattr__(self, "tex", html2tex(self.html))

#
# PROBLEM CLASS
#


@attr.s(frozen=True)
class Problem(object):
    id: str = attr.ib()
    problem_path: str = attr.ib()
    statement = attr.ib(init=False)
    solution: str = attr.ib(default="")
    obj: int = attr.ib(default=-1)
    answer: str = attr.ib(init=False)
    options = attr.ib(factory=list)
    data = attr.ib(factory=list)

    def __attrs_post_init__(self):
        file = os.path.join(self.problem_path, f'{self.id}.md')

        # get YAML data and contents
        problem_file = frontmatter.load(file)
        soup = md2soup(problem_file.content)

        for prop in ['data', 'answer']:
            if prop in problem_file:
                object.__setattr__(self, prop, problem_file[prop])

        # change images direcory to images folder
        for img in soup.find_all('img'):
            img['src'] = os.path.join(
                "./images/", os.path.basename(img['src']))

        # get problem options and ansewer, if objective
        task_list = soup.find('ul', class_='task-list')
        if task_list:
            options = []
            for index, item in enumerate(task_list.find_all('li')):
                check_box = item.find('input').extract()
                if check_box.has_attr('checked'):
                    object.__setattr__(self, "obj", Text(index))
                    object.__setattr__(self, "answer", Text(item))
                options.append(Text(item))
            task_list.decompose()
            object.__setattr__(self, "options", options)

        # get problem solution
        solution = soup.find('blockquote')
        if solution:
            object.__setattr__(self, "solution", Text(solution.extract().text))

        # get problem statement
        object.__setattr__(self, "statement", Text(soup))

    def asdict(self):
        filters = attr.filters.exclude(attr.fields(Text).html)
        return attr.asdict(self, filter=filters)

    def aslatex(self):
        return f'''
\\begin{{problem}}
    {self.statement.tex}
\\end{{problem}}'''

#
# ARSENAL CLASS
#


def get_file_paths(directory):
    return [(Path(filename).stem, root) for root, _, files in os.walk(directory) for filename in files if filename.endswith('.md')]


@attr.s(frozen=True)
class Arsenal(object):
    db_path: str = attr.ib()
    problem_ids = attr.ib(factory=list)

    def __attrs_post_init__(self):
        problems = []
        for id, path in get_file_paths(self.db_path):
            problems.append(Problem(id, path))
        object.__setattr__(self, "problems", problems)

        json_file = os.path.join(self.db_path, 'problems.json')
        with open(json_file, 'w') as f:
            json.dump(self.asdict(), f, indent=4, ensure_ascii=False)

    def asdict(self):
        filters = attr.filters.exclude(
            attr.fields(Arsenal).db_path,
            attr.fields(Text).html
        )
        return attr.asdict(self, filter=filters)

#
# Latex CLASS
#


@attr.s(frozen=True)
class Latex(object):
    Arsenal: str = attr.ib()
    problem_ids = attr.ib()
    problems = attr.ib(init=False)
    title: str = attr.ib(default="Título")
    affiliation: str = attr.ib(default="Colégio e Curso Pensi, Turma IME-ITA")
    author: str = attr.ib(default="Gabriel Braun")
    logo: str = attr.ib(default="pensi")

    def __attrs_post_init__(self):
        problems = []
        for problem in self.Arsenal.problems:
            if problem.id in self.problem_ids:
                problems.append(problem)
        object.__setattr__(self, "problems", problems)

    def document(self):
        content = '\n'.join([ problem.aslatex() for problem in self.problems ])

        return f'''\\documentclass[braun, twocolumn]{{braun}}
\\braunsetup{{DIV=calc}}
\\title{{{self.title}}}
\\affiliation{{{self.affiliation}}}
\\author{{{self.author}}}
\\logo{{{self.logo}}}
\\begin{{document}}
\\maketitle[botrule=false]
{content}
\\end{{document}}'''

#
# MAIN
#


def main():
    data = Arsenal("database")
    tex = Latex(data, ['1A01', '1A02']).document()
    with open('database/testes/1A.tex', 'w') as f:
            f.write(tex)


if __name__ == "__main__":
    main()
