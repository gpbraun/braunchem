#
# Gabriel Braun, 2021
#

from braunchem.legacy.topic import load_arsenal
from braunchem.legacy.convert import copy_r
from shutil import copytree


def main():
    arsenal = load_arsenal("data")
    arsenal.generate_pdfs()

    copy_r(
        "data/arsenal.json",
        "/home/braun/Documents/Developer/braunchem-web/database/arsenal.json",
    )

    copytree(
        "data/images/",
        "/home/braun/Documents/Developer/braunchem-web/public/",
        dirs_exist_ok=True,
    )

    copytree("out/", "/home/braun/Documents/Drive/Material/Listas", dirs_exist_ok=True)


if __name__ == "__main__":
    main()
