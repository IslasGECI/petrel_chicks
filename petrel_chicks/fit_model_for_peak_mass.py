from scipy.optimize import curve_fit
import pandas as pd


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


def calculate_max_weights_from_given_age(df, age):
    peak_mass_list = []
    for group, data in df.groupby("ID_unico"):
        peak_mass_value = data[data.Edad == age].Masa.max()
        peak_mass_list.append([group, peak_mass_value])
    return pd.DataFrame(peak_mass_list, columns=["ID_unico", "Peak_mass"])


def calculate_peak_mass_from_model_by_season(df):
    age_per_seasons = find_age_for_max_mass_from_data(df)
    return calculate_max_weights_from_given_age(df, age_per_seasons)
