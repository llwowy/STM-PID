import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import signal


def read_and_prepare_data(filename):

    data = pd.read_csv('max2.csv')

    y_values = data.iloc[:, 0].values

    num_samples = len(y_values)
    x_values = np.linspace(0, 140000, num_samples)

    return x_values, y_values


def inertial_model(t, k, T):
    """
    Model obiektu inercyjnego G = k/(sT+1)
    Odpowiedź skokowa: y(t) = k*(1-exp(-t/T))
    """
    return k * (1 - np.exp(-t / T))+28


def fit_and_plot(x_values, y_values):

    y_normalized = (y_values - y_values.min()) / (y_values.max() - y_values.min())

    try:
        popt, _ = curve_fit(inertial_model, x_values, y_values, p0=[1.0, 1000])
        k_opt, T_opt = popt
    except RuntimeError:
        print("Nie udało się dopasować modelu - spróbuj innych wartości początkowych")
        return


    y_model = inertial_model(x_values, k_opt, T_opt)


    plt.figure(figsize=(12, 6))
    plt.plot(x_values/100, y_values, 'b-', label='Dane pomiarowe')
    plt.plot(x_values/100, y_model, 'r--', label='Model inercyjny')
    plt.xlabel('Czas [s]')
    plt.ylabel('Znormalizowana wartość')
    plt.title(f'Dopasowanie obiektu inercyjnego\nk={k_opt:.3f}, T={T_opt/100:.1f}s')

    plt.grid(visible=True, which='major', linestyle='-', linewidth=0.75, alpha=0.9)  # Główna siatka
    plt.grid(visible=True, which='minor', linestyle='--', linewidth=0.5, alpha=0.7)  # Dokładna siatka
    plt.minorticks_on()

    plt.legend()
    plt.show()

    print(f"Dopasowane parametry:")
    print(f"k = {k_opt:.3f}")
    print(f"T = {T_opt/100:.1f}s")


def main():

    filename = "dane.csv"

    try:
        x_values, y_values = read_and_prepare_data(filename)
        fit_and_plot(x_values, y_values)
    except FileNotFoundError:
        print(f"Nie znaleziono pliku {filename}")
    except Exception as e:
        print(f"Wystąpił błąd: {str(e)}")


if __name__ == "__main__":
    main()