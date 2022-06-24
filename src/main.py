#
# Gabriel Braun, 2021
#

from topic import load_arsenal
from convert import copy_r
from shutil import copytree


def main():
    arsenal = load_arsenal('database')
    arsenal.generate_pdfs()

    copy_r(
        'database/arsenal.json',
        '/home/braun/Documents/Developer/braunchem-web/database/arsenal.json'
    )

    copytree(
        'database/images/',
        '/home/braun/Documents/Developer/braunchem-web/public/',
        dirs_exist_ok=True
    )

    copytree(
        'out/',
        '/home/braun/Documents/Drive/Material/Listas',
        dirs_exist_ok=True
    )


if __name__ == "__main__":
    main()
