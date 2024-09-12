import pandas as pd

from petrel_chicks import filterPerSeason


def test_filterPerSeason():
    df = pd.DataFrame({"Fecha": [], "Anio": [], "ID_anillo": []})
    obtained = filterPerSeason(df)
