import latex
from dataclasses import dataclass
from decimal import Decimal, Context


@dataclass(frozen=True)
class PhysicalQuantity:
    id_: str
    name: str
    symbol: str = ''
    value: Decimal = 0.0
    unit: str = ''

    def __lt__(self, other):
        # order quantity collections alphabetically
        return self.name < other.name

    def latex(self):
        # siunitx format
        if not self.value:
            return self.name

        return f'${self.symbol} = {latex.qty(self.value, self.unit)}$'


def parse_pq(data_type: str, data_id: str, value: str, prec=3):
    """Creates physical quantity
    """

    name = 'Teste'
    symbol = 'Teste'

    return PhysicalQuantity(
        id_=f'{data_type}-{data_id}',
        value=Context(prec).create_decimal(value),
        name=name,
        symbol=symbol
    )


def main():
    pq = parse_pq('Hf', 'CO3-2!aq@298K', '1.0e-7')

    print(pq)
    print(pq.latex())


if __name__ == "__main__":
    main()
