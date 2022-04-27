import latex
from attr import frozen


@frozen
class PhysicalQuantity:
    id_: str
    name: str
    symbol: str = ''
    value: float = 0.0
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
    print(0)


if __name__ == "__main__":
    main()
