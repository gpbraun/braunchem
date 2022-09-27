import importlib.resources

TEX_TEMPLATES_PATH = importlib.resources.files("braunchem.latex.templates")
"""Diretório da base de dados."""

print(TEX_TEMPLATES_PATH)
