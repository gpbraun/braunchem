#
# DOME - Gabriel Braun, 2021
#

# TODO:
# - Gerar o "elements"
# - Usar o GitHub Actions para rodar esse script automaticamente


# REQUIREMENTS

import os

import attr
from attr import frozen, Factory, asdict, fields

# import pickle
from json import dump as json_dump

from sys import exit
from pathlib import Path

import convert
from problem import ProblemSet, file2problem
from topic import Topic, List


#
# ARSENAL CLASS
#

@frozen
class Arsenal:
    path: str
    topics: list[Topic] = Factory(list)
    problems: dict = Factory(dict)

    def dump(self):
        # dump contents to pickle
        # pickle_file = os.path.join(self.path, 'arsenal.p')
        # with open(pickle_file, 'wb') as f:
        #     pickle.dump(self, f)

        # dump contents to json
        filters = attr.filters.exclude(
            fields(Topic).path,
        )

        json_file = os.path.join(self.path, 'arsenal.json')
        with open(json_file, 'w') as f:
            json_dump(
                asdict(self, filter=filters), f, indent=2, ensure_ascii=False
            )

    def filter(self, title, problem_ids):
        # get ProblemSet from list of ids
        return ProblemSet(title, [self.problems[i] for i in problem_ids])

    def aspdf(self, topic_ids):
        # compile list pdf for lists with id in topic_ids
        for topic in self.topics:
            if topic.id in topic_ids:
                psets = [self.filter(t, p) for t, p in topic.problems.items()]

                this_list = List(topic.id, topic.title, psets)
                print('compiling latex list')
                convert.tex2pdf(this_list.astex(), topic.id, path='archive')


def get_file_paths(db_path):
    # get the path of all problems and topics
    topic_files = []
    problem_files = []

    for root, _, files in os.walk(os.path.join(db_path, 'topics')):
        for f in files:
            path = Path(os.path.join(root, f))
            if path.suffix == '.md':
                topic_files.append(path)

    for root, _, files in os.walk(os.path.join(db_path, 'problems')):
        for f in files:
            path = Path(os.path.join(root, f))
            # problems
            if path.suffix == '.md':
                problem_files.append(path)
            # topics
            elif path.suffix in ['.jpg', '.jpeg', '.svg', '.pdf', '.tex']:
                convert.copyr(path, os.path.join(db_path, 'images', path.name))

    return topic_files, problem_files


def load_arsenal(path):
    # generate arsenal by walking on directory
    if not os.path.exists(path):
        exit(f"O diretório '{path}' não existe!")

    topic_files, problem_files = get_file_paths(path)

    topics = []
    for t in topic_files:
        print(t)
        topics.append(Topic(t))
    topics = [Topic(t) for t in topic_files]
    problems = {p.stem: file2problem(p) for p in problem_files}

    ars = Arsenal(path, topics, problems)

    ars.dump()

    # pickle_file = os.path.join(path, 'arsenal.p')
    # if os.path.exists(pickle_file):
    #     with open(pickle_file, 'rb') as f:
    #         print("Arquivo '%s' carregado" % pickle_file)
    #         return pickle.load(f)
    return ars

#
# PDF LIST CLASS
#


#
# MAIN
#


def main():
    data = load_arsenal('database')
    data.aspdf(['2A'])


if __name__ == "__main__":
    main()
