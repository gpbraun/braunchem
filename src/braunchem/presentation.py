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
    """Apresentação."""

    id_: str
    path: Path
    date: datetime
    title: str
    author: str = "Gabriel Braun"
    affiliation: str = "Colégio e Curso Pensi, Coordenação de Química"
    content: Text
    problems: list = None

    def tex(self):
        """Retorna o conteúdo do tópico em LaTeX."""
        return self.content.tex

    def tex_problems(self, problem_db: ProblemSet):
        """Retorna os problemas do tópico em LaTeX."""
        if not self.problems:
            return ""

        problem_collection = problem_db.filter(self.id, self.title, self.problems)

        tex_statements = problem_collection.tex_statements()

        return tex_statements

    def tex_document(self):
        """Cria o arquivo `pdf` do tópico."""
        return Document(
            id_=self.id_,
            path=self.path.parent,
            title=self.title,
            author=self.author,
            affiliation=self.affiliation,
            classname="braunpres",
            toc=True,
            contents=self.tex(),
        )

    def write_pdf(self, tmp_dir: Path, out_dir: Path):
        """Cria o arquivo `.pdf` do tópico."""
        self.tex_document().write_pdf(tmp_dir.joinpath(self.id_), out_dir)

    @classmethod
    def parse_mdfile(cls, pres_path: Path):
        """Cria um `Topic` a partir de um arquivo `.md`."""
        logger.info(f"Atualizando apresentação em {pres_path:}.")

        metadata, content = frontmatter.parse(pres_path.read_text())

        # informações básicas
        presentation = {
            "id_": pres_path.stem,
            "path": pres_path.resolve(),
            "date": datetime.utcfromtimestamp(pres_path.stat().st_mtime),
        }

        # extrair os metadados do arquivo `.md`
        presentation.update(metadata)

        # conteúdo
        presentation["content"] = Text.parse_md_pres(content)

        return cls.parse_obj(presentation)


class PresentationSet(BaseModel):
    """Conjunto de apresentações."""

    id_: str
    date: datetime
    title: str
    presentations: list[Presentation]

    def __len__(self):
        return len(self.presentations)

    def __iter__(self):
        return iter(self.presentations)

    def __getitem__(self, key: str) -> Presentation:
        return next(filter(lambda pres: pres.id_ == key, self), None)

    def filter(self, pres_set_id: str, title: str, pres_ids: list[str]):
        if not pres_ids:
            return None

        presentations = []
        for pres_id in pres_ids:
            try:
                presentations.append(self[pres_id])
            except KeyError:
                logger.warning(f"O tópico com ID {pres_id} não existe.")

        date = min(pres.date for pres in self)

        return PresentationSet(
            id_=pres_set_id, title=title, date=date, presentations=presentations
        )

    def update_presentations(self, pres_paths: list[Path]):
        """Atualiza os problemas do `ProblemSet`."""
        updated_presentations = []

        for pres_path in pres_paths:
            pres_id = pres_path.stem
            pres_date = datetime.utcfromtimestamp(pres_path.stat().st_mtime)

            pres = self[pres_id]

            if not pres:
                pres = Presentation.parse_mdfile(pres_path)

            elif pres.date < pres_date:
                pres = Presentation.parse_mdfile(pres_path)

            logger.debug(f"Tópico '{pres_id}' mantido.")
            updated_presentations.append(pres)

        self.presentations = updated_presentations

    def tex_documents(self):
        return map(lambda pres: pres.tex_document(), self.presentations)

    def write_pdfs(self, tmp_dir, out_dir):
        """Cria o arquivo `pdf` para todos os tópicos."""
        for pres in self.presentations:
            pres.write_pdf(tmp_dir, out_dir)

    @classmethod
    def parse_paths(cls, pres_paths: list[Path]):
        """Cria um `TopicSet` com os endereços de tópicos fornecidos."""
        with Pool() as pool:
            presentations = list(
                pool.imap_unordered(Presentation.parse_mdfile, pres_paths)
            )

        return cls(
            id_="root", title="ROOT", date=datetime.now(), presentations=presentations
        )

    @classmethod
    def parse_database(cls, presentations_dir: Path, force_update: bool = False):
        """Atualiza a base de dados"""
        pres_json_path = presentations_dir.joinpath("presentations.json")

        pres_paths = text.get_database_paths(presentations_dir)

        if not pres_json_path.exists() or force_update:
            pres_db = cls.parse_paths(pres_paths)
            pres_json_path.write_text(
                pres_db.json(indent=2, ensure_ascii=False), encoding="utf-8"
            )
            return pres_db

        logger.info(f"Lendo base de dados no arquivo: {pres_json_path}.")

        pres_db = cls.parse_file(pres_json_path)
        pres_db.update_presentations(pres_paths)

        pres_json_path.write_text(
            pres_db.json(indent=2, ensure_ascii=False), encoding="utf-8"
        )

        return pres_db


def main():
    pres = Presentation.parse_mdfile(Path("data/presentations/Q2/2A/S2A.md"))
    problem_db = ProblemSet.parse_database("./data/problems", force_update=False)

    pres.write_pdf(problem_db, tmp_dir=Path("test"), out_dir=Path("test"))
    return


if __name__ == "__main__":
    main()
