import hashlib
from petrel_chicks import (
    Cleaner_Morphometric,
    Fitter,
    Plotter,
    Predictions_and_Parameters,
    correct_age,
    fill_empty_age,
    get_subset_morphometric_data,
    select_data_per_burrow,
    update_with_age,
)
import pandas as pd
import numpy as np
import json
import os
import io
from datetime import timedelta, datetime

from pandas._testing import assert_frame_equal

dictionary = {
    "Fecha": ["2012-09-06", "2012-09-08"],
    "Edad": [1, 2],
    "Longitud_tarso": [1, 2],
    "Longitud_ala": [1, 2],
    "Longitud_pico": [1, 2],
    "Masa": [1, 2],
}
errores = {
    "Edades": [1, 2],
    "Error": [3, 2],
}
petrel_data = pd.DataFrame(dictionary)

features_list = ["Masa", "Longitud_pico"]
observables_list = ["Edad"]


def test_Cleaner_Morphometric_train_test_split():
    subset = Cleaner_Morphometric(petrel_data, features_list, observables_list)
    X_train, X_test, y_train, y_test = subset.train_test_split()
    expected_features = ["Masa", "Longitud_pico"]
    assert (X_train.columns.values == expected_features).all()
    expected_train = petrel_data[expected_features].loc[[False, True]]
    assert X_train.iloc[0, 1] == expected_train.iloc[0, 1]


def test_Fitter(mocker):
    def train_test_split(self):
        return (
            np.array([6, 4, 8]).reshape(-1, 1),
            np.array([1, 2, 3]).reshape(-1, 1),
            [3, 2, 4],
            pd.DataFrame({"y_train": [4]}),
        )

    mocker.patch(
        "petrel_chicks.petrel_age_predictor.Cleaner_Morphometric.train_test_split", train_test_split
    )
    Morphometric_Data = Cleaner_Morphometric(petrel_data, features_list, observables_list)
    Fitter_model = Fitter(Morphometric_Data)
    assert Fitter_model.lineal_model.normalize
    Fitter_model.fit_model()
    Fitter_model.predict()
    are_equal = np.allclose(Fitter_model.predictions, np.array([0.5, 1.0, 1.5]))
    assert are_equal
    Fitter_model.calculate_absolute_error()
    are_equal = np.allclose(Fitter_model.absolute_error_in_days, np.array([3.5, 3.0, 2.5]))
    assert are_equal
    predictions_dict, linear_model_parameters = Fitter_model.calculate_results()
    assert "Edades" in predictions_dict.keys()
    assert "Predicciones" in predictions_dict.keys()
    assert "Error" in predictions_dict.keys()
    assert "Alpha" in linear_model_parameters.keys()
    assert "Beta" in linear_model_parameters.keys()
    delete_data_processed()
    Open = mocker.spy(io, "open")
    makedirs = mocker.spy(os, "makedirs")
    path_exist = mocker.spy(os.path, "exists")
    Fitter_model.dump_model()
    path_exist.assert_called_with("data")
    makedirs.assert_called_with("data", exist_ok=False)
    filename = "data/processed/trained_linear_model.pickle"
    Open.assert_called_once_with(filename, "wb")


def test_Predictions_and_Parameters(mocker):
    Model_Fitter = mocker.Mock(spec=Fitter)
    Model_Fitter.calculate_results.return_value = errores, dictionary
    Prediction = Predictions_and_Parameters(errores, dictionary)
    delete_reports_nontabular()
    path = "reports/figures/salida.json"
    makedirs = mocker.spy(os, "makedirs")
    path_exist = mocker.spy(os.path, "exists")
    Prediction.result_to_json(path)
    makedirs.assert_called_once_with("reports/non-tabular")
    path_exist.assert_called_with("reports")
    with open(path, encoding="utf8") as info_file:
        information = json.load(info_file)
    assert information == {**errores, **dictionary}
    ages, prediction_days_diff = Prediction.data_for_plot()
    assert ages == errores["Edades"]
    assert prediction_days_diff == errores["Error"]


def test_Plotter(mocker):
    Parameters = mocker.Mock(spec=Predictions_and_Parameters)
    Parameters.data_for_plot.return_value = [1, 2, 3], [1, 2, 3]
    Plotter_parameters = Plotter(Parameters)
    Plotter_parameters.plot()
    output_path = "reports/figures/figura.png"
    Plotter_parameters.savefig(output_path)
    file_content = open(output_path, "rb").read()
    obtained_hash = hashlib.md5(file_content).hexdigest()
    expected_hash = "ab08f5f70507f53387c5a53522be33a5"
    assert obtained_hash == expected_hash


