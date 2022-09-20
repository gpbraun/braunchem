"""Base de dados para problemas de química, Gabriel Braun, 2022

Esse módulo implementa uma classe para os problemas.
"""
import braunchem.utils.convert2 as convert
import braunchem.utils.latex2 as latex
from braunchem.quantities import Table, QUANTITIES

import os
import logging
from datetime import datetime
from pathlib import Path, PosixPath
from multiprocessing import Pool

from tqdm import tqdm
from pydantic import BaseModel
from frontmatter import load


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
        """Cria um `Text` a partir de uma string em latex."""
        md_str = convert.html2md(html_str)
        tex_str = convert.html2tex(html_str)
        # Não sei o que é melhor, coverter de markdown ou de html para latex. Acho que tanto faz. Obs: converter de HTML para latex adiciona uns "{" e "}" a mais que podem ser úteis
        return cls(md=md_str, tex=tex_str)


class Problem(BaseModel):
    """Problema.

    Atributos:
        id_ (str): Identificador único.
        path (PosixPath): Diretório do problema.
        date (datetime): Data da última modificação do problema.
        statement (Text): Enunciado.
        solution (Text): Gabarito comentado.
        answer (list[Text]): Respostas.
        data (Table): Dados termodinâmicos.
        choices (list[Text]): Alternativas (problemas objetivos).
        correct_choice (int): Índice da alternativa correta.
    """

    id_: str
    path: PosixPath
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
    def parse_file(cls, problem_path: str):
        """Cria um `Problem` a partir de um arquivo `.md`."""
        path = Path(problem_path)

        pfile = load(path)

        p = {
            "id_": path.stem,
            "path": path.resolve(),
            "date": datetime.utcfromtimestamp(path.stat().st_mtime),
        }

        soup = convert.md2soup(pfile.content)

        # dados termodinâmicos
        if "dados" in pfile:
            p["data"] = QUANTITIES.filter(pfile["dados"])

        # solução
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
                    p["correct_choice"] = index
                    p["answer"] = [choice]
            p["choices"] = choices
            choice_list.decompose()
            if solution:
                p["solution"] = Text.parse_html(solution.extract())
            p["statement"] = Text.parse_html(soup)
            return cls.parse_obj(p)

        # problema objetivo: V ou F
        prop_list = soup.find("ol", class_="task-list")
        if prop_list:
            true_props = []
            for index, item in enumerate(prop_list.find_all("li")):
                check_box = item.find("input").extract()
                if check_box.has_attr("checked"):
                    true_props.append(index)
            if solution:
                p["solution"] = Text.parse_html(solution.extract())
            p["statement"] = Text.parse_html(soup)
            return cls.parse_obj(p)

        # problema discursivo
        if solution:
            answer_list = solution.find("ul")
            if answer_list:
                answer = [Text.parse_html(i) for i in answer_list.find_all("li")]
                p["answer"] = answer
                answer_list.decompose()
            p["solution"] = Text.parse_html(solution.extract())
        p["statement"] = Text.parse_html(soup)
        return cls.parse_obj(p)


def get_problem_paths(problem_db_path: str):
    # get the path of all problems and topics

    problem_files = []

    for root, _, files in os.walk(problem_db_path):
        for f in files:
            path = Path(os.path.join(root, f))
            dir_ = Path(root).relative_to(problem_db_path).parent

            # problems
            if path.suffix == ".md":
                # problem = Problem.parse_file(path)
                problem_files.append(path)

            elif path.suffix in [".svg", ".png"]:
                # figure
                convert.copy_r(path, f"data/images/{dir_}/{path.name}")

            # elif path.suffix == ".tex":
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


class ProblemSet(BaseModel):
    """Container para os problemas.

    Atributos:
        date (datetime): Data da última modificação do problema.
        problems (list[Problems]): Problemas.
    """

    date: datetime
    problems: list[Problem] | None = None

    def __len__(self):
        return len(self.problems)

    def __iter__(self):
        return iter(self.problems)

    def __getitem__(self, key: str):
        try:
            return [p for p in self if p.id_ == key][0]
        except IndexError:
            raise KeyError

    def update_problems(self, paths: list[str]):
        """Atualiza os problemas do `ProblemSet`."""
        updated_problems = []

        for path in paths:
            p_id_ = path.stem
            path_date = datetime.utcfromtimestamp(path.stat().st_mtime)

            try:
                if self[p_id_].date < path_date:
                    logging.warning(f"Problema {p_id_} atualizado.")
                    updated_problems.append(Problem.parse_file(path))
                else:
                    updated_problems.append(self[p_id_])
            except KeyError:
                updated_problems.append(Problem.parse_file(path))

        self.problems = updated_problems

    @classmethod
    def parse_paths(cls, paths: str):
        """Cria um `ProblemSet` com os problemas fornecidos."""
        with Pool() as pool:
            problems = list(
                tqdm(pool.imap(Problem.parse_file, paths, 5), total=len(paths))
            )

        return cls(date=datetime.now(), problems=problems)


PROBLEMS = ProblemSet.parse_file("data/problems/problems.json")
"""Base de dados de problemas."""


def main():
    logging.basicConfig(level=logging.DEBUG)

    paths = get_problem_paths("data/problems")

    PROBLEMS.update_problems(paths)
    # PROBLEMS = ProblemSet.parse_paths(paths)

    with open("data/problems/problems.json", "w") as json_file:
        json_file.write(PROBLEMS.json(indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()


def autoprops(true_props):
    """Cria as alternativas para problemas de V ou F."""
    if not true_props:
        choices = [
            "**N**" "**1**",
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
