#
# DOME - Gabriel Braun, 2021
#

from topic import load_arsenal
from convert import copy_r, copy_all


def main():
    arsenal = load_arsenal('database')
    arsenal.generate_pdfs()

    copy_r(
        'database/arsenal.json',
        '/home/braun/Documents/Developer/BraunChem/database/arsenal.json'
    )

    for q in ['Q1', 'Q2', 'Q3']:
        copy_all(
            f'archive/{q}',
            '/home/braun/Documents/Drive/Material/Listas'
        )


if __name__ == "__main__":
    main()
