import braunchem.utils.config as config
from braunchem.problem import ProblemSet
from braunchem.topic import TopicSet
from braunchem.focus import FocusSet

import logging
import shutil


def main():
    logging.basicConfig(level=logging.INFO, filename="bin/main.log", filemode="w")

    config.load_config("bin/config.cfg")

    problem_db = ProblemSet.parse_database(config.PROBLEMS_DIR)
    topic_db = TopicSet.parse_database(config.TOPICS_DIR, problem_db, force_update=True)

    # topic_db.write_pdfs(tmp_dir=config.TMP_TOPICS_DIR, out_dir=config.OUT_DIR)

    focus_db = FocusSet.parse_database(config.FOCUSES_DIR, topic_db)

    print(topic_db["3A"].tex())

    shutil.copy(
        config.FOCUSES_DIR.joinpath("focuses.json"),
        "../braunchem-web/database/database.json",
    )


if __name__ == "__main__":
    main()
