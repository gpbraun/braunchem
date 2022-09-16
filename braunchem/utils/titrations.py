import numpy as np
import matplotlib.pyplot as plt

KW = 1e-14
"""Constante de autoionização da água."""


class WeakAcidTitration:
    """Classe para titulações de ácido fraco com base forte

    Atributos:
        Ka (float): Constante de acidez.
        Ca (float): Concentração do ácido graco.
        Va (float): Volume da solução de ácido fraco.
        Cb (float): Concentração da solução de base forte.
        Vb (float): Volume máximo empregado da solução de base forte.
    """

    Ka: float
    Ca: float
    Va: float
    Cb: float
    Vb: float

    def __init__(self, Ka, Ca, Va, Cb, Vb):
        self.Ka = Ka
        self.Ca = Ca
        self.Va = Va
        self.Cb = Cb
        self.Vb = Vb

    def volume(self, pH):
        """Calcula o volume necessário para atingir um determinado valor de pH."""
        hidronium_conc = 10 ** (-pH)
        hydroxide_conc = KW / hidronium_conc

        delta = hidronium_conc - hydroxide_conc
        alpha = self.Ka / (hidronium_conc + self.Ka)

        return self.Va * (self.Ca * alpha - delta) / (self.Cb + delta)

    def plot(self):
        """Constroi o gráfico para a curva de titulação."""
        pH_range = np.linspace(0, 14, 100)

        x = []
        y = []

        for pH in pH_range:
            v = self.volume(pH)
            if v > 0 and v < self.Vb * 2:
                # multiplicar por 2 é importante! O volume varia muito rapidamente no final da titulação
                x.append(v)
                y.append(pH)

        return x, y


def main():
    t = WeakAcidTitration(Ka=2e-5, Ca=4e-4, Va=25, Cb=1e-3, Vb=20)
    x, y = t.plot()

    plt.plot(x, y)
    plt.show()


if __name__ == "__main__":
    main()
