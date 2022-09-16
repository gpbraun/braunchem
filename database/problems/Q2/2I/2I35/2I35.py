import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass

KW = 1e-14


@dataclass
class WeakAcidTitration:
    Ka: float
    Ca: float
    Va: float
    Cb: float
    Vb: float

    def volume(self, pH):
        """Calcula o volume necessário para atingir um determinado valor de pH."""
        hidronium_conc = 10 ** (-pH)

        delta = hidronium_conc - KW / hidronium_conc
        alpha = self.Ka / (hidronium_conc + self.Ka)

        return self.Va * (self.Ca * alpha - delta) / (self.Cb + delta)

    def points(self, points=100):
        """Constroi o gráfico para a curva de titulação."""
        pH_range = np.linspace(0, 14, points)

        for pH in pH_range:
            v = self.volume(pH)
            if v > 0 and v < self.Vb * 2:
                yield v, pH

    def latex(self):
        """Cria a figura do gráfico em latex."""
        points = "\n\t\t\t".join(f"({x:.3f}, {y:.3f})" for x, y in self.points())

        return f"""\\begin{{tikzpicture}}
    \\begin{{axis}}
        [
            grid = major,
            xlabel = {{Volume de solução básica, $V/\\unit{{mL}}$}},
            ylabel = {{$\\mathrm{{pH}}$}},
            xmin=0, xmax={self.Vb},
        ]
    \\addplot coordinates
        {{
            {points}   
        }};
    \end{{axis}}
\end{{tikzpicture}}
"""


def main():
    t = WeakAcidTitration(Ka=2e-5, Ca=4e-4, Va=25, Cb=1e-3, Vb=20)

    with open("database/problems/Q2/2I/2I35/2I35-1P.tex", "w") as file:
        file.write(t.latex())


if __name__ == "__main__":
    main()
