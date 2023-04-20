from pathlib import Path
import braunchem.utils.converter as converter

import json


def main():
    test_file = Path("test/test.md")
    md_text = test_file.read_text()

    problem_json = converter.md2problem(md_text)
    problem_jsons = json.dumps(problem_json, indent=2, ensure_ascii=False)
    print(problem_jsons)


if __name__ == "__main__":
    main()
