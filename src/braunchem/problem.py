"""Base de dados para problemas de química, Gabriel Braun, 2022

Esse módulo implementa uma classe para os problemas.
"""
import braunchem.utils.convert as convert
import braunchem.utils.latex as latex
from braunchem.utils.convert import Text
import braunchem.utils.config as config
from braunchem.quantities import Table, qtys
from braunchem.utils.autoprops import autoprops

import os
import shutil
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
            return latex.cmd("MiniBox", chr(65 + self.obj))

        if len(self.answer) == 1:
            return self.answer[0]

        return latex.enum("answers", self.answer)

    def tex(self):
        """Retorna o enunciado completo do problema em LaTeX."""
        contents = self.statement.tex + self.tex_choices() + self.tex_data()

        parameters = {
            "id": self.id_,
            "path": self.path.parent,
        }

        return latex.env("problem", contents, keys=parameters)

    @classmethod
    def parse_mdfile(cls, problem_path: str | Path):
        """Cria um `Problem` a partir de um arquivo `.md`."""
        if not isinstance(problem_path, Path):
            problem_path = Path(problem_path)

        # parse `.md`. with YAML metadata
        pfile = frontmatter.load(problem_path)

        problem = {
            "id_": problem_path.stem,
            "path": problem_path.resolve(),
            "date": datetime.utcfromtimestamp(problem_path.stat().st_mtime),
        }

        # dados termodinâmicos
        if "data" in pfile:
            problem["data"] = qtys(pfile["data"])

        # conteúdo
        soup = convert.md2soup(pfile.content)

        # resolução
        soup, solution = convert.soup_split(soup, "hr")

        # problema objetivo: normal
        choice_list = soup.find("ul", class_="task-list")
        if choice_list:
            choices = []
            for index, item in enumerate(choice_list.find_all("li")):
                choice = Text.parse_html(item)
                choices.append(choice)
                check_box = item.find("input").extract()
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
        proposition_list = soup.find("ol", class_="task-list")
        if proposition_list:
            true_props = []
            for index, item in enumerate(proposition_list.find_all("li")):
                check_box = item.find("input").extract()
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
                answer = [
                    Text.parse_html(list_item)
                    for list_item in answer_list.find_all("li")
                ]
                problem["answer"] = answer
                answer_list.decompose()
            problem["solution"] = Text.parse_html(solution.extract())
        problem["statement"] = Text.parse_html(soup)

        return cls.parse_obj(problem)


class ProblemSet(BaseModel):
    """Container para os problemas.

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

    def tex_statements(self) -> str:
        """Retorna o conjunto de problemas em LaTeX."""
        if not self.problems:
            return ""

        header = latex.section(self.title, level=0, numbered=False)
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

        date = max(problem.date for problem in self)

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

    @classmethod
    def parse_paths(cls, problem_paths: list[str] | list[Path]):
        """Cria um `ProblemSet` com os problemas fornecidos."""
        with Pool() as pool:
            problems = list(pool.imap(Problem.parse_mdfile, problem_paths))

        return cls(id_="root", title="ROOT", date=datetime.now(), problems=problems)


def get_problem_paths(problems_dir: str | Path) -> list[Path]:
    """Retorna os endereço dos arquivos `.md` dos problemas no diretório.

    Args:
        problems_dir (str | Path): Diretório com os problemas.

    Retorna:
        list[Path]: Lista com o endereço dos arquivos `.md` de problemas.
    """
    if not isinstance(problems_dir, Path):
        problems_dir = Path(problems_dir)

    problem_files = []

    for root, _, files in os.walk(problems_dir):
        for file in files:
            file_path = Path(root).joinpath(file)
            dir_ = Path(root).relative_to(problems_dir)

            # problemas
            if file_path.suffix == ".md":
                problem_files.append(file_path)
                continue

            image_dst_path = config.IMAGES_DIR.joinpath(dir_.parent).joinpath(
                file_path.name
            )

            # figuras
            if file_path.suffix in [".svg", ".png"]:
                # arquivo não existe na base de dados de imagens
                if not image_dst_path.exists():
                    os.makedirs(image_dst_path.parent, exist_ok=True)
                    shutil.copy(src=file_path, dst=image_dst_path)
                    logging.info(f"Arquivo {file_path} copiado para: {image_dst_path}")
                    pass
                # arquivo existente na base de dados
                elif file_path.stat().st_mtime > image_dst_path.stat().st_mtime:
                    shutil.copy(src=file_path, dst=image_dst_path)
                    logging.info(f"Arquivo {file_path} copiado para: {image_dst_path}")
                continue

            # figuras em LaTeX
            if file_path.suffix == ".tex":
                tex_image_dst_path = image_dst_path.with_suffix(".svg")
                tex_image_tmp_path = config.TMP_IMAGES_DIR.joinpath(dir_).joinpath(
                    file_path.name
                )

                print(tex_image_tmp_path)

                if not tex_image_dst_path.exists():
                    pass
                elif file_path.stat().st_mtime > tex_image_dst_path.stat().st_mtime:
                    print(image_dst_path)
                continue

            # elif path.suffix == ".tex":
            #     # figures
            #     convert.tikz2svg(
            #         path,
            #         tmp_path=f"temp/images/{dir_}/{path.stem}",
            #         out_path=f"data/images/{dir_}",
            #     )
            #     convert.copy_r(
            #         f"data/images/{dir_}/{path.stem}.svg",
            #         f"{path.parent}/{path.stem}.svg",
            #     )

    return problem_files
