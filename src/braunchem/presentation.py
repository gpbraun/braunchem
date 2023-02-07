"""Base de dados para problemas de química, Gabriel Braun, 2022

Esse módulo implementa uma classe para os tópicos.
"""
import logging
from datetime import datetime
from multiprocessing import Pool
from pathlib import Path

import frontmatter
from pydantic import BaseModel

import braunchem.utils.latex as latex
import braunchem.utils.text as text
from braunchem.latex.document import Document
from braunchem.problem import ProblemSet
from braunchem.utils.text import Text

logger = logging.getLogger(__name__)


class Presentation(BaseModel):
    """Apresentação.

    Atributos:
        id_ (str): Identificador único.
        path (Path): Endereço do arquivo `.md` do tópico
        title (str): Título do tópico.
        author (str): Autor da teoria.
        content (Text): Conteúdo teórico.
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

    def tex(self, problem_db: ProblemSet):
        """Retorna o conteúdo do tópico em LaTeX."""
        return self.content.tex

    def tex_document(self, problem_db: ProblemSet):
        """Cria o arquivo `pdf` do tópico."""
        return Document(
            id_=self.id_,
            path=self.path.parent,
            title=self.title,
            author=self.author,
            affiliation=self.affiliation,
            template="braun, twocolumn=true",
            toc=True,
            contents=self.tex(problem_db),
        )

    def write_pdf(self, problem_db: ProblemSet, tmp_dir: Path, out_dir: Path):
        """Cria o arquivo `.pdf` do tópico."""
        self.tex_document(problem_db).write_pdf(tmp_dir.joinpath(self.id_), out_dir)

    @classmethod
    def parse_mdfile(cls, topic_path: Path):
        """Cria um `Topic` a partir de um arquivo `.md`."""
        logger.info(f"Atualizando tópico em {topic_path}.")

        metadata, content = frontmatter.parse(topic_path.read_text())

        # informações básicas
        topic = {
            "id_": topic_path.stem,
            "path": topic_path.resolve(),
            "date": datetime.utcfromtimestamp(topic_path.stat().st_mtime),
        }

        # extrair os metadados do arquivo `.md`
        topic.update(metadata)

        # extrai as seções
        soup = text.md2soup(content)

        topic["sections"] = [
            Section.parse_obj(
                {
                    "id_": f"{topic_path.stem}{index:02d}",
                    "title": title,
                    "content": content,
                }
            )
            for index, (title, content) in enumerate(
                text.soup_split_header(soup), start=1
            )
        ]

        # conteúdo
        topic["content"] = Text.parse_md(content)

        return cls.parse_obj(topic)


class TopicSet(BaseModel):
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

    def filter(self, topic_set_id: str, title: str, topic_ids: list[str]):
        """Cria um subconjunto da lista problemas.

        Args:
            topic_set_id (str): Identificador da lista de tópicos.
            title (str): Título da lista de problemas.
            problem_ids (list[str]): Lista com os `id_` desejados.

        Retorna:
            ProblemSet: Subconjunto de dados com os `id_` selecionados.
        """
        if not topic_ids:
            return None

        topics = []
        for topic_id in topic_ids:
            try:
                topics.append(self[topic_id])
            except KeyError:
                logger.warning(f"O tópico com ID {topic_id} não existe.")

        date = min(topic.date for topic in self)

        return TopicSet(id_=topic_set_id, title=title, date=date, topics=topics)

    def update_topics(self, topic_paths: list[Path]):
        """Atualiza os problemas do `ProblemSet`."""
        updated_topics = []

        for topic_path in topic_paths:
            topic_id = topic_path.stem
            topic_date = datetime.utcfromtimestamp(topic_path.stat().st_mtime)

            topic = self[topic_id]

            if not topic:
                topic = Topic.parse_mdfile(topic_path)

            elif topic.date < topic_date:
                topic = Topic.parse_mdfile(topic_path)

            logger.debug(f"Tópico '{topic_id}' mantido.")
            updated_topics.append(topic)

        self.topics = updated_topics

    def tex_documents(self, problem_db: ProblemSet):
        return map(lambda topic: topic.tex_document(problem_db), self.topics)

    def write_pdfs(self, problem_db: ProblemSet, tmp_dir, out_dir):
        """Cria o arquivo `pdf` para todos os tópicos."""
        for topic in self.topics:
            topic.write_pdf(problem_db, tmp_dir, out_dir)

    @classmethod
    def parse_paths(cls, topic_paths: list[Path]):
        """Cria um `TopicSet` com os endereços de tópicos fornecidos."""
        with Pool() as pool:
            topics = list(pool.imap_unordered(Topic.parse_mdfile, topic_paths))

        return cls(id_="root", title="ROOT", date=datetime.now(), topics=topics)

    # @classmethod
    # def parse_database(cls, topics_dir: Path, force_update: bool = False):
    #     """Atualiza a base de dados"""
    #     topic_json_path = topics_dir.joinpath("topics.json")

    #     topic_paths = text.get_database_paths(topics_dir)

    #     if not topic_json_path.exists() or force_update:
    #         topic_db = cls.parse_paths(topic_paths)
    #         topic_json_path.write_text(
    #             topic_db.json(indent=2, ensure_ascii=False), encoding="utf-8"
    #         )
    #         return topic_db

    #     logger.info(f"Lendo base de dados no arquivo: {topic_json_path}.")

    #     topic_db = cls.parse_file(topic_json_path)
    #     topic_db.update_topics(topic_paths)

    #     topic_json_path.write_text(
    #         topic_db.json(indent=2, ensure_ascii=False), encoding="utf-8"
    #     )

    #     return topic_db


def main():
    return


if __name__ == "__main__":
    main()
