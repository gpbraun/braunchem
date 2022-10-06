"""
Fenced divs
"""

import panflute as pf


def latex(text):
    return pf.RawBlock(text, format="latex")


def div2env(elem, doc, debug=False):
    if isinstance(elem, pf.Div) and doc.format == "latex":
        env = elem.classes[0]

        begin = latex(f"\n\\begin{{{env}}}\n")
        end = latex(f"\n\\end{{{env}}}\n")

        elem = pf.Div(begin, *elem.content, end)

        return elem

    return


def main(doc=None):
    return pf.run_filter(div2env, doc=doc)


if __name__ == "__main__":
    main()
