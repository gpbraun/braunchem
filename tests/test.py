from braunchem.problem import Problem

import time
import logging


def main():
    logging.basicConfig(level=logging.DEBUG, filename='tests/test.log', filemode='w')
    p = Problem.parse_mdfile("tests/test-problem.md")


if __name__ == "__main__":
    start_time = time.time()
    main()
    dt = time.time() - start_time
    print(f"\nFinalizado em {dt:.2f} segundos.")
