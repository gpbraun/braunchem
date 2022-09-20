"""Base de dados para problemas de química, Gabriel Braun, 2022

Esse módulo implementa funções para converter entre diferentes formadts.
"""
import braunchem.utils.latex2 as latex

import os
import sys
import subprocess
from shutil import copy, SameFileError
from pathlib import Path

import pypandoc
import bs4


MARKDOWN_EXTENSIONS = [
    "task_lists",
    "table_captions",
    "pipe_tables",
    "implicit_figures",
]
"""Extensões de markdown utilizadas"""

PANDOC_MARKDOWN_FORMAT = (
    f"markdown_strict-raw_html+tex_math_dollars+{'+'.join(MARKDOWN_EXTENSIONS)}"
)
"""Formato markdown para o pandoc."""

PANDOC_LATEX_FORMAT = "latex"
"""Formato LaTeX para o pandoc."""

PANDOC_HTML_FORMAT = "html+tex_math_dollars"
"""Formato HTML para o pandoc."""


def html2md(html_str: str) -> str:
    """Converte HTML em markdown usando pandoc."""
    md_str = pypandoc.convert_text(
        source=html_str,
        to=PANDOC_MARKDOWN_FORMAT,
        format=PANDOC_HTML_FORMAT,
        extra_args=["--quiet"],
    )
    return md_str


def md2html(md_str: str) -> str:
    """Converte markdown em HTML usando pandoc."""
    html_str = pypandoc.convert_text(
        source=md_str,
        to=PANDOC_HTML_FORMAT,
        format=PANDOC_MARKDOWN_FORMAT,
        extra_args=["--quiet"],
    )
    return html_str


def html2tex(html_str: str) -> str:
    """Converte HTML em LaTeX usando pandoc."""
    tex_str = pypandoc.convert_text(
        source=html_str,
        to=PANDOC_LATEX_FORMAT,
        format=PANDOC_HTML_FORMAT,
        extra_args=["--quiet"],
    )
    tex_str = latex.pu2qty(tex_str)
    return tex_str


def md2tex(md_string: str) -> str:
    """Converte markdown em LaTeX usando pandoc."""
    tex_str = pypandoc.convert_text(
        source=md_string,
        to=PANDOC_LATEX_FORMAT,
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


def copy_r(loc, dest):
    try:
        copy(loc, dest)
    except SameFileError:
        pass


def copy_all(loc, dest):
    for f in os.listdir(loc):
        copy_r(os.path.join(loc, f), dest)


def latexmk(tex_file: str):
    subprocess.run(
        [
            "latexmk",
            "-shell-escape",
            "-interaction=nonstopmode",
            "-file-line-error",
            "-pdf",
            f"{tex_file}",
        ],
        stdout=subprocess.DEVNULL,
    )


def tex2pdf(tex_contents, filename, tmp_path="temp", out_path="archive", svg=False):
    # convert tex string to pdf
    cwd = Path.cwd()

    temp = Path(tmp_path)
    temp.mkdir(parents=True, exist_ok=True)

    # copy latex template files to temp folder
    copy_all("src/braunchem/latex", temp)

    os.chdir(temp)

    with open(f"{filename}.tex", "w") as f:
        f.write(tex_contents)

    subprocess.run(
        [
            "latexmk",
            "-shell-escape",
            "-interaction=nonstopmode",
            "-file-line-error",
            "-pdf",
            f"{filename}.tex",
        ],
        stdout=subprocess.DEVNULL,
    )
    print(f"Complilando o arquivo {filename}.tex")

    if not os.path.exists(f"{filename}.pdf"):
        sys.exit(f"Falha na compilação do arquivo '{filename}.tex'!")

    if svg:
        subprocess.run(
            [
                "pdf2svg",
                f"{filename}.pdf",
                f"{filename}.svg",
            ],
            stdout=subprocess.DEVNULL,
        )

    os.chdir(cwd)

    out = Path(out_path)
    out.mkdir(parents=True, exist_ok=True)

    if svg:
        copy_r(
            os.path.join(temp, f"{filename}.svg"), os.path.join(out, f"{filename}.svg")
        )
    else:
        copy_r(
            os.path.join(temp, f"{filename}.pdf"), os.path.join(out, f"{filename}.pdf")
        )


def tikz2svg(tikz_path, tmp_path="temp/images", out_path="data/images"):
    # convert tikz image file to svg for web
    tikz = Path(tikz_path)
    filename = tikz.stem
    input_path = os.path.relpath(tikz, tmp_path)

    tex_contents = latex.cmd("documentclass", "braunfigure") + latex.env(
        "document", latex.cmd("input", input_path)
    )

    tex2pdf(tex_contents, filename, tmp_path, out_path, svg=True)
