from petrel_chicks.fit_model_for_peak_mass import (
    fit_model_age_vs_mass,
    find_age_for_max_mass,
    find_age_for_max_mass_from_data,
)

import pandas as pd


ages_and_mass = pd.DataFrame({"ID": ["a", "a", "a"], "Masa": [5, 8, 0], "Edad": [0, 1, -1]})


def test_find_age_for_max_mass_from_data():
    obtained_age = find_age_for_max_mass_from_data(ages_and_mass)
    expected_age = 2
    assert obtained_age == expected_age


def test_fit_model_age_vs_mass():
    obtained_parameters, _ = fit_model_age_vs_mass(ages_and_mass)
    expected_parameters = [-1, 4, 5]
    assert all(obtained_parameters == expected_parameters)


def tests_find_age_for_max_mass():
    parameters = [-1, 4, 5]
    obtained_age = find_age_for_max_mass(parameters)
    expected_age = 2
    assert obtained_age == expected_age
