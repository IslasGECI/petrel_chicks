from scipy.optimize import curve_fit


def find_age_for_max_mass_from_data(age_mass_data):
    parameters, _ = fit_model_mass_vs_age(age_mass_data)
    return find_age_for_max_mass(parameters)


def find_age_for_max_mass(parameters):
    return int(-parameters[1] / (2 * parameters[0]))


def fit_model_mass_vs_age(ages_and_mass):
    ages_and_mass_without_na = ages_and_mass.dropna(subset=["Edad", "Masa"])
    return curve_fit(
        quadratic_function, ages_and_mass_without_na.Edad, ages_and_mass_without_na.Masa
    )


def quadratic_function(x, a, b, c):
    return a * x**2 + b * x + c
