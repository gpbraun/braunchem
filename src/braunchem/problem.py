"""Base de dados para problemas de química, Gabriel Braun, 2022

Esse módulo implementa uma classe para os problemas.
"""
from turtle import update
import braunchem.utils.text as text
import braunchem.utils.latex as latex
from braunchem.utils.text import Text
from braunchem.quantities import Table, qtys
from braunchem.utils.autoprops import autoprops

import logging
from datetime import datetime
from pathlib import Path
from multiprocessing import Pool

import frontmatter
import pydantic

logger = logging.getLogger(__name__)


class Problem(pydantic.BaseModel):
    """Problema.

    Atributos:
        id_ (str): Identificador único.
        path (Path): Diretório do problema.
        date (datetime): Data da última modificação do problema.
        statement (Text): Enunciado.
        solution (Text): Gabarito comentado.
        answer (list[Text]): Respostas.
        data (Table): Dados termodinâmicos.
        choices (list[Text]): Alternativas (problemas objetivos).
        correct_choice (int): Índice da alternativa correta.
    """

    id_: str
    path: Path
    date: datetime
    statement: Text
    solution: Text | None = None
    answer: list[Text] | None = None
    data: Table | None = None
    choices: list[Text] | None = None
    correct_choice: int | None = None

    @property
    def is_objective(self):
        """Verifica se o problema é objetivo."""
        return True if self.choices else False

    def tex_data(self):
        """Retorna os dados do problema formatados em latex."""
        if not self.data:
            return ""

        header = latex.section("Dados", level=2, numbered=False)
        data = self.data.equation_list()

        return header + latex.cmd("small") + data

    def tex_choices(self):
        """Retorna as alternativas do problema formatadas em latex."""
        if not self.is_objective:
            return ""

        tex_choices = [c.tex for c in self.choices]

        return latex.enum("choices", tex_choices, sep_cmd="item")

    def tex_answer(self):
        """Retorna as respostas do problema formatados em latex."""
        if not self.answer:
            return "-"

        if self.is_objective:
            return latex.cmd("MiniBox", chr(65 + self.correct_choice))

        if len(self.answer) == 1:
            return self.answer[0].tex

        return latex.enum("answers", [answer.tex for answer in self.answer])

    def tex(self):
        """Retorna o enunciado completo do problema em LaTeX."""
        contents = self.statement.tex + self.tex_choices() + self.tex_data()

        parameters = {
            "id": self.id_,
            "path": self.path.parent,
        }

        return latex.env("problem", contents, keys=parameters)

    @classmethod
    def parse_mdfile(cls, problem_path: Path):
        """Cria um `Problem` a partir de um arquivo `.md`."""
        logger.info(f"Atualizando problema em {problem_path}.")

        metadata, content = frontmatter.parse(problem_path.read_text())

        # informações básicas
        problem = {
            "id_": problem_path.stem,
            "path": problem_path.resolve(),
            "date": datetime.utcfromtimestamp(problem_path.stat().st_mtime),
        }

        # dados termodinâmicos
        data = metadata.pop("data", None)
        if data:
            problem["data"] = qtys(data)

        # conteúdo
        soup = text.md2soup(content)

        # resolução
        soup, solution = text.soup_split(soup, "hr")

        # problema objetivo: normal
        choice_list = soup.find("ul", {"class": "task-list"})
        if choice_list:
            choices = []
            for index, li in enumerate(choice_list.find_all("li")):
                choice = Text.parse_html(li)
                choices.append(choice)
                check_box = li.find("input").extract()
                if check_box.has_attr("checked"):
                    problem["correct_choice"] = index
                    problem["answer"] = [choice]
            problem["choices"] = choices
            choice_list.decompose()
            if solution:
                problem["solution"] = Text.parse_html(solution.extract())
            problem["statement"] = Text.parse_html(soup)

            return cls.parse_obj(problem)

        # problema objetivo: V ou F
        proposition_input = soup.find("input", {"type": "checkbox"})
        if proposition_input:
            proposition_list = proposition_input.parent.parent
            true_props = []
            for index, li in enumerate(proposition_list.find_all("li")):
                check_box = li.find("input").extract()
                if check_box.has_attr("checked"):
                    true_props.append(index)
            choices, answer, correct_choice = autoprops(true_props)
            problem["choices"] = choices
            problem["answer"] = answer
            problem["correct_choice"] = correct_choice
            if solution:
                problem["solution"] = Text.parse_html(solution.extract())
            problem["statement"] = Text.parse_html(soup)

            return cls.parse_obj(problem)

        # problema discursivo
        if solution:
            answer_list = solution.find("ul")
            if answer_list:
                answer = [Text.parse_html(li) for li in answer_list.find_all("li")]
                problem["answer"] = answer
                answer_list.decompose()
            problem["solution"] = Text.parse_html(solution.extract())
        problem["statement"] = Text.parse_html(soup)

        return cls.parse_obj(problem)


