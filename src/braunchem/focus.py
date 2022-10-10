"""Base de dados para problemas de química, Gabriel Braun, 2022

Esse módulo implementa uma classe para as áreas da química,
"""
import braunchem.utils.text as text
from braunchem.topic import TopicSet, Topic

import logging
from datetime import datetime
from pathlib import Path

import frontmatter
import pydantic

logger = logging.getLogger(__name__)


class Focus(pydantic.BaseModel):
    """Área (Química Inorgânica, Físico-Química, Química Analítica, Química Orgânica)"""

    id_: str
    path: Path
    date: datetime
    title: str
    content: str
    topics: list[Topic] = []

    @classmethod
    def parse_mdfile(cls, focus_path: Path, topic_db: TopicSet):
        """Cria um `Focus` a partir de um arquivo `.md`."""
        logger.info(f"Atualizando foco em {focus_path}.")

        metadata, content = frontmatter.parse(focus_path.read_text())

        # informações básicas
        focus = {
            "id_": focus_path.stem,
            "path": focus_path.resolve(),
            "date": datetime.utcfromtimestamp(focus_path.stat().st_mtime),
        }

        # extrair a lista de tópicos
        topic_ids = metadata.pop("topics", None)
        if topic_ids:
            topic_set = topic_db.filter(focus["id_"], focus["id_"], topic_ids)
            focus["topics"] = topic_set.topics

        # extrair os metadados do arquivo markdown
        focus.update(metadata)

        # conteúdo
        focus["content"] = content

        return cls.parse_obj(focus)


class FocusSet(pydantic.BaseModel):
    """Conjunto de areas"""

    id_: str
    date: datetime
    title: str
    focuses: list[Focus]

    @classmethod
    def parse_paths(cls, focus_paths: list[Path], topic_db: TopicSet):
        """Cria um `FocusSet` com os endereços dos fócos fornecidos."""
        path_parser = lambda focus_path: Focus.parse_mdfile(focus_path, topic_db)
        focuses = list(map(path_parser, focus_paths))

        return cls(id_="root", title="ROOT", date=datetime.now(), focuses=focuses)

    @classmethod
    def parse_database(cls, focus_dir: Path, topic_db: TopicSet):
        """Atualiza a base de dados"""
        focus_json_path = focus_dir.joinpath("focuses.json")
        logger.info(f"Procurando focos no diretório: {focus_dir}.")
        focus_paths = text.get_database_paths(focus_dir)

        focus_db = cls.parse_paths(focus_paths, topic_db=topic_db)
        focus_json_path.write_text(
            focus_db.json(indent=2, ensure_ascii=False), encoding="utf-8"
        )
        return focus_db
