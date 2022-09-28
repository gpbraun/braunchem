"""Base de dados para problemas de química, Gabriel Braun, 2022

Esse módulo implementa uma classe para os tópicos.
"""
import braunchem.utils.convert as convert
import braunchem.utils.config as config
import braunchem.utils.latex as latex
from braunchem.problem import Text, ProblemSet

import logging
import importlib.resources
from datetime import datetime
from pathlib import Path
from pydantic import BaseModel
from multiprocessing import Pool

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
    area: str
    title: str
    author: str = "Gabriel Braun"
    affiliation: str = "Colégio e Curso Pensi, Coordenação de Química"
    content: Text
    sections: list[str]
    problem_sets: list[ProblemSet] | None = None

    def tex_answers(self):
        """ "Retorna o gabarito dos problemas do tópico em LaTeX."""
        if not self.problem_sets:
            return ""

        header = latex.section("Gabarito", level=0, numbered=False)
        answers = "\n".join(
            problem_set.tex_answers() for problem_set in self.problem_sets
        )
        return header + answers

    def tex_statements(self):
        """Retorna os problemas do tópico em LaTeX."""
        if not self.problem_sets:
            return ""

        return "\n".join(
            [problem_set.tex_statements() for problem_set in self.problem_sets]
        )

    def tex(self):
        """Retorna o conteúdo do tópico em LaTeX."""
        return self.content.tex + self.tex_statements() + self.tex_answers()

    @classmethod
    def pdf(cls, topic):
        """Cria o arquivo `pdf` do tópico."""
        tmp_dir = config.TMP_TOPICS_DIR.joinpath(topic.area, topic.id_)
        out_dir = config.OUT_DIR.joinpath(topic.area, topic.id_)
        out_path = out_dir.with_name(topic.id_).with_suffix(".pdf")

        if out_path.exists():
            if topic.date < out_path.stat().st_mtime:
                return out_path

        tex_doc = convert.LaTeXDocument(
            id_=topic.id_,
            title=topic.title,
            author=topic.author,
            affiliation=topic.affiliation,
            template="braun, twocolumn",
            contents=topic.tex(),
        )

        return tex_doc.pdf(tmp_dir, out_dir)

    @classmethod
    def parse_mdfile(cls, topic_path: str | Path, problem_db: ProblemSet):
        """Cria um `Topic` a partir de um arquivo `.md`."""
        if not isinstance(topic_path, Path):
            topic_path = Path(topic_path)

        # parse `.md`. with YAML metadata
        topic_file = frontmatter.load(topic_path)

        # informações básicas
        topic = {
            "id_": topic_path.stem,
            "path": topic_path.resolve(),
            "date": datetime.utcfromtimestamp(topic_path.stat().st_mtime),
            "area": topic_path.parents[1].stem,
        }

        # extrair os metadados do arquivo `.md`
        for attr in ["title", "author", "affiliation", "template"]:
            if attr in topic_file:
                topic[attr] = topic_file[attr]

        # extrair a lista de problemas
        if "problems" in topic_file:
            problem_sets = []
            for i, (title, problem_ids) in enumerate(topic_file["problems"].items()):
                problem_set_id = f"{topic['id_']}{i+1}"
                problem_sets.append(
                    problem_db.filter(problem_set_id, title, problem_ids)
                )
            topic["problem_sets"] = problem_sets

        # extrair o título das seções
        soup = convert.md2soup(topic_file.content)
        topic["sections"] = [h1.text for h1 in soup.find_all("h1")]

        # conteúdo
        topic["content"] = Text.parse_md(topic_file.content)

        return cls.parse_obj(topic)


class TopicSet(BaseModel):
    """Conjunto de tópicos.

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

    def __getitem__(self, key: str) -> Topic:
        return next(filter(lambda topic: topic.id_ == key, self), None)

    def update_topics(self, topic_paths: list[str | Path], problem_db: ProblemSet):
        """Atualiza os problemas do `ProblemSet`."""
        updated_topics = []

        for topic_path in topic_paths:
            topic_id = topic_path.stem

            topic = self[topic_id]

            if not topic:
                topic = Topic.parse_mdfile(topic_path, problem_db)
                logging.warning(f"Tópico {topic_id} atualizado.")

            elif topic.date.timestamp() < topic_path.stat().st_mtime:
                topic = Topic.parse_mdfile(topic_path, problem_db)
                logging.warning(f"Tópico {topic_id} atualizado.")

            updated_topics.append(topic)

        self.topics = updated_topics

    def pdf(self):
        """Cria o arquivo `pdf` para todos os tópicos."""
        with Pool() as pool:
            pdfs = list(pool.imap(Topic.pdf, self.topics))
        return pdfs

    @classmethod
    def parse_paths(cls, topic_paths: list[str | Path], problem_db: ProblemSet):
        """Cria um `TopicSet` com os endereços problemas fornecidos."""
        topics = []

        for topic_path in topic_paths:
            topics.append(Topic.parse_mdfile(topic_path, problem_db))

        return cls(date=datetime.now(), topics=sorted(topics, key=lambda topic: topic.id_))
