"""Base de dados para problemas de química, Gabriel Braun, 2022

Esse módulo implementa funções para conversão entre diferentes formatos.
"""
import importlib.resources
import json
import logging

import pypandoc

logger = logging.getLogger(__name__)


PANDOC_FILTER_PATH = importlib.resources.files("braunchem.utils.filters")
PANDOC_WRITER_PATH = importlib.resources.files("braunchem.utils.writers")

PANDOC_PROBLEM_FILTERS = ["pandoc-crossref"]
"""Filtros usados nos problemas."""

PANDOC_PROBLEM_FILTER_PATHS = [
    str(PANDOC_FILTER_PATH.joinpath(pandoc_filter))
    for pandoc_filter in PANDOC_PROBLEM_FILTERS
]
"""Lista de endereços para os filtros do pandoc."""

PANDOC_PROBLEM_WRITER_PATH = str(PANDOC_WRITER_PATH.joinpath("problem.lua"))
PANDOC_SECTION_WRITER_PATH = str(PANDOC_WRITER_PATH.joinpath("section.lua"))

CROSSREF_YAML_PATH = str(PANDOC_FILTER_PATH.joinpath("pandoc-crossref.yaml"))


def md2problem(md_str: str) -> dict:
    """Converte HTML em LaTeX usando pandoc."""
    problem = pypandoc.convert_text(
        source=md_str,
        to=PANDOC_PROBLEM_WRITER_PATH,
        format="markdown",
        extra_args=[
            "--quiet",
            "--metadata=id:1A01",
            "--metadata=seed:123456",
        ],
        filters=PANDOC_PROBLEM_FILTER_PATHS,
    )
    return json.loads(problem)


def md2section(md_str: str) -> dict:
    """Converte HTML em LaTeX usando pandoc."""
    section = pypandoc.convert_text(
        source=md_str,
        to=PANDOC_SECTION_WRITER_PATH,
        format="markdown",
        extra_args=[
            "--quiet",
            "--metadata=id:1A",
            f"--metadata=crossrefYaml:{CROSSREF_YAML_PATH}",
        ],
        filters=PANDOC_PROBLEM_FILTER_PATHS,
    )
    return json.loads(section)
