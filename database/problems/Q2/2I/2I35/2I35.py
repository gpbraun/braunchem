import matplotlib.pyplot as plt
from braunchem.utils.acidbase import WeakAcidSolution, StrongBaseSolution, Titration


def main():
    acid = WeakAcidSolution(Ka=[2e-5], C=4e-4, V=25)
    base = StrongBaseSolution(C=1e-3, V=20)

    t = Titration(acid, base)

    x, y = t.curve()

    plt.xlim([0, base.V])

    plt.plot(x, y)

    plt.show()


if __name__ == "__main__":
    main()
