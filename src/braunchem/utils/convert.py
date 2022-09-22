"""Base de dados para problemas de química, Gabriel Braun, 2022

Esse módulo implementa funções para conversão entre diferentes formatos.
"""
import braunchem.utils.latex as latex

import os
import sys
import subprocess
import shutil
from pathlib import Path

import pypandoc
import bs4


MARKDOWN_EXTENSIONS = [
    "task_lists",
    "table_captions",
    "pipe_tables",
    "implicit_figures",
    "fenced_divs",
]
"""Extensões de markdown utilizadas"""

PANDOC_MARKDOWN_FORMAT = (
    f"markdown_strict-raw_html+tex_math_dollars+raw_tex+{'+'.join(MARKDOWN_EXTENSIONS)}"
)
"""Formato markdown para o pandoc."""

PANDOC_HTML_FORMAT = "html+tex_math_dollars+raw_tex"
"""Formato HTML para o pandoc."""

PANDOC_LATEX_FORMAT = "latex"
"""Formato LaTeX para o pandoc."""


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
        shutil.copy(loc, dest)
    except shutil.SameFileError:
        pass


def copy_all(loc, dest):
    for f in os.listdir(loc):
        copy_r(os.path.join(loc, f), dest)


def latexmk(tex_file_name: str):
    subprocess.run(
        [
            "latexmk",
            "-shell-escape",
            "-interaction=nonstopmode",
            "-file-line-error",
            "-pdf",
            f"{tex_file_name}",
        ],
        stdout=subprocess.DEVNULL,
    )


def tex2pdf(tex_contents, filename, tmp_path="temp", out_path="archive"):
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

    os.chdir(cwd)

    out = Path(out_path)
    out.mkdir(parents=True, exist_ok=True)


def pdf2svg(tex_file_name: str):
    subprocess.run(
        [
            "pdf2svg",
            f"{tex_file_name}.pdf",
            f"{tex_file_name}.svg",
        ],
        stdout=subprocess.DEVNULL,
    )
    return


def tikz2svg(tikz_path, tmp_path="temp/images", out_path="data/images"):
    # convert tikz image file to svg for web
    tikz = Path(tikz_path)
    filename = tikz.stem
    input_path = os.path.relpath(tikz, tmp_path)

    tex_contents = latex.cmd("documentclass", "braunfigure") + latex.env(
        "document", latex.cmd("input", input_path)
    )

    tex2pdf(tex_contents, filename, tmp_path, out_path, svg=True)
