"""Base de dados para problemas de química, Gabriel Braun, 2022

Esse módulo implementa funções para conversão entre diferentes formatos.
"""
from braunchem.latex.document import Document
import braunchem.utils.latex as latex
import braunchem.utils.config as config

import os
import shutil
import importlib.resources
import logging
from pathlib import Path
from dataclasses import dataclass

import pypandoc
import bs4
import pydantic

logger = logging.getLogger(__name__)


MARKDOWN_EXTENSIONS = [
    "fancy_lists",
    "task_lists",
    "pipe_tables",
    "implicit_figures",
    "fenced_divs",
]
"""Extensões de markdown utilizadas"""

PANDOC_MARKDOWN_FORMAT = (
    f"markdown_strict-raw_html+tex_math_dollars+{'+'.join(MARKDOWN_EXTENSIONS)}"
)
"""Formato markdown para o pandoc."""

PANDOC_FILTER_PATH = importlib.resources.files("braunchem.utils.filters")
"""Diretório contendo os filtros"""

PANDOC_FILTERS = [
    "containers.py",
    "pu2qty.py",
]
"""Filtros para o pandoc."""

PANDOC_FILTER_PATHS = [
    str(PANDOC_FILTER_PATH.joinpath(pandoc_filter)) for pandoc_filter in PANDOC_FILTERS
]
"""Lista de endereços para os filtros do pandoc."""


def md2html(md_str: str) -> str:
    """Converte markdown em HTML usando pandoc."""
    return pypandoc.convert_text(
        source=md_str,
        to="html",
        format=PANDOC_MARKDOWN_FORMAT,
        extra_args=["--quiet", "--mathjax"],
    )


def html2md(html_str: str) -> str:
    """Converte HTML em markdown usando pandoc."""
    return pypandoc.convert_text(
        source=html_str,
        to=PANDOC_MARKDOWN_FORMAT,
        format="html+tex_math_dollars+tex_math_single_backslash",
        extra_args=["--quiet"],
    )


def html2tex(html_str: str) -> str:
    """Converte HTML em LaTeX usando pandoc."""
    tex_str = pypandoc.convert_text(
        source=html_str,
        to="latex",
        format="html+tex_math_dollars+tex_math_single_backslash",
        extra_args=["--quiet"],
        filters=PANDOC_FILTER_PATHS,
    )
    tex_str = tex_str.replace("\\toprule()", "\\toprule")
    tex_str = tex_str.replace("\\midrule()", "\\midrule")
    tex_str = tex_str.replace("\\bottomrule()", "\\bottomrule")
    return tex_str


def md2tex(md_str: str) -> str:
    """Converte markdown em LaTeX usando pandoc."""
    tex_str = pypandoc.convert_text(
        source=md_str,
        to="latex",
        format=PANDOC_MARKDOWN_FORMAT,
        extra_args=["--quiet"],
        filters=PANDOC_FILTER_PATHS,
    )
    tex_str = tex_str.replace("\\toprule()", "\\toprule")
    tex_str = tex_str.replace("\\midrule()", "\\midrule")
    tex_str = tex_str.replace("\\bottomrule()", "\\bottomrule")
    return tex_str


def md2soup(md_str: str) -> bs4.BeautifulSoup:
    """Converte markdown em HTML que é parseado pelo BS."""
    html_str = md2html(md_str)
    return bs4.BeautifulSoup(html_str, "html.parser")


def soup_split(soup: bs4.BeautifulSoup, tag: str) -> list[bs4.BeautifulSoup]:
    """Divide um `BeaultifulSoup` por tag."""
    split_tag = soup.find(tag)
    if not split_tag:
        return [soup, None]

    splited = str(soup).split(str(split_tag), 1)
    return map(lambda s: bs4.BeautifulSoup(s, "html.parser"), splited)


class Text(pydantic.BaseModel):
    """Texto para diagramação.

    Atributos:
        md (str): Texto em markdown.
        tex (str): Texto em latex.
    """

    md: str
    tex: str

    @classmethod
    def parse_md(cls, md_str: str):
        """Cria um `Text` a partir de uma string em markdown."""
        if not md_str:
            return

        md_str = str(md_str).strip()

        tex_str = md2tex(md_str)
        return cls(md=md_str, tex=tex_str)

    @classmethod
    def parse_html(cls, html_str: str):
        """Cria um `Text` a partir de uma string em LaTeX."""
        if not html_str:
            return

        html_str = str(html_str).strip()

        md_str = html2md(html_str)
        tex_str = html2tex(html_str)
        return cls(md=md_str, tex=tex_str)


def get_database_paths(database_dir: Path) -> list[Path]:
    """Retorna os endereço dos arquivos `.md` dos problemas no diretório.

    Args:
        database_dir (Path): Diretório com os problemas.

    Retorna:
        list[Path]: Lista com o endereço dos arquivos `.md` de problemas.
    """
    logger.info(f"Procurando arquivos no diretório: {database_dir}.")

    md_files = []

    for root, _, files in os.walk(database_dir):
        for file in files:
            file_path = Path(root).joinpath(file)
            file_name = file_path.name
            name = file_path.stem
            dir_ = Path(root).relative_to(database_dir)

            # problemas
            if file_path.suffix == ".md":
                md_files.append(file_path)
                logging.debug(f"Arquivo {file_path} adicionado à lista.")
                continue

            img_dst_path = config.IMAGES_DIR.joinpath(dir_.parent, file_name)

            # figuras
            if file_path.suffix in [".svg", ".png"]:
                if img_dst_path.exists():
                    if file_path.stat().st_mtime < img_dst_path.stat().st_mtime:
                        continue

                img_dst_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(src=file_path, dst=img_dst_path)
                logging.info(f"Arquivo {file_path} copiado para: {img_dst_path}.")
                continue

            # figuras em LaTeX
            if file_path.suffix == ".tex":
                tex_img_dst_path = img_dst_path.with_suffix(".svg")
                if tex_img_dst_path.exists():
                    if file_path.stat().st_mtime < tex_img_dst_path.stat().st_mtime:
                        continue

                tex_img_dst_dir = tex_img_dst_path.parent
                tex_img_tmp_dir = config.TMP_IMAGES_DIR.joinpath(dir_).joinpath(name)
                tex_img_tmp_dir.mkdir(parents=True, exist_ok=True)

                tex_doc = Document(
                    id_=name,
                    contents=latex.cmd("input", file_path.resolve()),
                    standalone=True,
                )
                tex_doc.write_svg(tmp_dir=tex_img_tmp_dir, out_dir=tex_img_dst_dir)
                shutil.copy(
                    src=tex_img_dst_dir.joinpath(name).with_suffix(".svg"),
                    dst=file_path.with_suffix(".svg"),
                )

    return md_files
