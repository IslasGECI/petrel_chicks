from scipy.optimize import curve_fit


def fit_model_age_vs_mass(ages_and_mass):
    return curve_fit(polinomio, ages_and_mass.Edad, ages_and_mass.Masa)


def polinomio(x, a, b, c):
    return a * x**2 + b * x + c
