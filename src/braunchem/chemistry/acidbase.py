import numpy as np
import matplotlib.pyplot as plt

KW: float = 1e-14
"""Constante de autoionização da água."""


class Solution:
    C: float
    V: float


class StrongAcidSolution(Solution):
    C: float
    V: float

    def __init__(self, C, V):
        self.C = C
        self.V = V

    def charge_concentration(self, pH: float):
        """Retorna a concentração de carga da solução."""
        return -self.C


class StrongBaseSolution(Solution):
    C: float
    V: float

    def __init__(self, C, V):
        self.C = C
        self.V = V

    def charge_concentration(self, pH: float):
        """Retorna a concentração de carga da solução."""
        return self.C


class WeakAcidSolution(Solution):
    """Classe para soluções de ácidos fracos.

    Atributos:
        Ka (float): Constantes de acidez.
        C (float): Concentração da solução.
        V (float): Volume da solução.
        charge (int): Carga da molécula.
    """

    Ka: list[float]
    charge: int

    def __init__(self, Ka, C, V, charge=0):
        self.Ka = Ka
        self.C = C
        self.V = V
        self.charge = charge

    @property
    def ionizations(self) -> int:
        """Número de hidrogênios ionizáveis no ácido."""
        return len(self.Ka)

    def alpha(self, n: int, pH: float) -> float:
        """Calcula a fração molar da n-ésima base conjugada em um valor de pH."""
        hidronium_conc = 10 ** (-pH)

        coef = [
            np.prod(self.Ka[:i]) * hidronium_conc ** (self.ionizations - i)
            for i in range(self.ionizations + 1)
        ]

        return coef[n] / sum(coef)

    def charge_concentration(self, pH: float) -> float:
        """Retorna a concentração de carga da solução."""
        return self.charge - self.C * sum(
            i * self.alpha(i, pH) for i in range(self.ionizations + 1)
        )

    def alpha_plot(self, points=100):
        """Constroi o gráfico para a curva alfa."""
        pH_range = np.linspace(0, 14, points)

        y = []

        for i in range(self.ionizations + 1):
            y.append(np.array(list(map(lambda pH: self.alpha(i, pH), pH_range))))

        return pH_range, y


class WeakBaseSolution(WeakAcidSolution):
    """Classe para soluções de bases fracas.

    Atributos:
        Kb (float): Constantes de basicidade.
        C (float): Concentração da solução.
        V (float): Volume da solução.
        charge (int): Carga da molécula.
    """

    def __init__(self, Kb, C, V, charge=0):
        self.Ka = [KW / k for k in Kb]
        self.C = C
        self.V = V
        self.charge = charge + len(Kb)


class Titration:
    """Classe para titulações.

    Atributos:
        titrand (Solution): Solução a ser titulada.
        titrant (Solution): Solução titulante.
    """

    titrand: Solution
    titrant: Solution

    def __init__(self, titrand: Solution, titrant: Solution):
        self.titrand = titrand
        self.titrant = titrant

    def titrant_volume(self, pH: float) -> float:
        """Calcula o volume de titulante forte necessário para atingir um valor de pH."""
        hidronium_conc = 10 ** (-pH)
        hydroxide_conc = KW / hidronium_conc

        delta = hidronium_conc - hydroxide_conc

        return (
            -self.titrand.V
            * (self.titrand.charge_concentration(pH) + delta)
            / (self.titrant.charge_concentration(pH) + delta)
        )

    def curve(self, points=100):
        """Constroi o gráfico para a curva de titulação."""
        pH_range = np.linspace(-1, 15, points)

        x = []
        y = []

        for pH in pH_range:
            v = self.titrant_volume(pH)
            if v > 0 and v < self.titrant.V * 2:
                # multiplicar por 2 é importante! O volume varia muito rapidamente no final da titulação
                x.append(v)
                y.append(pH)

        return x, y


def main():
    # titrand = WeakAcidSolution(Ka=[7.6e-3, 6.2e-8, 2.1e-13], C=1, V=10)
    # titrant = StrongBaseSolution(C=1, V=40)

    # titrand = WeakBaseSolution(Kb=[2e-5], C=1, V=10)
    titrand = StrongBaseSolution(C=1, V=20)
    titrant = StrongAcidSolution(C=1, V=40)

    t = Titration(titrand, titrant)

    x, y = t.curve()

    plt.xlim([0, titrant.V])

    plt.plot(x, y)

    plt.show()


if __name__ == "__main__":
    main()
