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

import pypandoc
import bs4
import pydantic

logger = logging.getLogger(__name__)


MARKDOWN_EXTENSIONS = [
    "smart",
    "fancy_lists",
    "task_lists",
    "pipe_tables",
    "table_captions",
    "implicit_figures",
    "fenced_divs",
    # "yaml_metadata_block",
]
"""Extensões de markdown utilizadas"""

PANDOC_MARKDOWN_FORMAT = (
    f"markdown_strict-raw_html+tex_math_dollars+{'+'.join(MARKDOWN_EXTENSIONS)}"
)
"""Formato markdown para o pandoc."""

PANDOC_WRITER_PATH = importlib.resources.files("braunchem.utils.writers")
"""Diretório contendo os filtros"""

PANDOC_FILTER_PATH = importlib.resources.files("braunchem.utils.filters")
"""Diretório contendo os filtros"""

PANDOC_FILTERS = [
    "legacy_containers.lua",
    "figures.py",
    "pu2qty.py",
]
"""Filtros para o pandoc."""

PANDOC_FILTER_PATHS = [
    str(PANDOC_FILTER_PATH.joinpath(pandoc_filter)) for pandoc_filter in PANDOC_FILTERS
]
"""Lista de endereços para os filtros do pandoc."""

PANDOC_COLUMN_NUM = 150
"""Número de colunas consideradas pelo pandoc"""


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


def html2tex(html_str: str, path: Path = None) -> str:
    """Converte HTML em LaTeX usando pandoc."""
    tex_str = pypandoc.convert_text(
        source=html_str,
        to="latex",
        format="html+tex_math_dollars+tex_math_single_backslash",
        extra_args=[
            "--quiet",
            f"--columns={PANDOC_COLUMN_NUM}",
            f"--metadata=path:{path}" if path else "",
        ],
        filters=PANDOC_FILTER_PATHS,
    )
    # tex_str = tex_str.replace("\\noalign{}", "")
    return tex_str


def md2tex(md_str: str, path: Path = None) -> str:
    """Converte markdown em LaTeX usando pandoc."""
    tex_str = pypandoc.convert_text(
        source=md_str,
        to="latex",
        format=PANDOC_MARKDOWN_FORMAT,
        extra_args=[
            "--quiet",
            f"--columns={PANDOC_COLUMN_NUM}",
            f"--metadata=path:{path}" if path else "",
        ],
        filters=PANDOC_FILTER_PATHS,
    )
    # tex_str = tex_str.replace("\\noalign{}", "")
    return tex_str


def md2soup(md_str: str) -> bs4.BeautifulSoup:
    """Converte markdown em HTML que é parseado pelo BS."""
    html_str = md2html(md_str)
    return bs4.BeautifulSoup(html_str, "html.parser")


def soup_split(soup: bs4.BeautifulSoup, tag: str):
    """Divide um `BeaultifulSoup` por tag."""
    split_tag = soup.find(tag)
    if not split_tag:
        return [soup, None]

    splited = str(soup).split(str(split_tag), 1)
    return map(lambda s: bs4.BeautifulSoup(s, "html.parser"), splited)


class Text(pydantic.BaseModel):
    """Texto para diagramação.

    Atributos:
        html (str): Texto em HTML.
        md (str): Texto em markdown.
        tex (str): Texto em latex.
    """

    html: str
    md: str
    tex: str

    @classmethod
    def parse_md(cls, md_str: str, path: Path = None):
        """Cria um `Text` a partir de uma string em markdown."""
        if not md_str:
            return

        md_str = str(md_str).strip()

        html_str = md2html(md_str)
        tex_str = md2tex(md_str, path)

        return cls(html=html_str, md=md_str, tex=tex_str)

    @classmethod
    def parse_html(cls, html_str: str | bs4.BeautifulSoup, path: Path = None):
        """Cria um `Text` a partir de uma string em LaTeX."""
        if not html_str:
            return

        html_str = str(html_str).strip()

        md_str = html2md(html_str)
        tex_str = html2tex(html_str, path)

        return cls(html=html_str, md=md_str, tex=tex_str)


def get_database_paths(database_dir: Path, generate_figures=True) -> list[Path]:
    """Retorna os endereço dos arquivos `.md` dos problemas no diretório.

    Args:
        database_dir (Path): Diretório com os problemas.

    Retorna:
        list[Path]: Lista com o endereço dos arquivos `.md` de problemas.
    """
    logger.info(f"Procurando arquivos no diretório: '{database_dir}'.")

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
                logging.debug(f"Arquivo '{file_path}' adicionado à lista.")
                continue

            # figuras
            if generate_figures:
                img_dst_path = config.IMAGES_DIR.joinpath(file_name)

                if file_path.suffix in [".svg", ".png"]:
                    # se o svg veio de um .tex, continuar
                    if file_path.with_suffix(".tex").exists():
                        continue

                    if img_dst_path.exists():
                        if file_path.stat().st_mtime < img_dst_path.stat().st_mtime:
                            continue

                    img_dst_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy(src=file_path, dst=img_dst_path)
                    logging.info(
                        f"Arquivo '{file_path}' copiado para: '{img_dst_path}'."
                    )
                    continue

                # figuras em LaTeX
                if file_path.suffix == ".tex":
                    tex_svg_img_dst_path = img_dst_path.with_suffix(".svg")
                    if tex_svg_img_dst_path.exists():
                        if (
                            file_path.stat().st_mtime
                            < tex_svg_img_dst_path.stat().st_mtime
                        ):
                            logging.debug(f"Figura '{file_path}' mantida.")
                            continue

                    tex_img_dst_dir = tex_svg_img_dst_path.parent
                    tex_img_tmp_dir = config.TMP_IMAGES_DIR.joinpath(dir_).joinpath(
                        name
                    )
                    tex_img_tmp_dir.mkdir(parents=True, exist_ok=True)

                    tex_doc = Document(
                        id_=name,
                        contents=latex.cmd("input", str(file_path.resolve())),
                        standalone=True,
                    )
                    tex_doc.write_svg(tmp_dir=tex_img_tmp_dir, out_dir=tex_img_dst_dir)
                    shutil.copy(
                        src=tex_svg_img_dst_path,
                        dst=file_path.with_suffix(".svg"),
                    )

    return md_files


def soup_split_header(soup: bs4.BeautifulSoup, tag="h1", path: Path = None):
    """Divide um `BeaultifulSoup` por tag."""
    headers = soup.find_all(tag)
    if not headers:
        raise StopIteration

    for header in headers:
        next_node = header
        content = ""
        while True:
            next_node = next_node.nextSibling
            if next_node is None:
                break
            if isinstance(next_node, bs4.NavigableString):
                content = "\n".join([content, str(next_node)])
            if isinstance(next_node, bs4.Tag):
                if next_node.name == tag:
                    break
                content = "\n".join([content, str(next_node)])

        yield header.text, Text.parse_html(content, path)
