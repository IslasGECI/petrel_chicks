import pandas as pd


def filterPerSeason(data):
    seasons = data.Anio.unique()
    dates = []
    rings = []
    recaptures = []

    for i in seasons:
        data_season = data[data.Anio == i]
        dates.append(len(data_season.Fecha.unique()))
        rings.append(len(data_season.ID_anillo.unique()))
        duplicados = data_season["ID_anillo"].duplicated(keep="last")
        recaptures.append(sum(duplicados))

    data = {"temporada": seasons, "eventos": dates, "capturas": rings, "recapturas": recaptures}

    dataframe = pd.DataFrame(data=data)
    return dataframe


def add_anio_column(df):
    df["Anio"] = pd.to_datetime(df.Fecha).dt.year
    return df
