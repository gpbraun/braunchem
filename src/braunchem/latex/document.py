import braunchem.utils.latex as latex

import logging
import subprocess
import shutil
from pathlib import Path
import importlib.resources

logger = logging.getLogger(__name__)

TEX_TEMPLATES_PATH = importlib.resources.files("braunchem.latex.templates")
"""Diretório da base de dados."""


def run_latexmk(tex_path: Path):
    """Executa o comando `latexmk`."""
    logger.info(f"Compilando o arquivo '{tex_path}' com latexmk.")
    latexmk = subprocess.run(
        [
            shutil.which("latexmk"),
            "-shell-escape",
            "-interaction=nonstopmode",
            "-file-line-error",
            "-pdf",
            "-cd",
            str(tex_path),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    logger.debug(f"Comando executado: '{' '.join(latexmk.args)}'")
    if latexmk.stdout:
        try:
            logger.info(latexmk.stdout.decode())
        except UnicodeDecodeError:
            pass
    if latexmk.stderr:
        try:
            logger.warning(latexmk.stderr.decode())
        except UnicodeDecodeError:
            pass
    logger.info(f"Arquivo {tex_path} compilado com latexmk!")


def run_tectonic(tex_path: Path):
    """Executa o comando `latexmk`."""
    logger.info(f"Compilando o arquivo '{tex_path}' com tectonic.")
    tectonic = subprocess.run(
        [
            shutil.which("tectonic"),
            "-X",
            "compile",
            "--keep-intermediates",
            str(tex_path),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    logger.debug(f"Comando executado: '{' '.join(tectonic.args)}'")
    if tectonic.stdout:
        logger.info(tectonic.stdout.decode())
    if tectonic.stderr:
        logger.warning(tectonic.stderr.decode())
    logger.info(f"Arquivo '{tex_path}' compilado com tectonic!")


def run_pdf2svg(tex_path: Path, svg_path: Path | None = None, run_scour=True):
    """Executa o comando `pdf2svg`."""
    pdf2svg = subprocess.run(
        [
            "pdf2svg",
            str(tex_path),
            str(svg_path),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if pdf2svg.stdout:
        logger.info(pdf2svg.stdout.decode())
    if pdf2svg.stderr:
        logger.warning(pdf2svg.stderr.decode())

    if run_scour:
        scour = subprocess.run(
            [
                "scour",
                str(svg_path),
                "--enable-viewboxing",
                "--enable-id-stripping",
                "--shorten-ids",
                "--indent=none",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        svg_path.write_bytes(scour.stdout)
        if scour.stderr:
            logger.info(scour.stderr.decode())

    logger.info(f"Arquivo '{tex_path}' convertido em '{svg_path}'.")


def run_pdfcrop(pdf_path: Path):
    """Executa o comando `latexmk`."""
    pdfcrop = subprocess.run(
        [
            shutil.which("pdfcrop"),
            str(pdf_path),
            str(pdf_path),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    logger.debug(f"Comando executado: '{' '.join(pdfcrop.args)}'")
    if pdfcrop.stdout:
        logger.info(pdfcrop.stdout.decode())
    if pdfcrop.stderr:
        logger.warning(pdfcrop.stderr.decode())
    logger.info(f"Bordas removidas no arquivo '{pdf_path}'!")


class Document:
    """Documento em LaTeX."""

    def __init__(
        self,
        id_: str | None,
        path: str | None = None,
        title: str | None = None,
        author: str | None = None,
        affiliation: str | None = None,
        template: str | None = None,
        contents: str | None = None,
        toc: bool = False,
        standalone: bool = False,
    ):
        self.id_ = id_
        self.path = path
        self.title = title
        self.author = author
        self.affiliation = affiliation
        self.template = template
        self.contents = contents
        self.standalone = standalone
        self.toc = toc

    @property
    def preamble(self) -> str:
        """Preâmbulo do documento"""
        if self.standalone:
            return ""

        return "\n".join(
            [
                latex.cmd("path", self.path) if self.path else "",
                latex.cmd("title", self.title) if self.title else "",
                latex.cmd("author", self.author) if self.author else "",
                latex.cmd("affiliation", self.affiliation) if self.affiliation else "",
            ]
        )

    @property
    def cls(self) -> str:
        """Comando que especifica a classe do documento."""
        return "braunfigure" if self.standalone else "braun"

    @property
    def documentclass(self) -> str:
        """Comando que especifica a classe do documento."""
        if not self.template:
            return f"\\documentclass{{{self.cls}}}\n"

        return f"\\documentclass[{self.template}]{{{self.cls}}}\n"

    @property
    def body(self) -> str:
        """Corpo do documento em LaTeX."""
        if self.standalone:
            return latex.env("document", self.contents)
        if not self.toc:
            return latex.env("document", f"\\maketitle\n\n{self.contents}")

        return latex.env(
            "document", f"\\maketitle\n\n\\tableofcontents\n\n{self.contents}"
        )

    def document(self) -> str:
        return "\n".join(
            [
                self.documentclass,
                self.preamble,
                self.body,
            ]
        )

    # TODO: Da pra fazer uma função que cria o diretório temporário e uma função que roda os pdf, assim a paralelização pode ser feita nesse módulo em vez de no módulo de tópicos.

    def write_pdf(
        self, tmp_dir: Path, out_dir: Path | None = None, tectonic: bool = False
    ) -> Path:
        """Gera o `pdf` e copia para um diretório de saída.

        Args:
            tmp_dir (Path): Diretório para arquivos temporários.
            out_dir (Path): Diretório de saída.
        """
        tmp_dir.mkdir(parents=True, exist_ok=True)

        # copia os arquivos do template para o diretório temporário
        cls_path = TEX_TEMPLATES_PATH.joinpath(self.cls).with_suffix(".cls")
        shutil.copy(cls_path, tmp_dir)

        # copia o braunchem.sty (melhorar isso)
        braun_chem_path = TEX_TEMPLATES_PATH.joinpath("braunchem.sty")
        shutil.copy(braun_chem_path, tmp_dir)

        tex_path = tmp_dir.joinpath(self.id_).with_suffix(".tex")
        tex_path.write_text(self.document())

        if tectonic:
            run_tectonic(tex_path)
        else:
            run_latexmk(tex_path)

        pdf_path = tex_path.with_suffix(".pdf")

        if self.standalone:
            run_pdfcrop(pdf_path)

        if out_dir:
            out_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy(src=tex_path.with_suffix(".pdf"), dst=out_dir)

        return pdf_path

    def write_svg(self, tmp_dir: Path, out_dir: Path | None = None) -> Path:
        """Gera o `svg` e copia para um diretório de saída.

        Args:
            tmp_dir (Path): Diretório para arquivos temporários.
            out_dir (Path): Diretório de saída.
        """
        pdf_path = self.write_pdf(tmp_dir)

        if not out_dir:
            out_dir = tmp_dir
        else:
            out_dir.mkdir(parents=True, exist_ok=True)

        svg_path = out_dir.joinpath(self.id_).with_suffix(".svg")
        run_pdf2svg(pdf_path, svg_path)

        return svg_path
