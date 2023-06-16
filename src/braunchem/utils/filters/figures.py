from pathlib import Path

import panflute as pf


def figures(elem, doc, debug=False):
    if isinstance(elem, pf.Image) and doc.format in ["latex"]:
        metadata = doc.get_metadata()
        if "path" in metadata:
            figure_path = Path(metadata["path"]).parent.joinpath(elem.url)
            tex_path = figure_path.with_suffix(".tex")

            if tex_path.exists():
                return pf.RawInline(tex_path.read_text(), "latex")

            pdf_path = figure_path.with_suffix(".pdf")
            if pdf_path.exists():
                return pf.RawInline(f"\\includegraphics{{{pdf_path}}}", "latex")

            if figure_path.suffix == ".svg":
                return pf.RawInline(f"\\includesvg{{{figure_path}}}", "latex")

            return pf.RawInline(
                f"\\includegraphics[width=0.9\linewidth]{{{figure_path}}}", "latex"
            )

        return elem


def main(doc=None):
    return pf.run_filter(figures, doc=doc)


if __name__ == "__main__":
    main()
