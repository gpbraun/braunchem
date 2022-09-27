"""Base de dados para problemas de química, Gabriel Braun, 2022

Esse módulo implementa uma classe para os problemas.
"""
import braunchem.utils.convert as convert
import braunchem.utils.latex as latex
import braunchem.utils.config as config
from braunchem.utils.convert import Text
from braunchem.quantities import Table, qtys
from braunchem.utils.autoprops import autoprops

import logging
from datetime import datetime
from pathlib import Path
from multiprocessing import Pool

import frontmatter
from pydantic import BaseModel


class Problem(BaseModel):
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

        tex_choices = [
            latex.cmd("everymath", latex.cmd("displaystyle", end="")) + c.tex
            for c in self.choices
        ]

        # return latex.List("choices", tex_choices).display()
        return latex.enum("choices", tex_choices, auto_cols=True, sep_cmd="task")

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

    def write_texfile(self):
        """Cria o arquivo em LaTeX do problema."""
        tex_path = config.TMP_PROBLEMS_DIR.joinpath(self.id_, self.id_).with_suffix(
            ".tex"
        )
        if tex_path.exists():
            if self.date.timestamp() > tex_path.stat().st_mtime:
                tex_path.parent.mkdir(parents=True, exist_ok=True)
                tex_path.write_text(self.tex(), encoding="utf-8")
        else:
            tex_path.parent.mkdir(parents=True, exist_ok=True)
            tex_path.write_text(self.tex(), encoding="utf-8")

    @classmethod
    def parse_mdfile(cls, problem_path: str | Path):
        """Cria um `Problem` a partir de um arquivo `.md`."""
        if not isinstance(problem_path, Path):
            problem_path = Path(problem_path)

        # parse `.md`. with YAML metadata
        problem_file = frontmatter.load(problem_path)

        # informações básicas
        problem = {
            "id_": problem_path.stem,
            "path": problem_path.resolve(),
            "date": datetime.utcfromtimestamp(problem_path.stat().st_mtime),
        }

        # dados termodinâmicos
        if "data" in problem_file:
            problem["data"] = qtys(problem_file["data"])

        # conteúdo
        soup = convert.md2soup(problem_file.content)

        # resolução
        soup, solution = convert.soup_split(soup, "hr")

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


class ProblemSet(BaseModel):
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
        try:
            return [problem for problem in self if problem.id_ == key][0]
        except IndexError:
            raise KeyError

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

    def filter(self, problem_set_id: str, title: str, problem_ids: list[str]):
        """Cria um subconjunto da lista problemas.

        Args:
            problem_set_id (str): Identificador da lista de problemas.
            title (str): Título da lista de problemas.
            problem_ids (list[str]): Lista com os `id_` desejados.

        Retorna:
            ProblemSet: Subconjunto de dados com os `id_` selecionados.
        """
        problems = []
        for problem_id in problem_ids:
            try:
                problems.append(self[problem_id])
            except KeyError:
                logging.warning(f"O problema com ID {problem_id} não existe.")

        date = min(problem.date for problem in self)

        return ProblemSet(id_=problem_set_id, title=title, date=date, problems=problems)

    def get_updated_problem(self, problem_path: str | Path) -> Problem:
        """Retorna a versão mais recente de um problema no `ProblemSet`.

        Se a versão em `self` é mais recente, retorna essa versão.
        Em caso contrário, retorna a versão parseada em `problem_path`.

        Args:
            problems_path (str | Path): Endereço do problema.

        Retorna:
            Problem: Problema atualizado.
        """
        if not isinstance(problem_path, Path):
            problem_path = Path(problem_path)

        problem_id = problem_path.stem
        path_date = datetime.utcfromtimestamp(problem_path.stat().st_mtime)

        try:
            if self[problem_id].date < path_date:
                logging.warning(f"Problema {problem_id} atualizado.")
                problem = Problem.parse_mdfile(problem_path)
            else:
                problem = self[problem_id]
                problem.path = problem_path.resolve()
        except KeyError:
            problem = Problem.parse_mdfile(problem_path)

        return problem

    def update_problems(self, problem_paths: list[str] | list[Path]):
        """Atualiza os problemas do `ProblemSet`."""
        self.problems = list(map(self.get_updated_problem, problem_paths))

    def write_texfiles(self):
        """Cria os arquivos em LaTeX de todos os problemas."""
        for problem in self:
            problem.write_texfile()

    @classmethod
    def parse_paths(cls, problem_paths: list[str] | list[Path]):
        """Cria um `ProblemSet` com os problemas fornecidos."""
        with Pool() as pool:
            problems = list(pool.imap(Problem.parse_mdfile, problem_paths))

        return cls(id_="root", title="ROOT", date=datetime.now(), problems=problems)
