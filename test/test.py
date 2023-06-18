import json
from pathlib import Path

from problem2 import Problem

import braunchem.utils.converter as converter


def test_problem():
    test_file = Path("test/problem/test_problem.md")
    problem = Problem.parse_mdfile(test_file)

    # md_text = test_file.read_text()

    # problem_json = converter.md2problem(md_text)
    # problem_json_str = json.dumps(problem_json, indent=4, ensure_ascii=True)

    # json_file = Path("test/problem/test_problem.json")
    # json_file.touch(exist_ok=True)
    # json_file.write_text(problem_json_str)

    tex_file = Path("test/problem/test_problem.tex")
    tex_file.touch(exist_ok=True)
    tex_file.write_text(problem.render_latex())

    # html_file = Path("test/problem/test_problem.html")
    # html_file.touch(exist_ok=True)
    # html_file.write_text(problem_json["statement"]["html"])


def test_section():
    test_file = Path("test/section/test_section.md")
    md_text = test_file.read_text()

    problem_json = converter.md2section(md_text)
    problem_json_str = json.dumps(problem_json, indent=4, ensure_ascii=True)

    json_file = Path("test/section/test_section.json")
    json_file.touch(exist_ok=True)
    json_file.write_text(problem_json_str)

    tex_file = Path("test/section/test_section.tex")
    tex_file.touch(exist_ok=True)
    tex_file.write_text(problem_json["content"]["latex"])

    html_file = Path("test/section/test_section.html")
    html_file.touch(exist_ok=True)
    html_file.write_text(problem_json["content"]["html"])


def main():
    test_problem()


if __name__ == "__main__":
    main()
