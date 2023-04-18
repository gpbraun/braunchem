from pathlib import Path
import braunchem.utils.text as text


def main():
    test_file = Path("test/test.md")
    md_text = test_file.read_text()

    tex_text = text.md2tex(md_text)
    print(tex_text)


if __name__ == "__main__":
    main()
