import panflute as pf

from pathlib import Path


def figures(elem, doc, debug=False):
    if isinstance(elem, pf.Image) and doc.format in ["latex"]:
        metadata = doc.get_metadata()
        if "path" in metadata:
            figure_path = Path(metadata["path"]).parent.joinpath(elem.url)
            tex_path = figure_path.with_suffix(".tex")

            if tex_path.exists():
                return pf.RawInline(tex_path.read_text(), "latex")

            return pf.RawInline(f"includegraphics{{{figure_path}}}", "latex")

        return elem


def main(doc=None):
    return pf.run_filter(figures, doc=doc)


if __name__ == "__main__":
    main()