class ProblemSet(pydantic.BaseModel):
    """Conjunto de Problemas.

    Atributos:
        date (datetime): Data da última modificação do problema.
        problems (list[Problems]): Problemas.
    """

    id_: str
    title: str
    date: datetime
    problems: list[Problem] | None = None

    def __len__(self):
        return len(self.problems)

    def __iter__(self):
        return iter(self.problems)

    def __getitem__(self, key: str) -> Problem:
        return next(filter(lambda problem: problem.id_ == key, self), None)

    def filter(self, problem_set_id: str, title: str, problem_ids: list[str]):
        """Cria um subconjunto da lista problemas.

        Args:
            problem_set_id (str): Identificador da lista de problemas.
            title (str): Título da lista de problemas.
            problem_ids (list[str]): Lista com os `id_` desejados.

        Retorna:
            ProblemSet: Subconjunto de dados com os `id_` selecionados.
        """
        if not problem_ids:
            return None

        problems = []
        for problem_id in problem_ids:
            try:
                problems.append(self[problem_id])
            except KeyError:
                logger.warning(f"O problema com ID {problem_id} não existe.")

        date = min(problem.date for problem in self)

        return ProblemSet(id_=problem_set_id, title=title, date=date, problems=problems)

    @property
    def is_objective(self) -> bool:
        """Verifica se todos os problemas são objetivos."""
        return True if all(p.is_objective for p in self) else False

    def tex_statements(self, use_header: bool = True) -> str:
        """Retorna o conjunto de problemas em LaTeX."""
        if not self.problems:
            return ""

        header = latex.section(self.title, level=0) if use_header else ""
        statements = "\n".join(p.tex() for p in self)

        return header + statements

    def tex_answers(self) -> str:
        """Retorna o gabarito dos problemas em LaTeX."""
        if not self.problems:
            return ""

        header = latex.section(self.title, level=1, numbered=False)
        answers = [p.tex_answer() for p in self.problems]

        if self.is_objective:
            return header + latex.enum("checks", answers, cols=5)

        return header + latex.enum("answers", answers)

    def get_updated_problem(self, problem_path: Path) -> Problem:
        """Retorna a versão mais recente de um problema no `ProblemSet`.

        Se a versão em `self` é mais recente, retorna essa versão.
        Em caso contrário, retorna a versão parseada em `problem_path`.

        Args:
            problems_path (Path): Endereço do problema.

        Retorna:
            Problem: Problema atualizado.
        """
        problem_id = problem_path.stem
        problem_date = datetime.utcfromtimestamp(problem_path.stat().st_mtime)

        problem = self[problem_id]

        if not problem:
            return Problem.parse_mdfile(problem_path)

        if problem.date < problem_date:
            return Problem.parse_mdfile(problem_path)

        logger.debug(f"Problema {problem_id} mantido.")
        problem.path = problem_path.resolve()
        return problem

    def update_problems(self, problem_paths: list[Path]):
        """Atualiza os problemas do `ProblemSet`."""
        self.problems = list(map(self.get_updated_problem, problem_paths))

    def update(self, other):
        """Atualiza os problemas do `ProblemSet` com os problemas de outro `ProblemSet`"""
        updated_problems = []
        for problem in self.problems:
            updated_problem = other[problem.id_]
            if updated_problem:
                updated_problems.append(other[problem.id_])

        self.problems = updated_problems

    @classmethod
    def parse_paths(cls, problem_paths: list[Path]):
        """Cria um `ProblemSet` com os problemas fornecidos."""
        with Pool() as pool:
            problems = list(pool.imap_unordered(Problem.parse_mdfile, problem_paths))

        return cls(id_="root", title="ROOT", date=datetime.now(), problems=problems)

    @classmethod
    def parse_database(
        cls,
        problems_dir: Path,
        force_update: bool = False,
    ):
        """Atualiza a base de dados"""
        problem_json_path = problems_dir.joinpath("problems.json")
        logger.info(f"Procurando problemas no diretório: {problems_dir}.")
        problem_paths = text.get_database_paths(problems_dir)

        if not problem_json_path.exists() or force_update:
            problem_db = cls.parse_paths(problem_paths)
            problem_json_path.write_text(
                problem_db.json(indent=2, ensure_ascii=False), encoding="utf-8"
            )
            return problem_db

        problem_db = cls.parse_file(problem_json_path)
        problem_db.update_problems(problem_paths)

        problem_json_path.write_text(
            problem_db.json(indent=2, ensure_ascii=False), encoding="utf-8"
        )

        return problem_db
