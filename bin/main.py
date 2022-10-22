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

    topic_db = TopicSet.parse_database(config.TOPICS_DIR)

    focus_db = FocusSet.parse_database(config.FOCUSES_DIR)

    topic_db["3H"].write_pdf(
        problem_db,
        tmp_dir=config.TMP_TOPICS_DIR,
        out_dir=config.OUT_DIR,
    )

    # SEND FILES TO BRAUNCHEM-WEB
    for db_file in [
        config.PROBLEMS_DIR.joinpath("problems.json"),
        config.TOPICS_DIR.joinpath("topics.json"),
        config.FOCUSES_DIR.joinpath("focuses.json"),
    ]:
        shutil.copy(
            db_file,
            f"../braunchem-web/database/{db_file.name}",
        )


if __name__ == "__main__":
    main()
