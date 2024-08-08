from petrel_chicks import (
    calculate_time_days,
    logistic_model,
    inverse_logistic_model,
    initialize_logistic_model,
    fit_logistic_model,
    perform_fit,
    plot_morphometric_data,
    set_axis_labels,
    set_ticks_and_limits,
)
from geci_plots import geci_plot

import hashlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


dictionary = {
    "Fecha": ["2012-09-06", "2012-09-08"],
    "Edad": [1, 2],
    "Longitud_tarso": [1, 2],
    "Longitud_ala": [1, 2],
    "Longitud_pico": [1, 2],
    "Masa": [1, 2],
}
petrel_data = pd.DataFrame(dictionary)


def test_calculate_time_days():
    expected_days = np.array([1, 3])
    obtained_days = calculate_time_days(petrel_data)
    np.testing.assert_array_equal(expected_days, obtained_days)


A, t0, k, n = 10, 0.1, 2, 3
time_array = np.arange(5)


def test_logistic_model():
    expected_values = np.array([7.6640365, 9.50285763, 9.92652388, 9.98992847, 9.99863459])
    obtained_values = logistic_model(time_array, A, t0, k, n)
    np.testing.assert_allclose(expected_values, obtained_values)


def test_inverse_logistic_model():
    expected_values = np.array([-np.inf, -3.35337739, -2.31014078, -1.69227361, -1.2413662])
    obtained_values = inverse_logistic_model(time_array, A, t0, k, n)
    np.testing.assert_allclose(expected_values, obtained_values)


def test_initialize_logistic_model():
    expected_params_names = ["A", "t0", "k", "n"]
    expected_model_name = "Model(logistic_model)"
    expected_initial_values = [1, 1, 1, 1]
    obteined_model, obtained_params = initialize_logistic_model()
    assert expected_params_names == obteined_model.param_names
    assert expected_model_name == obteined_model.name
    assert expected_initial_values == list(obtained_params.valuesdict().values())


def test_fit_logistic_model():
    expected_params = np.array([A, t0, k, n])
    logistic_curve = pd.DataFrame({"log_curve": logistic_model(time_array, A, t0, k, n)})
    model, params = initialize_logistic_model()
    obtained_params = np.array(
        fit_logistic_model(model, params, logistic_curve, time_array, "log_curve")
    )
    np.testing.assert_allclose(obtained_params, expected_params)


def test_perform_fit():
    logistic_curve = pd.DataFrame({"log_curve": logistic_model(time_array, A, t0, k, n)})
    model, params = initialize_logistic_model()
    obtained_results_object = perform_fit(model, params, logistic_curve, time_array, "log_curve")
    assert obtained_results_object.max_nfev == 20000


def test_plot_morphometric_data():
    data_feature = pd.read_csv("tests/data/logistic_curve.csv")
    fig, ax = plt.subplots()
    plot_morphometric_data(ax, data_feature, "Longitud_ala")
    set_ticks_and_limits(ax, data_feature, "Longitud_ala")
    output_path = "tests/baseline/test_plot_morphometric_data.png"
    plt.savefig(output_path)
    file_content = open(output_path, "rb").read()
    obtained_hash = hashlib.md5(file_content).hexdigest()
    expected_hash = "f36abf26f39e6d98782641cac1c8477f"
    assert obtained_hash == expected_hash


def test_set_axis_labels():
    fig1, expected_ax_one = geci_plot()
    fig2, expected_ax_two = geci_plot()

    fig3, obteined_ax_one = geci_plot()
    fig4, obteined_ax_two = geci_plot()

    variable_uno = "Masa"
    label_uno = "Masa (g)"
    variable_dos = "Longitud_Total"
    label_dos = "Longitud Total (mm)"
    expected_x_label = "Días desde la eclosión"

    expected_ax_one.set_xlabel("Días desde la eclosión", fontsize=25, labelpad=10)
    expected_ax_one.set_ylabel(label_uno, fontsize=25, labelpad=10)

    set_axis_labels(obteined_ax_one, morphometric_variable=variable_uno)
    ax_one_obtained_xlabel = obteined_ax_one.get_xlabel()
    ax_one_obtained_ylabel = obteined_ax_one.get_ylabel()
    ax_one_obtained_labelpad = obteined_ax_one.yaxis.labelpad

    expected_ax_two.set_xlabel("Días desde la eclosión", fontsize=25, labelpad=10)
    expected_ax_two.set_ylabel(label_dos, fontsize=25, labelpad=10)

    set_axis_labels(obteined_ax_two, morphometric_variable=variable_dos)
    ax_two_obtained_xlabel = obteined_ax_two.get_xlabel()
    ax_two_obtained_ylabel = obteined_ax_two.get_ylabel()
    ax_two_obtained_labelpad = obteined_ax_two.yaxis.labelpad

    assert ax_one_obtained_xlabel == expected_x_label
    assert ax_one_obtained_ylabel == label_uno
    assert ax_one_obtained_labelpad == 10

    assert ax_two_obtained_xlabel == expected_x_label
    assert ax_two_obtained_ylabel == label_dos
    assert ax_two_obtained_labelpad == 10
