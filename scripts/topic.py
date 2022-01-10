#
# TOPIC CLASS
#

from attr import frozen, Factory

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
    title: str = ""
    problems: dict = Factory(dict)
    subtopics: list = Factory(list)


def file2topic(path):
    kwargs = {}
    # get YAML data and contents
    id_ = path.stem
    kwargs['id_'] = id_

    tfile = load(path)
    soup = convert.md2soup(tfile.content)

    for p in ['title', 'problems']:
        if p in tfile:
            kwargs[p] = tfile[p]

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
                subtopic_id, subtopic_title, subtopic_items, subtopic_abilities
            )
        )

    return Topic(**kwargs)


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
        preamble = latex.cmd(f'documentclass[{template}]', ['braun'])

        for prop in ['title', 'affiliation', 'author', 'logo']:
            preamble += '\n' + latex.cmd(prop, [getattr(self, prop)])

        preamble += '\n' + latex.cmd('dbpath', ['../database'])

        answers = latex.section('Gabarito', newpage=False)
        problems = '\n'
        for pset in self.problem_sets:
            problems += pset.tex_statements()
            answers += pset.tex_answers()

        body = latex.cmd('maketitle') + latex.pu2qty(problems + answers)

        return preamble + latex.env('document', body)
