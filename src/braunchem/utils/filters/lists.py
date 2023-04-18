"""
Custom lists
"""

import panflute as pf


def latex(text):
    return pf.RawBlock(text, format="latex")


def lists(elem, doc, debug=False):
    if doc.format == "latex" and isinstance(elem, pf.OrderedList):
        if elem.style == "LowerAlpha":
            return pf.BulletList(*elem.content)

        return elem

    return


def main(doc=None):
    return pf.run_filter(lists, doc=doc)


if __name__ == "__main__":
    main()