def test_Plotter_(mocker):
    delete_reports_figures()
    Parameters = mocker.Mock(spec=Predictions_and_Parameters)
    Parameters.data_for_plot.return_value = [1, 2, 3], [1, 2, 3]
    Plotter_parameters = Plotter(Parameters)
    Plotter_parameters.plot()
    makedirs = mocker.spy(os, "makedirs")
    Plotter_parameters.savefig("reports/figures/figura.png")
    makedirs.assert_called_once_with("reports/figures")


def test_get_subset_morphometric_data(mocker):
    predictions = [1, 2, 3]
    expected_data_subset_dictionary = {
        "Fecha": ["01/Jan/2021", "02/Feb/2021", "03/Mar/2021"],
        "age_predictions": predictions,
        "Fecha_dt": [datetime(2021, 1, 1), datetime(2021, 2, 2), datetime(2021, 3, 3)],
    }
    expected_data_subset = pd.DataFrame(expected_data_subset_dictionary)
    data_subset = pd.DataFrame({"Fecha": ["01/Ene/2021", "02/Feb/2021", "03/Mar/2021"]})
    Cleaner_Morphometric = mocker.Mock()
    Cleaner_Morphometric.data_subset = data_subset.copy()
    Predictor = mocker.Mock()
    Predictor.predictions = predictions
    obtained_data_subset = get_subset_morphometric_data(Cleaner_Morphometric, Predictor)
    assert_frame_equal(obtained_data_subset, expected_data_subset)


def delete_reports_figures():
    os.system("rm -rf reports/figures")


def delete_reports_nontabular():
    os.system("rm -rf reports/non-tabular")


def delete_data_processed():
    os.system("rm -rf data")


def test_correct_age():
    delta = timedelta(days=50)
    data_dict = {"age_predictions": [2, 2, 2], "Time_diff_days": [delta, delta, delta]}
    obtained_data_per_burrow = pd.DataFrame(data_dict)
    correct_age(obtained_data_per_burrow)

    expected_data_dict = {"age_predictions": [2, 52, 102], "Time_diff_days": [delta, delta, delta]}
    expected_data_per_burrow = pd.DataFrame(expected_data_dict)

    assert_frame_equal(obtained_data_per_burrow, expected_data_per_burrow)


def test_select_data_per_burrow():
    data_dict = {
        "ID_unico": [1, 1, 2, 3],
        "Fecha": ["03/May/2022", "04/May/2022", "05/May/2022", "06/May/2022"],
        "age_predictions": [1, 2, 2, 2],
        "Fecha_dt": [
            datetime(2022, 5, 3),
            datetime(2022, 5, 4),
            datetime(2022, 5, 5),
            datetime(2022, 5, 6),
        ],
    }
    obtained_data_subset = pd.DataFrame(data_dict)

    obtained_id_petrel_chick = 1
    obtained_data_per_burrow = select_data_per_burrow(
        obtained_data_subset, obtained_id_petrel_chick
    )
    delta = timedelta(days=1)
    expected_data_dict = {
        "ID_unico": [1, 1],
        "Fecha": ["03/May/2022", "04/May/2022"],
        "age_predictions": [1, 2],
        "Fecha_dt": [datetime(2022, 5, 3), datetime(2022, 5, 4)],
        "Time_diff_days": [float("NaN"), delta],
    }
    expected_data_per_burrow = pd.DataFrame(expected_data_dict)

    assert_frame_equal(obtained_data_per_burrow, expected_data_per_burrow)


def test_update_with_age():
    data_dict = {"age_predictions": [4, 6, 9]}
    obtained_data_per_burrow = pd.DataFrame(data_dict)

    original_data_modified = {"Edad": [999, 999, 999]}
    obtained_data_modified = pd.DataFrame(original_data_modified)

    update_with_age(obtained_data_modified, obtained_data_per_burrow)
    expected_data_modified = pd.DataFrame({"Edad": [4, 6, 9]})

    assert_frame_equal(obtained_data_modified, expected_data_modified)


def test_fill_age_empty():
    raw_data_modified = pd.DataFrame({"Edad": [4, np.nan, 6, np.nan, np.nan, 9, 10]})
    expected_data_modified = pd.DataFrame({"Edad": [4, 5, 6, 7, 8, 9, 10]})
    obtained_data_modified = fill_empty_age(raw_data_modified)
    assert_frame_equal(obtained_data_modified, expected_data_modified)

    two_ids_data_modified = pd.DataFrame(
        {
            "Edad": [4, np.nan, 6, np.nan, np.nan, 9, 10],
            "ID_unico": ["uno", "uno", "uno", "uno", "dos", "dos"],
        }
    )
    expected_data_modified = pd.DataFrame({"Edad": [4, 5, 6, 7, 8, 9, 10]})

    obtained_data_modified = fill_empty_age(two_ids_data_modified)
    assert_frame_equal(obtained_data_modified, expected_data_modified)
