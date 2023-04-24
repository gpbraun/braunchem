"""Base de dados para problemas de química, Gabriel Braun, 2022

Esse módulo implementa funções para conversão entre diferentes formatos.
"""
import importlib.resources
import logging
import json

import pypandoc

logger = logging.getLogger(__name__)


MARKDOWN_EXTENSIONS = [
    "smart",
    "fancy_lists",
    "task_lists",
    "pipe_tables",
    "implicit_figures",
    "fenced_divs",
    "yaml_metadata_block",
]
"""Extensões de markdown utilizadas"""

PANDOC_MARKDOWN_FORMAT = (
    f"markdown_strict-raw_html+tex_math_dollars+{'+'.join(MARKDOWN_EXTENSIONS)}"
)
"""Formato markdown para o pandoc."""

PANDOC_FILTER_PATH = importlib.resources.files("braunchem.utils.filters")
PANDOC_WRITER_PATH = importlib.resources.files("braunchem.utils.writers")

PANDOC_PROBLEM_FILTERS = [
    "containers.lua",
    "pu2qty.py",
    "problem_lists.lua",
]
"""Filtros usados nos problemas."""

PANDOC_PROBLEM_FILTER_PATHS = [
    str(PANDOC_FILTER_PATH.joinpath(pandoc_filter))
    for pandoc_filter in PANDOC_PROBLEM_FILTERS
]
"""Lista de endereços para os filtros do pandoc."""

PANDOC_PROBLEM_WRITER_PATH = str(PANDOC_WRITER_PATH.joinpath("problem.lua"))
"""Endereço do `writer` para problemas."""

PANDOC_COLUMN_NUM = 150
"""Número de colunas consideradas pelo pandoc"""


def md2problem(md_str: str) -> str:
    """Converte HTML em LaTeX usando pandoc."""
    problem = pypandoc.convert_text(
        source=md_str,
        to=PANDOC_PROBLEM_WRITER_PATH,
        format=PANDOC_MARKDOWN_FORMAT,
        extra_args=[
            "--quiet",
            "--katex",
            f"--columns={PANDOC_COLUMN_NUM}",
            "--metadata=id:1234",
        ],
        filters=PANDOC_PROBLEM_FILTER_PATHS,
    )
    return json.loads(problem)
