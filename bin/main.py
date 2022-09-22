from braunchem.problem import get_problem_paths, ProblemSet
from braunchem.topic import get_topic_paths, TopicSet

import logging
from pathlib import Path


def main():
    logging.basicConfig(level=logging.INFO)

    problem_paths = get_problem_paths("data/problems")
    topic_paths = get_topic_paths("data/topics")

    # problemas
    problem_db_path = Path("data/problems/problems.json")
    # try:
    #     problem_db = ProblemSet.parse_file(problem_db_path)
    #     problem_db.update_problems(problem_paths)
    # except FileNotFoundError:
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
