import braunchem.utils.config as config
from braunchem.problem import ProblemSet
from braunchem.topic import TopicSet
from braunchem.focus import FocusSet

import logging


def main():
    logging.basicConfig(level=logging.INFO, filename="bin/main.log", filemode="w")

    config.load_config("bin/config.cfg")

    problem_db = ProblemSet.parse_database(config.PROBLEMS_DIR)
    topic_db = TopicSet.parse_database(config.TOPICS_DIR, problem_db)

    # topic_db.write_pdfs(tmp_dir=config.TMP_TOPICS_DIR, out_dir=config.OUT_DIR)

    focus_db = FocusSet.parse_database(config.FOCUSES_DIR, topic_db)


if __name__ == "__main__":
    main()
