#
# CONVERSION
#

import os

from sys import exit
from subprocess import run, DEVNULL
from shutil import copy, SameFileError

from bs4 import BeautifulSoup
from pypandoc import convert_text
from markdown import Markdown

from pathlib import Path

import latex


MD = Markdown(extensions=['pymdownx.tasklist', 'markdown.extensions.tables'])


def md2soup(content):
    # convert markdown to html and parse as soup
    content = content.replace('\\\\', '\\\\\\')
    return BeautifulSoup(MD.convert(content), 'html.parser')


def html2md(content):
    # convert md to html using pandoc and parse as soup
    return convert_text(
        content, 'commonmark_x',
        format='html+tex_math_dollars+raw_tex'
    )


def soup_split(soup, tag):
    split_tag = soup.find(tag)
    if not split_tag:
        return [soup, '']

    splited = str(soup).split(str(split_tag), 1)
    return map(lambda s: BeautifulSoup(s, 'html.parser'), splited)


EXTENSIONS = ''.join([
    '+', 'task_lists',
    '+', 'table_captions',
    '+', 'pipe_tables',
    '+', 'implicit_figures',
])


def md2tex(content):
    # convert html string to tex using pandoc
    return convert_text(
        content, 'tex',
        format=f'markdown_strict+tex_math_dollars+raw_tex{EXTENSIONS}',
    ).replace('\\tightlist', '')


def copy_r(loc, dest):
    try:
        copy(loc, dest)
    except SameFileError:
        pass


def copy_all(loc, dest):
    for f in os.listdir(loc):
        copy_r(os.path.join(loc, f), dest)


def tex2pdf(tex_contents, filename, tmp_path='temp', out_path='archive',
            svg=False):
    # convert tex string to pdf
    cwd = Path.cwd()

    temp = Path(tmp_path)
    temp.mkdir(parents=True, exist_ok=True)

    # copy latex template files to temp folder
    copy_all('src/latex', temp)

    os.chdir(temp)

    with open(f'{filename}.tex', 'w') as f:
        f.write(tex_contents)

    run(
        ['latexmk',
         '-shell-escape',
         '-interaction=nonstopmode',
         '-file-line-error',
         '-pdf',
         f'{filename}.tex'],
        stdout=DEVNULL,
    )

    if not os.path.exists(f'{filename}.pdf'):
        exit(f"Falha na compilação do arquivo '{filename}.tex'!")

    if svg:
        run(
            ['pdf2svg',
             f'{filename}.pdf',
             f'{filename}.svg', ],
            stdout=DEVNULL,
        )

    os.chdir(cwd)

    out = Path(out_path)
    out.mkdir(parents=True, exist_ok=True)

    if svg:
        copy_r(
            os.path.join(temp, f'{filename}.svg'),
            os.path.join(out, f'{filename}.svg')
        )
    else:
        copy_r(
            os.path.join(temp, f'{filename}.pdf'),
            os.path.join(out, f'{filename}.pdf')
        )


def tikz2svg(tikz_path, tmp_path='temp/images', out_path='database/images'):
    # convert tikz image file to svg for web
    tikz = Path(tikz_path)
    filename = tikz.stem
    input_path = os.path.relpath(tikz, tmp_path)

    tex_contents = latex.cmd('documentclass', 'braunfigure') + \
        latex.env('document', latex.cmd('input', input_path))

    tex2pdf(tex_contents, filename, tmp_path, out_path, True)
