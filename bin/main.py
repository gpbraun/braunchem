import braunchem.utils.config as config
from braunchem.problem import ProblemSet
from braunchem.topic import TopicSet
from braunchem.utils.convert import get_database_paths

import logging
from pathlib import Path


def main():
    logging.basicConfig(level=logging.DEBUG, filename="bin/main.log", filemode="w")

    config.load_config("bin/config.cfg")

    problem_paths = get_database_paths(config.PROBLEMS_DIR)
    topic_paths = get_database_paths(config.TOPICS_DIR)

    # problemas
    problem_db_path = config.PROBLEMS_DIR.joinpath("problems.json")
    try:
        problem_db = ProblemSet.parse_file(problem_db_path)
        problem_db.update_problems(problem_paths)
    except FileNotFoundError:
        problem_db = ProblemSet.parse_paths(problem_paths)

    problem_db_path.write_text(
        problem_db.json(indent=2, ensure_ascii=False), encoding="utf-8"
    )

    problem_db.write_texfiles()

    # tópicos
    topic_db_path = config.TOPICS_DIR.joinpath("topic.json")
    try:
        topic_db = TopicSet.parse_file(topic_db_path)
        topic_db.update_topics(topic_paths, problem_db=problem_db)
    except FileNotFoundError:
        topic_db = TopicSet.parse_paths(topic_paths, problem_db=problem_db)

    topic_db_path.write_text(
        topic_db.json(indent=2, ensure_ascii=False), encoding="utf-8"
    )

    topic_db.pdf()


if __name__ == "__main__":
    main()
