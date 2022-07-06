from dataclasses import dataclass, field
from pathlib import Path
from bs4 import BeautifulSoup
from pypandoc import convert_text
from quantities import Table


def md2html(content):
    """Convert markdown to html using pandoc and parse as soup."""
    return convert_text(
        content, 'html',
        format='markdown-tex_math_dollars-raw_tex'
    )


def md2soup(content):
    # convert markdown to html and parse as soup
    content = content.replace('\\\\', '\\\\\\')
    return BeautifulSoup(md2html(content), 'html.parser')


@dataclass
class Problem:
    id_: str
    path: Path 
    statement: str
    solution: str = None
    answer: list[str] = field(default_factory=list)
    choices: list[str] = field(default_factory=list)
    obj: int = None
    constants: Table = field(default_factory=Table)
    data: Table = field(default_factory=Table)


def main():
    with open('braunchem/v2-test/test-problems/1A01-test.md', 'r') as file:
        data = file.read()

    print(md2html(data))


if __name__ == "__main__":
    main()
