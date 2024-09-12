import pandas as pd

from petrel_chicks import filterPerSeason


def test_filterPerSeason():
    df = pd.DataFrame(
        {
            "Fecha": ["12/Sep/2024", "13/Sep/2024", "12/Ago/2023"],
            "Anio": [2024, 2024, 2023],
            "ID_anillo": ["A01", "A01", "A01"],
        }
    )
    obtained = filterPerSeason(df)
    expected_rows = 2
    obtained_rows = len(obtained)

    assert obtained_rows == expected_rows
    expected_columns = ["temporada", "eventos", "capturas", "recapturas"]
    assert expected_columns in obtained.columns.values

    expected_recaptures = [1, 0]
    obtained_recaptures = obtained.recapturas
    assert (obtained_recaptures == expected_recaptures).all()

    df = pd.DataFrame(
        {
            "Fecha": ["12/Sep/2024", "13/Sep/2024", "14/Ago/2024", "15/Ago/2024"],
            "Anio": [2024, 2024, 2024, 2024],
            "ID_anillo": ["A01", "A01", "A02", "A02"],
        }
    )
    obtained = filterPerSeason(df)
    expected_recaptures = [2]
    obtained_recaptures = obtained.recapturas
    assert (obtained_recaptures == expected_recaptures).all()

    expected_resume = [2024, 4, 2, 2]
    assert (obtained.iloc[0].values == expected_resume).all()
