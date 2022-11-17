def parse_fractions(unit_str: str):
    try:
        numerator, denominator = unit_str.split("//", 1)
        return f"\\tfrac{{\\pu{{{numerator}}}}}{{{parse_fractions(denominator)}}}"
    except ValueError:
        return f"\\pu{{{unit_str}}}"


def main():
    test_str = r"kJ // mol // K lalala // C"

    out = parse_fractions(test_str)

    print(out)


if __name__ == "__main__":
    main()
