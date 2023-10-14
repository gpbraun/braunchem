"""Base de dados para problemas de química, Gabriel Braun, 2022

Esse módulo implementa funções para conversão entre diferentes formatos.
"""
import json
import logging
from importlib import resources
from pathlib import Path

import pypandoc

logger = logging.getLogger(__name__)


TEXINPUTS = resources.files("braunchem").joinpath("../../latex")

PANDOC_FILTER_PATH = resources.files("braunchem.utils").joinpath("filters")
PANDOC_WRITER_PATH = resources.files("braunchem.utils").joinpath("writers")

PANDOC_PROBLEM_WRITER_PATH = str(PANDOC_WRITER_PATH.joinpath("problem.lua"))
PANDOC_SECTION_WRITER_PATH = str(PANDOC_WRITER_PATH.joinpath("section.lua"))

PANDOC_PROBLEM_FILTERS = [
    "row_width.lua",
]
PANDOC_SECTION_FILTERS = [
    "pandoc-crossref",
    "row_width.lua",
    "tikz_img.lua",
]

PANDOC_PROBLEM_FILTER_PATHS = [
    str(PANDOC_FILTER_PATH.joinpath(pandoc_filter))
    for pandoc_filter in PANDOC_PROBLEM_FILTERS
]
PANDOC_SECTION_FILTER_PATHS = [
    str(PANDOC_FILTER_PATH.joinpath(pandoc_filter))
    for pandoc_filter in PANDOC_SECTION_FILTERS
]

CROSSREF_YAML_PATH = str(PANDOC_FILTER_PATH.joinpath("pandoc-crossref.yaml"))


def pandoc_args(meta: dict) -> str:
    """Converte um `.dics` nos argumentos para o Pandoc."""
    args = ["--quiet"]
    meta.update(
        {
            "texinputs": TEXINPUTS,
            "filterpath": PANDOC_FILTER_PATH,
            "writerpath": PANDOC_WRITER_PATH,
            "crossrefYaml": CROSSREF_YAML_PATH,
        }
    )
    for key, val in meta.items():
        args.append(f"--metadata={key}:{val}")

    return args


def md2problem(md_str: str) -> dict:
    """Converte um arquivo `.md` em um `Problem`."""
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


def md2section(path: Path) -> dict:
    """Converte um arquivo `.md` em um `Section`."""
    section = pypandoc.convert_file(
        source_file=path,
        format="markdown",
        to=PANDOC_SECTION_WRITER_PATH,
        filters=PANDOC_SECTION_FILTER_PATHS,
        extra_args=pandoc_args(
            {
                "id": path.stem,
                "path": path.parent,
                "imgpath": Path("img"),
            }
        ),
    )

    return json.loads(section)
