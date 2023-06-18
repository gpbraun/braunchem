"""Base de dados para problemas de química, Gabriel Braun, 2022

Esse módulo implementa uma classe para os problemas.
"""
import logging
from datetime import datetime
from pathlib import Path

import jinja2
import pydantic

import braunchem.utils.converter as converter

logger = logging.getLogger(__name__)


JINJA_LATEX_ENV = jinja2.Environment(
    block_start_string="((*",
    block_end_string="*))",
    variable_start_string="(((",
    variable_end_string=")))",
    comment_start_string="((=",
    comment_end_string="=))",
    trim_blocks=True,
    lstrip_blocks=True,
    loader=jinja2.PackageLoader("braunchem"),
)

JINJA_PROBLEM_TEMPLATE = JINJA_LATEX_ENV.get_template("problem.tex.j2")


class Text(pydantic.BaseModel):
    """Texto para diagramação.

    Atributos:
        html (str): Texto em HTML.
        md (str): Texto em markdown.
        tex (str): Texto em latex.
    """

    html: str
    latex: str


class Problem(pydantic.BaseModel):
    """Problema.

    Atributos:
        id_ (str): Identificador único.
        path (Path): Diretório do problema.
        date (datetime): Data da última modificação do problema.
        statement (Text): Enunciado.
        solution (Text): Gabarito comentado.
        answer (list[Text]): Respostas.
        data (Table): Dados termodinâmicos.
        choices (list[Text]): Alternativas (problemas objetivos).
        correct_choice (int): Índice da alternativa correta.
    """

    id_: str
    date: datetime
    statement: Text
    solution: Text = None
    choices: list[Text] = None
    correct_choice: int = None

    @property
    def is_objective(self):
        """Verifica se o problema é objetivo."""
        return True if self.choices else False

    def render_latex(self):
        tex_str = JINJA_PROBLEM_TEMPLATE.render(self.dict())
        return tex_str

    @classmethod
    def parse_mdfile(cls, problem_path: Path):
        """Cria um `Problem` a partir de um arquivo `.md`."""
        md_text = problem_path.read_text()
        problem_json = converter.md2problem(md_text)
        return cls.parse_obj(problem_json)
