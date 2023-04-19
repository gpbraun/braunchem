from pathlib import Path
import braunchem.utils.text as text

import json


def main():
    test_file = Path("test/test.md")
    md_text = test_file.read_text()

    # json_text = json.loads(text.md2json(md_text))
    # json_text = json.dumps(json_text, indent=2, ensure_ascii=False)
    # print(json_text)

    problem_json = json.loads(text.md2problem(md_text))
    problem_json = json.dumps(problem_json, indent=2, ensure_ascii=False)
    print(problem_json)


if __name__ == "__main__":
    main()
