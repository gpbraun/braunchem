#
# DOME - Gabriel Braun, 2021
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
    title: str = 'Química'
    author: str = 'Gabriel Braun'
    affiliation: str = 'Colégio e Curso Pensi, Coordenação de Química'
    template: str = 'braun, twocolumn'
    answers: bool = False
    solutions: bool = False
    problems: dict = Factory(dict)
    subtopics: list = Factory(list)

    def latex(self):
        # return tex file for compiling problem sheet as pdf
        preamble = latex.cmd(f'documentclass[{self.template}]', ['braun'])

        for prop in ['title', 'affiliation', 'author']:
            preamble += '\n' + latex.cmd(prop, [getattr(self, prop)])

        answers = latex.section('Gabarito', newpage=False)
        problems = '\n'
        for name, pset in self.problems.items():
            problems += pset.tex_statements(title=name)
            answers += pset.tex_answers(title=name)

        body = latex.cmd('maketitle') + latex.pu2qty(problems + answers)

        return preamble + latex.env('document', body)

    def compile_pdf(self):
        # generate problem sheet pdf
        convert.tex2pdf(self.latex(), self.id_, path='archive')


def file2topic(path, problemset):
    kwargs = {}
    # get YAML data and contents
    id_ = path.stem
    kwargs['id_'] = id_

    tfile = load(path)
    soup = convert.md2soup(tfile.content)

    for p in ['title', 'author', 'affiliation']:
        if p in tfile:
            kwargs[p] = tfile[p]

    if 'problems' in tfile:
        print(tfile['problems'])
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
                subtopic_id, subtopic_title, subtopic_items, subtopic_abilities
            )
        )

    return Topic(**kwargs)
