#
# DOME - Gabriel Braun, 2021
#

from topic import load_arsenal


def main():
    arsenal = load_arsenal('database')
    arsenal.generate_pdfs()


if __name__ == "__main__":
    main()
