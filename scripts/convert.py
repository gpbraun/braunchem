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


MD = Markdown(extensions=['pymdownx.tasklist'])


def md2soup(content):
    content = content.replace('\\\\', '\\\\\\')
    return BeautifulSoup(MD.convert(content), 'html.parser')


def html2md(content):
    # convert md to html using pandoc and parse as soup
    return convert_text(
        content, 'md',
        format='html+tex_math_dollars+raw_tex'
    )


def md2tex(content):
    # convert html string to tex using pandoc
    return convert_text(
        content, 'tex',
        format='markdown+tex_math_dollars+raw_tex',
    ).replace('\\tightlist', '')


def copy_r(loc, dest):
    try:
        copy(loc, dest)
    except SameFileError:
        pass


def copy_all(loc, dest):
    for f in os.listdir(loc):
        copy_r(os.path.join(loc, f), dest)


def tex2pdf(tex_contents, filename, tmp_path='temp', out_path='archive'):
    # convert tex string to pdf
    cwd = Path.cwd()

    temp = Path(os.path.join(tmp_path, filename))
    temp.mkdir(parents=True, exist_ok=True)

    # copy latex template files to temp folder
    copy_all('scripts/latex', temp)

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

    os.chdir(cwd)

    out = Path(out_path)
    out.mkdir(parents=True, exist_ok=True)

    copy_r(
        os.path.join(temp, f'{filename}.pdf'),
        os.path.join(out, f'{filename}.pdf')
    )
