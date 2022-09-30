"""Base de dados para problemas de química, Gabriel Braun, 2022

Esse módulo implementa funções para conversão entre diferentes formatos.
"""
import braunchem.utils.latex as latex
import braunchem.utils.config as config

import os
import subprocess
import shutil
import importlib.resources
import logging
from pathlib import Path
from dataclasses import dataclass

import pypandoc
import bs4
from pydantic import BaseModel


MARKDOWN_EXTENSIONS = [
    "task_lists",
    "table_captions",
    "pipe_tables",
    "implicit_figures",
    "fenced_divs",
]
"""Extensões de markdown utilizadas"""

PANDOC_MARKDOWN_FORMAT = (
    f"markdown_strict-raw_html+tex_math_dollars+{'+'.join(MARKDOWN_EXTENSIONS)}"
)
"""Formato markdown para o pandoc."""

PANDOC_FILTER_PATH = importlib.resources.files("braunchem.filters")
"""Diretório contendo os filtros"""


def md2html(md_str: str) -> str:
    """Converte markdown em HTML usando pandoc."""
    html_str = pypandoc.convert_text(
        source=md_str,
        to="html",
        format=PANDOC_MARKDOWN_FORMAT,
        extra_args=["--quiet", "--mathjax"],
        # filters=[str(PANDOC_FILTER_PATH.joinpath("test.py"))],
    )
    return html_str


def html2md(html_str: str) -> str:
    """Converte HTML em markdown usando pandoc."""
    md_str = pypandoc.convert_text(
        source=html_str,
        to=PANDOC_MARKDOWN_FORMAT,
        format="html+tex_math_dollars+tex_math_single_backslash",
        extra_args=["--quiet"],
        # filters=[str(PANDOC_FILTER_PATH.joinpath("test.py"))],
    )
    return md_str


def html2tex(html_str: str) -> str:
    """Converte HTML em LaTeX usando pandoc."""
    tex_str = pypandoc.convert_text(
        source=html_str,
        to="latex",
        format="html+tex_math_dollars+tex_math_single_backslash",
        extra_args=["--quiet"],
        # filters=[str(PANDOC_FILTER_PATH.joinpath("test.py"))],
    )
    tex_str = latex.pu2qty(tex_str)
    return tex_str


def md2tex(md_str: str) -> str:
    """Converte markdown em LaTeX usando pandoc."""
    tex_str = pypandoc.convert_text(
        source=md_str,
        to="latex",
        format=PANDOC_MARKDOWN_FORMAT,
        extra_args=["--quiet"],
    )
    tex_str = latex.pu2qty(tex_str)
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


class Text(BaseModel):
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
        md_str = str(md_str).strip()

        tex_str = md2tex(md_str)
        return cls(md=md_str, tex=tex_str)

    @classmethod
    def parse_html(cls, html_str: str):
        """Cria um `Text` a partir de uma string em LaTeX."""
        html_str = str(html_str).strip()

        md_str = html2md(html_str)
        tex_str = html2tex(html_str)
        return cls(md=md_str, tex=tex_str)


def copy_r(src, dest):
    try:
        shutil.copy(src, dest)
    except shutil.SameFileError:
        pass


def copy_all(loc, dest):
    for f in os.listdir(loc):
        copy_r(os.path.join(loc, f), dest)


def run_latexmk(tex_path: Path, tmp_dir: Path):
    """Executa o comando `latexmk`."""
    logging.info(f"Compilando o arquivo {tex_path}.")
    subprocess.run(
        [
            "latexmk",
            "-shell-escape",
            "-interaction=nonstopmode",
            "-file-line-error",
            "-pdf",
            "-cd",
            tex_path,
        ],
        stdout=subprocess.DEVNULL,
    )
    logging.info(f"Arquivo {tex_path} compilado!")


def run_pdf2svg(tex_path: Path, svg_path: Path | None = None):
    """Executa o comando `pdf2svg`."""
    subprocess.run(
        [
            "pdf2svg",
            f"{tex_path}",
            f"{svg_path}",
        ],
        stdout=subprocess.DEVNULL,
    )
    logging.info(f"Arquivo {tex_path} convertido em {svg_path}.")


@dataclass
class Document:
    id_: str
    title: str | None = None
    author: str | None = None
    affiliation: str | None = None
    template: str | None = None
    contents: str | None = None
    standalone: bool = False

    def preamble(self):
        if self.standalone:
            return ""

        return "\n".join(
            [
                latex.cmd("title", self.title) if self.title else "",
                latex.cmd("author", self.author) if self.author else "",
                latex.cmd("affiliation", self.affiliation) if self.affiliation else "",
            ]
        )

    def documentclass(self):
        if self.standalone:
            return latex.cmd("documentclass", "braunfigure")

        return f"\\documentclass[{self.template}]{{braun}}\n"

    def body(self):
        if self.standalone:
            return latex.env("document", self.contents)

        return latex.env("document", f"\\maketitle\n\n{self.contents}")

    def document(self):
        return "\n".join(
            [
                self.documentclass(),
                self.preamble(),
                self.body(),
            ]
        )

    def pdf(self, tmp_dir: Path, out_dir: Path | None = None) -> Path:
        """Gera o `pdf` e copia para um diretório de saída.

        Args:
            tmp_dir (Path): Diretório para arquivos temporários.
            out_dir (Path): Diretório de saída.
        """
        tmp_dir.mkdir(parents=True, exist_ok=True)
        copy_all("src/braunchem/latex/templates", tmp_dir)

        tex_path = tmp_dir.joinpath(self.id_).with_suffix(".tex")
        tex_path.write_text(self.document())
        run_latexmk(tex_path, tmp_dir)
        pdf_path = tex_path.with_suffix(".pdf")

        if out_dir:
            out_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy(src=tex_path.with_suffix(".pdf"), dst=out_dir)

        return pdf_path

    def svg(self, tmp_dir: Path, out_dir: Path | None = None) -> Path:
        """Gera o `svg` e copia para um diretório de saída.

        Args:
            tmp_dir (Path): Diretório para arquivos temporários.
            out_dir (Path): Diretório de saída.
        """
        pdf_path = self.pdf(tmp_dir)

        if not out_dir:
            out_dir = tmp_dir

        svg_path = out_dir.joinpath(self.id_).with_suffix(".svg")
        run_pdf2svg(pdf_path, svg_path)

        return svg_path


def get_database_paths(database_dir: Path) -> list[Path]:
    """Retorna os endereço dos arquivos `.md` dos problemas no diretório.

    Args:
        database_dir (Path): Diretório com os problemas.

    Retorna:
        list[Path]: Lista com o endereço dos arquivos `.md` de problemas.
    """
    logging.info(f"Procurando arquivos no diretório: {database_dir}.")

    md_files = []

    for root, _, files in os.walk(database_dir):
        for file in files:
            file_path = Path(root).joinpath(file)
            name = file_path.name
            dir_ = Path(root).relative_to(database_dir)

            # problemas
            if file_path.suffix == ".md":
                md_files.append(file_path)
                logging.debug(f"Arquivo {file_path} adicionado à lista.")

                continue

            img_dst_path = config.IMAGES_DIR.joinpath(dir_.parent, name)

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
                tex_img_tmp_dir = config.TMP_IMAGES_DIR.joinpath(dir_)
                tex_img_tmp_dir.mkdir(parents=True, exist_ok=True)

                tex_doc = Document(
                    id_=name,
                    contents=latex.cmd("input", file_path.resolve()),
                    standalone=True,
                )
                tex_doc.svg(tmp_dir=tex_img_tmp_dir, out_dir=tex_img_dst_dir)

    return md_files
