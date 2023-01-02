import logging
import shutil
from pathlib import Path

import braunchem.utils.config as config
from braunchem.focus import FocusSet
from braunchem.problem import ProblemSet
from braunchem.topic import TopicSet

WEB_PATH = Path("/home/braun/Documents/Developer/braunchem-web")


def main():
    logging.basicConfig(level=logging.INFO, filename="bin/main.log", filemode="w")

    config.load_config("bin/config.cfg")

    problem_db = ProblemSet.parse_database(config.PROBLEMS_DIR)
    topic_db = TopicSet.parse_database(config.TOPICS_DIR)
    focus_db = FocusSet.parse_database(config.FOCUSES_DIR)

    topic_db["2K"].write_pdf(
        problem_db,
        tmp_dir=config.TMP_TOPICS_DIR,
        out_dir=config.OUT_DIR,
    )

    # COPIA A BASE DE DADOS PARA O SITE
    for db_file in [
        config.PROBLEMS_DIR.joinpath("problems.json"),
        config.TOPICS_DIR.joinpath("topics.json"),
        config.FOCUSES_DIR.joinpath("focuses.json"),
    ]:
        shutil.copy(db_file, WEB_PATH.joinpath("database", db_file.name))
    # COPIA AS IMAGENS PARA O SITE
    shutil.copytree(
        config.IMAGES_DIR, WEB_PATH.joinpath("public", "images"), dirs_exist_ok=True
    )


if __name__ == "__main__":
    main()
