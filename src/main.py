#
# DOME - Gabriel Braun, 2021
#

from topic import load_arsenal
from convert import copy_r


def main():
    arsenal = load_arsenal('database')
    arsenal.generate_pdfs()

    copy_r(
        'database/arsenal.json',
        '/home/braun/Documents/Developer/BraunChem/database/arsenal.json'
    )


if __name__ == "__main__":
    main()
