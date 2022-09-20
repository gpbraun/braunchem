from braunchem.problem2 import Problem

import time


def main():
    p = Problem.parse_file("tests/test-problem.md")
    print(p.statement.tex)
    # print(p.statement.md)


if __name__ == "__main__":
    start_time = time.time()
    main()
    dt = time.time() - start_time
    print(f"\nFinalizado em {dt:.2f} segundos.")
