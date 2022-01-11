#
# DOME - Gabriel Braun, 2021
#

# TODO:
# - Gerar o "elements"

# REQUIREMENTS

import os

from attr import frozen, Factory, asdict, filters, fields

# import pickle
from json import dump as json_dump

from sys import exit
from pathlib import Path

from problem import Problem, ProblemSet, files2problemset
from topic import Topic, file2topic


#
# ARSENAL CLASS
#

@frozen
class Arsenal:
    problems: ProblemSet
    topics: list[Topic] = Factory(list)

    def dump(self, path):
        # dump contents to pickle
        # pickle_file = os.path.join(self.path, 'arsenal.p')
        # with open(pickle_file, 'wb') as f:
        #     pickle.dump(self, f)

        # dump contents to json
        flter = filters.exclude(
            fields(Problem).path,
            fields(Arsenal).problems
        )

        json_file = os.path.join(path, 'arsenal.json')

        with open(json_file, 'w') as f:
            json_dump(
                asdict(self, filter=flter), f, indent=2, ensure_ascii=False
            )

    def generate_pdfs(self):
        for topic in self.topics:
            topic.compile_pdf()


def get_file_paths(db_path):
    # get the path of all problems and topics
    problem_files = []
    topic_files = []

    for root, _, files in os.walk(os.path.join(db_path, 'problems')):
        for f in files:
            path = Path(os.path.join(root, f))
            # problems
            if path.suffix == '.md':
                problem_files.append(path)

    for root, _, files in os.walk(os.path.join(db_path, 'topics')):
        for f in files:
            path = Path(os.path.join(root, f))
            if path.suffix == '.md':
                topic_files.append(path)

    return problem_files, topic_files


def load_arsenal(path):
    # generate arsenal by walking on directory
    if not os.path.exists(path):
        exit(f"O diretório '{path}' não existe!")

    problem_files, topic_files = get_file_paths(path)

    problem_set = files2problemset(problem_files)
    topics = [file2topic(t, problem_set) for t in topic_files]

    ars = Arsenal(problem_set, topics)

    ars.dump(path)

    # pickle_file = os.path.join(path, 'arsenal.p')
    # if os.path.exists(pickle_file):
    #     with open(pickle_file, 'rb') as f:
    #         print("Arquivo '%s' carregado" % pickle_file)
    #         return pickle.load(f)
    return ars


#
# MAIN
#


def main():
    data = load_arsenal('database')
    data.generate_pdfs()


if __name__ == "__main__":
    main()
