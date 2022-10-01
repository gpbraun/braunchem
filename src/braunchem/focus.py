"""Base de dados para problemas de química, Gabriel Braun, 2022

Esse módulo implementa uma classe para as áreas da química,
"""
import braunchem.utils.text as text
from braunchem.topic import TopicSet
from braunchem.utils.text import Text

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
    topic_sets: list[TopicSet] | None = None

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
        topic_set_list = metadata.pop("topics", None)
        if topic_set_list:
            topic_sets = []
            for i, (title, topic_ids) in enumerate(topic_set_list.items()):
                topic_set_id = focus["id_"] + str(i + 1)
                topic_sets.append(topic_db.filter(topic_set_id, title, topic_ids))
            focus["topic_sets"] = topic_sets

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
