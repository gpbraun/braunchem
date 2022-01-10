#
# CONVERSION
#

import os

from sys import exit
from subprocess import run, DEVNULL
from shutil import move, copy, SameFileError

from bs4 import BeautifulSoup
from pypandoc import convert_text
from markdown import Markdown
from markdownify import markdownify


MD = Markdown(extensions=['pymdownx.tasklist'])


def md2soup(content):
    return BeautifulSoup(MD.convert(content), 'html.parser')


def html2md(content):
    # convert md to html using pandoc and parse as soup
    #return markdownify(str(content))
    return convert_text(str(content), 'md', format='html+tex_math_dollars+raw_tex')


def md2tex(content):
    # convert html string to tex using pandoc
    return convert_text(
       str(content), 'tex',
       format='markdown+tex_math_dollars+raw_tex',
    ).replace('\\tightlist', '')


def copyr(loc, dest):
    try:
        copy(loc, dest)
    except SameFileError:
        pass


def tex2pdf(tex, filename, path='', clear=True):
    # convert tex string to pdf
    cwd = os.getcwd()
    os.chdir('template')

    with open(f'{filename}.tex', 'w') as f:
        f.write(tex)

    # run(
    #     ['pdflatex', '-interaction=nonstopmode', f'{filename}.tex'],
    #     stdout=DEVNULL,
    # )

    # if not os.path.exists(f'{filename}.pdf'):
    #     exit(f"Falha na compilação do arquivo '{filename}.tex'!")

    # # clear output files
    # if clear:
    #     for ext in ['.tex', '.aux', '.log', '.out']:
    #         os.remove(filename + ext)

    os.chdir(cwd)

    # move(
    #     os.path.join('template', f'{filename}.pdf'),
    #     os.path.join(path, f'{filename}.pdf')
    # )
