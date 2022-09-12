from boolFun import BoolFun
from tkinter import *


def main():
    # 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0
    proba = BoolFun([0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1], 3)
    proba2 = BoolFun([1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1], 1)
    proba3 = BoolFun([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1,
                      0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0], 1)
    print(proba)
    proba.to_char_form()
    print(proba)
    proba.to_normal_form()
    print(proba)
    print("Transforamta Walsha-Hadamarda: \n", proba.transform_wh())
    proba.show_normal_form()
    print("Stopień algebraiczny: ", proba.algebraic_degree())
    print("Waga Hamminga: ", proba.hamming_weight())
    print("Odległość Hamminga dla : \n", proba, "\n", proba2, BoolFun.hamming_distance(proba, proba2))
    print("Nieliniowość: ", proba.non_linearity())
    print("Najbliższe liniowe: ")
    proba.closest_linear()
    print("Najdalsze liniowe: ")
    proba.farthest_linear()
    print("Najbliższe afiniczne: ")
    proba.closest_affine()
    print("Najdalsze afiniczne: ")
    proba.farthest_affine()
    print("Korelacja pomiedzy funkcjami: ", BoolFun.correlation_fun(proba, proba2))
    proba.balanced()
    print("Transformata: ", proba3.transform_wh())
    proba3.correlation_immune()
    # root = Tk()
    # root.geometry("1080x720")
    # root.title("Kalkulator Boolowski")
    # BoolApp(root)
    # root.mainloop()


if __name__ == "__main__":
    main()
