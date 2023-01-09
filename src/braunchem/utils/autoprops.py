"""Gabriel Braun, 2022

Esse módulo implementa funções para geração automática de alternativas.
"""
from braunchem.utils.text import Text


def autoprops(true_props):
    """Cria as alternativas para problemas de V ou F."""
    if not true_props:
        choices = [
            "<strong>N</strong>",
            "<strong>1</strong>",
            "<strong>2</strong>",
            "<strong>3</strong>",
            "<strong>4</strong>",
        ]
        correct_choice = 0
    # Uma correta
    if true_props == [0]:
        choices = [
            "<strong>1</strong>",
            "<strong>2</strong>",
            "<strong>1</strong> e <strong>2</strong>",
            "<strong>1</strong> e <strong>3</strong>",
            "<strong>1</strong> e <strong>4</strong>",
        ]
        correct_choice = 0
    if true_props == [1]:
        choices = [
            "<strong>1</strong>",
            "<strong>2</strong>",
            "<strong>1</strong> e <strong>2</strong>",
            "<strong>2</strong> e <strong>3</strong>",
            "<strong>2</strong> e <strong>4</strong>",
        ]
        correct_choice = 1
    if true_props == [2]:
        choices = [
            "<strong>2</strong>",
            "<strong>3</strong>",
            "<strong>1</strong> e <strong>3</strong>",
            "<strong>2</strong> e <strong>3</strong>",
            "<strong>3</strong> e <strong>4</strong>",
        ]
        correct_choice = 1
    if true_props == [3]:
        choices = [
            "<strong>3</strong>",
            "<strong>4</strong>",
            "<strong>1</strong> e <strong>4</strong>",
            "<strong>2</strong> e <strong>4</strong>",
            "<strong>3</strong> e <strong>4</strong>",
        ]
        correct_choice = 1
    # Duas corretas
    if true_props == [0, 1]:
        choices = [
            "<strong>1</strong>",
            "<strong>2</strong>",
            "<strong>1</strong> e <strong>2</strong>",
            "<strong>1</strong>, <strong>2</strong> e <strong>3</strong>",
            "<strong>1</strong>, <strong>2</strong> e <strong>4</strong>",
        ]
        correct_choice = 2
    if true_props == [0, 2]:
        choices = [
            "<strong>1</strong>",
            "<strong>3</strong>",
            "<strong>1</strong> e <strong>3</strong>",
            "<strong>1</strong>, <strong>2</strong> e <strong>3</strong>",
            "<strong>1</strong>, <strong>3</strong> e <strong>4</strong>",
        ]
        correct_choice = 2
    if true_props == [0, 3]:
        choices = [
            "<strong>1</strong>",
            "<strong>4</strong>",
            "<strong>1</strong> e <strong>4</strong>",
            "<strong>1</strong>, <strong>2</strong> e <strong>4</strong>",
            "<strong>1</strong>, <strong>3</strong> e <strong>4</strong>",
        ]
        correct_choice = 2
    if true_props == [1, 2]:
        choices = [
            "<strong>2</strong>",
            "<strong>3</strong>",
            "<strong>2</strong> e <strong>3</strong>",
            "<strong>1</strong>, <strong>2</strong> e <strong>3</strong>",
            "<strong>2</strong>, <strong>3</strong> e <strong>4</strong>",
        ]
        correct_choice = 2
    if true_props == [1, 3]:
        choices = [
            "<strong>2</strong>",
            "<strong>4</strong>",
            "<strong>2</strong> e <strong>4</strong>",
            "<strong>1</strong>, <strong>2</strong> e <strong>4</strong>",
            "<strong>2</strong>, <strong>3</strong> e <strong>4</strong>",
        ]
        correct_choice = 2
    if true_props == [2, 3]:
        choices = [
            "<strong>3</strong>",
            "<strong>4</strong>",
            "<strong>3</strong> e <strong>4</strong>",
            "<strong>1</strong>, <strong>3</strong> e <strong>4</strong>",
            "<strong>2</strong>, <strong>3</strong> e <strong>4</strong>",
        ]
        correct_choice = 2
    # Três corretas
    if true_props == [0, 1, 2]:
        choices = [
            "<strong>1</strong> e <strong>2</strong>",
            "<strong>1</strong> e <strong>3</strong>",
            "<strong>2</strong> e <strong>3</strong>",
            "<strong>1</strong>, <strong>2</strong> e <strong>3</strong>",
            "<strong>1</strong>, <strong>2</strong>, <strong>3</strong> e <strong>4</strong>",
        ]
        correct_choice = 3
    if true_props == [0, 1, 3]:
        choices = [
            "<strong>1</strong> e <strong>2</strong>",
            "<strong>1</strong> e <strong>4</strong>",
            "<strong>2</strong> e <strong>4</strong>",
            "<strong>1</strong>, <strong>2</strong> e <strong>4</strong>",
            "<strong>1</strong>, <strong>2</strong>, <strong>3</strong> e <strong>4</strong>",
        ]
        correct_choice = 3
    if true_props == [0, 2, 3]:
        choices = [
            "<strong>1</strong> e <strong>3</strong>",
            "<strong>1</strong> e <strong>4</strong>",
            "<strong>3</strong> e <strong>4</strong>",
            "<strong>1</strong>, <strong>3</strong> e <strong>4</strong>",
            "<strong>1</strong>, <strong>2</strong>, <strong>3</strong> e <strong>4</strong>",
        ]
        correct_choice = 3
    if true_props == [1, 2, 3]:
        choices = [
            "<strong>2</strong> e <strong>3</strong>",
            "<strong>2</strong> e <strong>4</strong>",
            "<strong>3</strong> e <strong>4</strong>",
            "<strong>2</strong>, <strong>3</strong> e <strong>4</strong>",
            "<strong>1</strong>, <strong>2</strong>, <strong>3</strong> e <strong>4</strong>",
        ]
        correct_choice = 3
    # Todas corretas
    if true_props == [0, 1, 2, 3]:
        choices = [
            "<strong>1</strong>, <strong>2</strong> e <strong>3</strong>",
            "<strong>1</strong>, <strong>2</strong> e <strong>4</strong>",
            "<strong>1</strong>, <strong>3</strong> e <strong>4</strong>",
            "<strong>2</strong>, <strong>3</strong> e <strong>4</strong>",
            "<strong>1</strong>, <strong>2</strong>, <strong>3</strong> e <strong>4</strong>",
        ]
        correct_choice = 4

    choices = [Text.parse_html(choice) for choice in choices]
    answer = [choices[correct_choice]]
    return choices, answer, correct_choice
