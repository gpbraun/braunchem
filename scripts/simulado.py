#
# TOPIC CLASS
#

from attr import frozen

import latex

from problem import ProblemSet, link2problem


@frozen
class Simulado:
    id: str
    title: str
    modelo: str
    problems: ProblemSet

    def astex(self):
        # return tex file for compiling list as pdf
        preamble = latex.cmd(f'documentclass[{self.modelo}]', ['braun'])

        for prop in ['title']:
            preamble += '\n' + latex.cmd(prop, [getattr(self, prop)])

        preamble += '\n' + latex.cmd('dbpath', ['../database'])

        answers = latex.section('Gabarito', newpage=False) + \
            self.problems.tex_answers()
        problems = '\n' + self.problems.tex_statements()

        body = latex.cmd('maketitle') + latex.pu2qty(problems + answers)

        return preamble + latex.env('document', body)


def create_simulado(cur, p_links):
    kwargs = {}
    kwargs['title'] = 'Ciclo 6 Discursivo Química'
    kwargs['modelo'] = 'IME'
    kwargs['problems'] = ProblemSet(
        'título', [link2problem(cur, link) for link in p_links]
    )
    return Simulado('id', **kwargs)
