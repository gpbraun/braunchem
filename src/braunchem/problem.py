"""Base de dados para problemas de química, Gabriel Braun, 2022

Esse módulo implementa uma classe para os problemas.
"""
import braunchem.utils.convert as convert
import braunchem.utils.latex as latex
from braunchem.quantities import Table, qtys

import os
import logging
import importlib.resources
from datetime import datetime
from pathlib import Path
from multiprocessing import Pool

import frontmatter
from tqdm import tqdm
from pydantic import BaseModel


DB_PATH = importlib.resources.files("braunchem.data")
"""Diretório da base de dados."""


class Text(BaseModel):
    """Texto para diagramação.

    Atributos:
        md (str): Texto em markdown.
        tex (str): Texto em latex.
    """

    md: str
    tex: str

    @classmethod
    def parse_md(cls, md_str: str):
        """Cria um `Text` a partir de uma string em markdown."""
        tex_str = convert.md2tex(md_str)
        return cls(md=md_str, tex=tex_str)

    @classmethod
    def parse_html(cls, html_str: str):
        """Cria um `Text` a partir de uma string em LaTeX."""
        md_str = convert.html2md(html_str)
        tex_str = convert.html2tex(html_str)
        # Não sei o que é melhor, coverter de markdown ou de HTML para LaTeX. Acho que tanto faz.
        # Obs: converter de HTML para latex adiciona uns "{" e "}" a mais que podem ser úteis
        return cls(md=md_str, tex=tex_str)


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
        if not self.choices:
            return False
        return True

    def tex_data(self):
        """Retorna os dados do problema formatados em latex."""
        if not self.data:
            return

        header = latex.section("Dados", level=2, numbered=False)
        data = self.data.equation_list()

        return header + latex.cmd("small") + data

    def tex_choices(self):
        """Retorna as alternativas do problema formatadas em latex."""
        if not self.is_objective:
            return

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
        """Retorna o enunciado completo do problema formatado em latex."""
        contents = self.statement.tex + self.tex_choices() + self.tex_data()

        parameters = {
            "id": self.id_,
            "path": self.path.parent,
        }

        return latex.env("problem", contents, keys=parameters)

    @classmethod
    def parse_mdfile(cls, problem_path: str | Path):
        """Cria um `Problem` a partir de um arquivo `.md`."""
        if isinstance(problem_path, str):
            path = Path(problem_path)
        else:
            path = problem_path

        # parse `.md`. with YAML metadata
        pfile = frontmatter.load(path)

        attrs = {
            "id_": path.stem,
            "path": path.resolve(),
            "date": datetime.utcfromtimestamp(path.stat().st_mtime),
        }

        # dados termodinâmicos
        if "data" in pfile:
            attrs["data"] = qtys(pfile["data"])

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
                    attrs["correct_choice"] = index
                    attrs["answer"] = [choice]
            attrs["choices"] = choices
            choice_list.decompose()
            if solution:
                attrs["solution"] = Text.parse_html(solution.extract())
            attrs["statement"] = Text.parse_html(soup)

            return cls.parse_obj(attrs)

        # problema objetivo: V ou F
        prop_list = soup.find("ol", class_="task-list")
        if prop_list:
            true_props = []
            for index, item in enumerate(prop_list.find_all("li")):
                check_box = item.find("input").extract()
                if check_box.has_attr("checked"):
                    true_props.append(index)
            if solution:
                attrs["solution"] = Text.parse_html(solution.extract())
            attrs["statement"] = Text.parse_html(soup)

            return cls.parse_obj(attrs)

        # problema discursivo
        if solution:
            answer_list = solution.find("ul")
            if answer_list:
                answer = [Text.parse_html(i) for i in answer_list.find_all("li")]
                attrs["answer"] = answer
                answer_list.decompose()
            attrs["solution"] = Text.parse_html(solution.extract())
        attrs["statement"] = Text.parse_html(soup)

        return cls.parse_obj(attrs)


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

    def __getitem__(self, key: str):
        try:
            return [problem for problem in self if problem.id_ == key][0]
        except IndexError:
            raise KeyError

    def filter(self, id_: str, title: str, p_ids: list):
        """Cria um subconjunto da lista problemas.

        Args:
            id_ (str): Identificador da lista de problemas.
            title (str): Título da lista de problemas.
            p_ids (list[str]): Lista com os `id_` desejados.

        Retorna:
            ProblemSet: Subconjunto de dados com os `id_` selecionados.
        """
        problems = []
        for p_id_ in p_ids:
            try:
                problems.append(self[p_id_])
            except KeyError:
                logging.warning(f"O problema com ID {p_id_} não existe.")

        date = max(p.date for p in self)

        return ProblemSet(id_=id_, title=title, date=date, problems=problems)

    def update_problems(self, problem_paths: list[str] | list[Path]):
        """Atualiza os problemas do `ProblemSet`."""
        updated_problems = []

        for path in problem_paths:
            p_id_ = path.stem
            path_date = datetime.utcfromtimestamp(path.stat().st_mtime)

            try:
                if self[p_id_].date < path_date:
                    logging.warning(f"Problema {p_id_} atualizado.")
                    updated_problems.append(Problem.parse_mdfile(path))
                else:
                    updated_problems.append(self[p_id_])
            except KeyError:
                updated_problems.append(Problem.parse_mdfile(path))

        self.problems = updated_problems

    @classmethod
    def parse_paths(cls, problem_paths: str):
        """Cria um `ProblemSet` com os problemas fornecidos."""
        with Pool() as pool:
            problems = list(
                tqdm(
                    pool.imap(Problem.parse_mdfile, problem_paths, 5),
                    total=len(problem_paths),
                )
            )

        return cls(id_="main", title="Main", date=datetime.now(), problems=problems)


