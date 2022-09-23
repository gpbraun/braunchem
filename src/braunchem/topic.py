"""Base de dados para problemas de química, Gabriel Braun, 2022

Esse módulo implementa uma classe para os tópicos.
"""
import braunchem.utils.convert as convert
from braunchem.problem import Text, ProblemSet

import os
import logging
import importlib.resources
from datetime import datetime
from pathlib import Path
from pydantic import BaseModel

import frontmatter


DB_PATH = importlib.resources.files("braunchem.data")
"""Diretório da base de dados."""


class Topic(BaseModel):
    """Tópico.

    Atributos:
        id_ (str): Identificador único.
        title (str): Título do tópico.
        author (str): Autor da teoria.
        content (str): Conteúdo teórico.
        sections (list[str]): Títulos das seções.
        problem_sets (list[ProblemSet]): Conjuntos de problemas.
    """

    id_: str
    path: Path
    date: datetime
    title: str
    author: str = "Gabriel Braun"
    content: Text
    sections: list[str]
    problem_sets: list[ProblemSet] | None = None

    def __lt__(self, other):
        return self.id_ < other.id_

    @classmethod
    def parse_mdfile(cls, topic_path: str | Path, problem_db: ProblemSet):
        """Cria um `Topic` a partir de um arquivo `.md`."""
        if isinstance(topic_path, str):
            path = Path(topic_path)
        else:
            path = topic_path

        # parse `.md`. with YAML metadata
        tfile = frontmatter.load(path)

        # basic info
        topic = {
            "id_": path.stem,
            "path": path.resolve(),
            "date": datetime.utcfromtimestamp(path.stat().st_mtime),
        }

        # extrair os metadados do arquivo `.md`
        for attr in ["title", "author", "affiliation", "template"]:
            if attr in tfile:
                topic[attr] = tfile[attr]

        # extrair a lista de problemas
        if "problems" in tfile:
            problem_sets = []
            for i, (title, p_ids) in enumerate(tfile["problems"].items()):
                set_id = f"{topic['id_']}{i+1}"
                problem_sets.append(
                    problem_db.filter(id_=set_id, title=title, p_ids=p_ids)
                )
            topic["problem_sets"] = problem_sets

        # extrair o título das seções
        soup = convert.md2soup(tfile.content)
        topic["sections"] = [s.text for s in soup.find_all("h1")]

        # conteúdo
        topic["content"] = Text.parse_md(tfile.content)

        return cls.parse_obj(topic)


class TopicSet(BaseModel):
    """Tópico.

    Atributos:
        date (datetime): Data.
        topics (list[str]): Conjuntos de tópicos.
    """

    date: datetime
    topics: list[Topic]

    def __len__(self):
        return len(self.topics)

    def __iter__(self):
        return iter(self.topics)

    def __getitem__(self, key: str):
        try:
            return [topic for topic in self if topic.id_ == key][0]
        except IndexError:
            raise KeyError

    def update_topics(self, paths: list[str] | list[Path], problem_db: ProblemSet):
        """Atualiza os problemas do `ProblemSet`."""
        updated_topics = []

        for path in paths:
            t_id_ = path.stem
            path_date = datetime.utcfromtimestamp(path.stat().st_mtime)

            try:
                if self[t_id_].date < path_date:
                    logging.warning(f"Tópico {t_id_} atualizado.")
                    updated_topics.append(
                        Topic.parse_mdfile(path, problem_db=problem_db)
                    )
                else:
                    updated_topics.append(self[t_id_])
            except KeyError:
                updated_topics.append(Topic.parse_mdfile(path, problem_db=problem_db))

        self.topics = updated_topics

    @classmethod
    def parse_paths(cls, paths: list[str] | list[Path], problem_db: ProblemSet):
        """Cria um `TopicSet` com os endereços problemas fornecidos."""
        topics = []

        for path in paths:
            topics.append(Topic.parse_mdfile(topic_path=path, problem_db=problem_db))

        return cls(date=datetime.now(), topics=sorted(topics))


def get_topic_paths(topic_db_path):
    """Retorna os endereço dos arquivos `.md` de tópicoss."""
    topic_files = []

    for root, _, files in os.walk(topic_db_path):
        for f in files:
            path = Path(os.path.join(root, f))

            # topicos
            if path.suffix == ".md":
                topic_files.append(path)

    return topic_files
