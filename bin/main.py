import braunchem.utils.config as config
from braunchem.problem import ProblemSet
from braunchem.topic import TopicSet


import logging
from pathlib import Path


def main():
    logging.basicConfig(level=logging.DEBUG, filename="bin/main.log", filemode="w")

    config.load_config("bin/config.cfg")

    problem_db = ProblemSet.get_database(
        config.PROBLEMS_DIR, config.PROBLEMS_DIR.joinpath("problems.json")
    )

    topic_db = TopicSet.get_database(
        config.TOPICS_DIR,
        config.TOPICS_DIR.joinpath("topics.json"),
        problem_db,
        # force_update=True,
    )

    topic_db.pdf()


if __name__ == "__main__":
    main()
