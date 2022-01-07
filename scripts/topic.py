#
# TOPIC CLASS
#

from attr import frozen, Factory, field

from frontmatter import load

import convert
import latex


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
    problems: dict = Factory(dict)
    subtopics: list = Factory(list)

    def __attrs_post_init__(self):
        # get YAML data and contents
        object.__setattr__(self, 'id', self.path.stem)
        tfile = load(self.path)
        soup = convert.md2soup(tfile.content)

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
                convert.html2md(i) for i in all_items[index].find_all('li')
            ]
            subtopic_abilities = [
                convert.html2md(a) for a in all_abilities[index].find_all('li')
            ]

            self.subtopics.append(
                Subtopic(subtopic_id, subtopic_title,
                         subtopic_items, subtopic_abilities)
            )

        return self

# def file2topic(path):
#     props = {}
#     # get YAML data and contents
#     props['id'] = path.stem

#     tfile = load(path)
#     soup = convert.md2soup(tfile.content)

#     for p in ['title', 'problems']:
#         if p in tfile:
#             props[p] = tfile[p]

#     # get subtopics items and abilities from HTML tags
#     all_subtopics = soup.find_all('h1')
#     all_items = soup.find_all('ol')
#     all_abilities = soup.find_all('ul')

#     for index, subtopic in enumerate(all_subtopics):
#         subtopic_id = f'{self.id}.{index+1}'
#         subtopic_title = subtopic.text
#         subtopic_items = [
#             convert.html2md(i) for i in all_items[index].find_all('li')
#         ]
#         subtopic_abilities = [
#             convert.html2md(a) for a in all_abilities[index].find_all('li')
#         ]

#         self.subtopics.append(
#             Subtopic(subtopic_id, subtopic_title,
#                         subtopic_items, subtopic_abilities)
#         )

#     return Topic(**props)


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
