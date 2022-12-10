"""Base de dados para problemas de química, Gabriel Braun, 2022

Esse módulo implementa uma classe para as áreas da química,
"""
import braunchem.utils.text as text

import logging
from datetime import datetime
from pathlib import Path

import frontmatter
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class Focus(BaseModel):
    """Área (Química Inorgânica, Físico-Química, Química Analítica, Química Orgânica)"""

    id_: str
    path: Path
    title: str
    content: str
    topics: list[str] = []

    @classmethod
    def parse_mdfile(cls, focus_path: Path):
        """Cria um `Focus` a partir de um arquivo `.md`."""
        logger.info(f"Atualizando foco em {focus_path}.")

        metadata, content = frontmatter.parse(focus_path.read_text())

        # informações básicas
        focus = {
            "id_": focus_path.stem,
            "path": focus_path.resolve(),
            "date": datetime.utcfromtimestamp(focus_path.stat().st_mtime),
        }

        # extrair os metadados do arquivo markdown
        focus.update(metadata)

        # conteúdo
        focus["content"] = content

        return cls.parse_obj(focus)


class FocusSet(BaseModel):
    """Conjunto de areas"""

    id_: str
    title: str
    focuses: list[Focus]

    @classmethod
    def parse_paths(cls, focus_paths: list[Path]):
        """Cria um `FocusSet` com os endereços dos fócos fornecidos."""
        focuses = list(map(Focus.parse_mdfile, focus_paths))

        return cls(id_="root", title="ROOT", focuses=focuses)

    @classmethod
    def parse_database(cls, focus_dir: Path):
        """Atualiza a base de dados"""
        focus_json_path = focus_dir.joinpath("focuses.json")

        focus_paths = text.get_database_paths(focus_dir)

        focus_db = cls.parse_paths(focus_paths)
        focus_json_path.write_text(
            focus_db.json(indent=2, ensure_ascii=False), encoding="utf-8"
        )
        return focus_db
