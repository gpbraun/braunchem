"""Base de dados para problemas de química, Gabriel Braun, 2022

Esse módulo implementa uma classe para os tópicos.
"""
import braunchem.utils.convert as convert
import braunchem.utils.latex as latex
from braunchem.utils.convert import Text
from braunchem.problem import ProblemSet

import logging
from datetime import datetime
from pathlib import Path

import frontmatter
import pydantic


class Topic(pydantic.BaseModel):
    """Tópico.

    Atributos:
        id_ (str): Identificador único.
        title (str): Título do tópico.
        author (str): Autor da teoria.
        content (str): Conteúdo teórico.
        sections (list[str]): Títulos das seções.
        problem_sets (list[ProblemSet]): Listas de problemas.
    """

    id_: str
    path: Path
    date: datetime
    title: str
    author: str = "Gabriel Braun"
    affiliation: str = "Colégio e Curso Pensi, Coordenação de Química"
    content: Text
    sections: list[str]
    problem_sets: list[ProblemSet] | None = None

    def tex_answers(self):
        """Retorna o gabarito dos problemas do tópico em LaTeX."""
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

    def write_pdf(self, tmp_dir: Path, out_dir: Path):
        """Cria o arquivo `pdf` do tópico."""
        out_path = out_dir.with_name(self.id_).with_suffix(".pdf")

        if out_path.exists():
            if self.date < out_path.stat().st_mtime:
                return out_path

        tex_doc = convert.Document(
            id_=self.id_,
            title=self.title,
            author=self.author,
            affiliation=self.affiliation,
            template="braun, twocolumn",
            contents=self.tex(),
        )

        tex_doc.pdf(tmp_dir, out_dir)

    def update_problems(self, problem_db: ProblemSet):
        """Atualiza os problemas em um tópico."""
        if not self.problem_sets:
            return

        for problem_set in self.problem_sets:
            problem_set.update(problem_db)

    @classmethod
    def parse_mdfile(cls, topic_path: Path, problem_db: ProblemSet):
        """Cria um `Topic` a partir de um arquivo `.md`."""
        logging.info(f"Tópico {topic_path} atualizado.")

        metadata, content = frontmatter.parse(topic_path.read_text())

        # informações básicas
        topic = {
            "id_": topic_path.stem,
            "path": topic_path.resolve(),
            "date": datetime.utcfromtimestamp(topic_path.stat().st_mtime),
        }

        # extrair a lista de problemas
        problem_set_list = metadata.pop("problems", None)
        if problem_set_list:
            problem_sets = []
            for i, (title, problem_ids) in enumerate(problem_set_list.items()):
                problem_set_id = topic["id_"] + str(i + 1)
                problem_sets.append(
                    problem_db.filter(problem_set_id, title, problem_ids)
                )
            topic["problem_sets"] = problem_sets

        # extrair os metadados do arquivo `.md`
        topic.update(metadata)

        # extrair o título das seções
        soup = convert.md2soup(content)
        topic["sections"] = [h1.text for h1 in soup.find_all("h1")]

        # conteúdo
        topic["content"] = Text.parse_md(content)

        return cls.parse_obj(topic)


class TopicSet(pydantic.BaseModel):
    """Conjunto de tópicos.

    Atributos:
        date (datetime): Data.
        topics (list[Topic]): Conjuntos de tópicos.
    """

    id_: str
    date: datetime
    title: str
    topics: list[Topic]

    def __len__(self):
        return len(self.topics)

    def __iter__(self):
        return iter(self.topics)

    def __getitem__(self, key: str) -> Topic:
        return next(filter(lambda topic: topic.id_ == key, self), None)

    def update_topics(self, topic_paths: list[Path], problem_db: ProblemSet):
        """Atualiza os problemas do `ProblemSet`."""
        updated_topics = []

        for topic_path in topic_paths:
            topic_id = topic_path.stem
            topic_date = datetime.utcfromtimestamp(topic_path.stat().st_mtime)

            topic = self[topic_id]

            if not topic:
                topic = Topic.parse_mdfile(topic_path, problem_db)

            elif topic.date < topic_date:
                topic = Topic.parse_mdfile(topic_path, problem_db)

            logging.debug(f"Tópico {topic_id} mantido.")
            topic.update_problems(problem_db)
            updated_topics.append(topic)

        self.topics = updated_topics

    def write_pdfs(self, out_dir: Path, tmp_dir: Path):
        """Cria o arquivo `pdf` para todos os tópicos."""
        map(lambda topic: topic.write_pdf(tmp_dir, out_dir), self.topics)

    @classmethod
    def parse_paths(cls, topic_paths: list[Path], problem_db: ProblemSet):
        """Cria um `TopicSet` com os endereços problemas fornecidos."""
        path_parser = lambda topic_path: Topic.parse_mdfile(topic_path, problem_db)
        topics = list(map(path_parser, topic_paths))

        return cls(id_="root", title="ROOT", date=datetime.now(), topics=topics)

    @classmethod
    def parse_database(
        cls, topics_dir: Path, problem_db: ProblemSet, force_update: bool = False
    ):
        """Atualiza a base de dados"""
        topic_json_path = topics_dir.joinpath("topics.json")
        topic_paths = convert.get_database_paths(topics_dir)

        if not topic_json_path.exists() or force_update:
            topic_db = cls.parse_paths(topic_paths, problem_db=problem_db)
            topic_json_path.write_text(
                topic_db.json(indent=2, ensure_ascii=False), encoding="utf-8"
            )
            return topic_db

        topic_db = cls.parse_file(topic_json_path)
        topic_db.update_topics(topic_paths, problem_db=problem_db)

        topic_json_path.write_text(
            topic_db.json(indent=2, ensure_ascii=False), encoding="utf-8"
        )

        return topic_db
