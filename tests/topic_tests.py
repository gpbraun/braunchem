from braunchem.problem import ProblemSet
from braunchem.topic import Topic


def main():
    problem_db = ProblemSet.parse_file("data/problems/problems.json")

    t = Topic.parse_mdfile(topic_path="tests/data/test_topic.md", problem_db=problem_db)

    for p in t.problem_sets:
        print(p.tex_statements())


if __name__ == "__main__":
    main()
