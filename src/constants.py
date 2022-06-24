import latex
from dataclasses import dataclass


@dataclass(frozen=True)
class PhysicalQuantity:
    id_: str
    name: str
    symbol: str = ''
    value: str = ''  # value must be string to accept scientific notation
    unit: str = ''

    def __lt__(self, other):
        # used to order quantity collections alphabetically
        return self.name < other.name

    def latex(self):
        # siunitx format
        if not self.value:
            return self.name

        return f'${self.symbol} = {latex.qty(self.value, self.unit)}$'


def main():
    pq = PhysicalQuantity('a', 'Constante a', 'a', '0', 'm')
    print(pq.latex())


if __name__ == "__main__":
    main()
