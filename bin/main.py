from braunchem.problem import ProblemSet
from braunchem.topic import TopicSet
from braunchem.utils.convert import get_database_paths
from braunchem.utils.config import load_config, CONFIG

import logging
from pathlib import Path


def main():
    logging.basicConfig(level=logging.DEBUG, filename="bin/main.log", filemode="w")

    load_config("bin/config.cfg")

    problem_paths = get_database_paths(CONFIG["paths"]["problems"])
    topic_paths = get_database_paths(CONFIG["paths"]["topics"])

    # problemas
    problem_db_path = Path("data/problems/problems.json")
    try:
        problem_db = ProblemSet.parse_file(problem_db_path)
        problem_db.update_problems(problem_paths)
    except FileNotFoundError:
        problem_db = ProblemSet.parse_paths(problem_paths)

    with open(problem_db_path, "w", encoding="utf-8") as problem_json:
        problem_json.write(problem_db.json(indent=2, ensure_ascii=False))

    # tópicos
    topic_db_path = Path("data/topics/topics.json")
    try:
        topic_db = TopicSet.parse_file(topic_db_path)
        topic_db.update_topics(topic_paths, problem_db=problem_db)
    except FileNotFoundError:
        topic_db = TopicSet.parse_paths(topic_paths, problem_db=problem_db)

    with open(topic_db_path, "w", encoding="utf-8") as topic_json:
        topic_json.write(topic_db.json(indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
