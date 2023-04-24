from pathlib import Path
import braunchem.utils.converter as converter

import json


def main():
    test_file = Path("test/test.md")
    md_text = test_file.read_text()

    problem_json = converter.md2problem(md_text)
    problem_json_str = json.dumps(problem_json, indent=4, ensure_ascii=False)

    json_file = Path("test/test_problem.json")
    json_file.touch(exist_ok=True)
    json_file.write_text(problem_json_str)

    print(problem_json["statement"]["latex"])


if __name__ == "__main__":
    main()