def get_problem_paths(problem_db_path: str):
    """Retorna os endereço dos arquivos `.md` de problemas."""
    problem_files = []

    for root, _, files in os.walk(problem_db_path):
        for f in files:
            path = Path(os.path.join(root, f))
            dir_ = Path(root).relative_to(problem_db_path).parent

            # problemas
            if path.suffix == ".md":
                problem_files.append(path)

            # figuras
            elif path.suffix in [".svg", ".png"]:
                convert.copy_r(path, f"data/images/{dir_}/{path.name}")

            # elif path.suffix == ".tex":os.walk(topic_path)
            #     # tikz figures
            #     dir_ = Path(root).relative_to(problem_path).parent
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


PROBLEMS_DB_PATH = DB_PATH.joinpath("problems.json")
"""Endereço da base de dados de problemas."""

PROBLEMS = ProblemSet.parse_file(PROBLEMS_DB_PATH)
"""Base de dados de problemas."""


def problem(p_id: str) -> Problem:
    """Retorna um problema da base de dados."""
    return PROBLEMS[p_id]


def pset(id_: str, title: str, p_ids: list[str]) -> ProblemSet:
    """Retorna um conjunto de dados termodiâmicos da base de dados."""
    return PROBLEMS.filter(id_=id_, title=title, p_ids=p_ids)


def main():
    logging.basicConfig(level=logging.DEBUG)

    paths = get_problem_paths("data/problems")

    PROBLEMS.update_problems(paths)
    # PROBLEMS = ProblemSet.parse_paths(paths)

    with open(PROBLEMS_DB_PATH, "w", encoding="utf-8") as json_file:
        json_file.write(PROBLEMS.json(indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()


def autoprops(true_props):
    """Cria as alternativas para problemas de V ou F."""
    if not true_props:
        choices = [
            "**N**",
            "**1**",
            "**2**",
            "**3**",
            "**4**",
        ]
        correct_choice = 0
    # Uma correta
    if true_props == [0]:
        choices = [
            "**1**",
            "**2**",
            "**1** e **2**",
            "**1** e **3**",
            "**1** e **4**",
        ]
        correct_choice = 0
    if true_props == [1]:
        choices = ["**1**", "**2**", "**1** e **2**", "**2** e **3**", "**2** e **4**"]
        correct_choice = 1
    if true_props == [2]:
        choices = ["**2**", "**3**", "**1** e **3**", "**2** e **3**", "**3** e **4**"]
        correct_choice = 1
    if true_props == [3]:
        choices = ["**3**", "**4**", "**1** e **4**", "**2** e **4**", "**3** e **4**"]
        correct_choice = 1
    # Duas corretas
    if true_props == [0, 1]:
        choices = [
            "**1**",
            "**2**",
            "**1** e **2**",
            "**1**, **2** e **3**",
            "**1**, **2** e **4**",
        ]
        correct_choice = 2
    if true_props == [0, 2]:
        choices = [
            "**1**",
            "**3**",
            "**1** e **3**",
            "**1**, **2** e **3**",
            "**1**, **3** e **4**",
        ]
        correct_choice = 2
    if true_props == [0, 3]:
        choices = [
            "**1**",
            "**4**",
            "**1** e **4**",
            "**1**, **2** e **4**",
            "**1**, **3** e **4**",
        ]
        correct_choice = 2
    if true_props == [1, 2]:
        choices = [
            "**2**",
            "**3**",
            "**2** e **3**",
            "**1**, **2** e **3**",
            "**2**, **3** e **4**",
        ]
        correct_choice = 2
    if true_props == [1, 3]:
        choices = [
            "**2**",
            "**4**",
            "**2** e **4**",
            "**1**, **2** e **4**",
            "**2**, **3** e **4**",
        ]
        correct_choice = 2
    if true_props == [2, 3]:
        choices = [
            "**3**",
            "**4**",
            "**3** e **4**",
            "**1**, **3** e **4**",
            "**2**, **3** e **4**",
        ]
        correct_choice = 2
    # Três corretas
    if true_props == [0, 1, 2]:
        choices = [
            "**1** e **2**",
            "**1** e **3**",
            "**2** e **3**",
            "**1**, **2** e **3**",
            "**1**, **2**, **3** e **4**",
        ]
        correct_choice = 3
    if true_props == [0, 1, 3]:
        choices = [
            "**1** e **2**",
            "**1** e **4**",
            "**2** e **4**",
            "**1**, **2** e **4**",
            "**1**, **2**, **3** e **4**",
        ]
        correct_choice = 3
    if true_props == [0, 2, 3]:
        choices = [
            "**1** e **3**",
            "**1** e **4**",
            "**3** e **4**",
            "**1**, **3** e **4**",
            "**1**, **2**, **3** e **4**",
        ]
        correct_choice = 3
    if true_props == [1, 2, 3]:
        choices = [
            "**2** e **3**",
            "**2** e **4**",
            "**3** e **4**",
            "**2**, **3** e **4**",
            "**1**, **2**, **3** e **4**",
        ]
        correct_choice = 3
    # Todas corretas
    if true_props == [0, 1, 2, 3]:
        choices = [
            "**1**, **2** e **3**",
            "**1**, **2** e **4**",
            "**1**, **3** e **4**",
            "**2**, **3** e **4**",
            "**1**, **2**, **3** e **4**",
        ]
        correct_choice = 4
    answer = [choices[correct_choice]]
    return choices, answer, correct_choice
