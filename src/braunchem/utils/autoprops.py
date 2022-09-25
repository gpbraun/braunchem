"""Gabriel Braun, 2022

Esse módulo implementa funções para geração automática de alternativas.
"""
from braunchem.utils.convert import Text


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

    choices = [Text.parse_md(choice) for choice in choices]
    answer = [choices[correct_choice]]
    return choices, answer, correct_choice
