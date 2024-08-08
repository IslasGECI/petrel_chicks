from petrel_chicks.fit_model_for_peak_mass import fit_model_for_peak_mass

import pandas as pd


def test_fit_model_age_vs_mass():
    ages_and_mass = pd.DataFrame({"ID": ["a", "a", "a"], "Masa": [5, 8, 0], "Edad": [0, 1, -1]})
    obtained_model = fit_model_age_vs_mass(ages_and_mass)
