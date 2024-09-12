import pandas as pd


def filterPerSeason(data):
    seasons = data.Anio.unique()
    dates = []
    rings = []
    recaptures = []

    for i in seasons:
        data_season = data[data.Anio == i]
        dates.append(len(data_season.Fecha.unique()))
        rings.append(len(data_season.Id_anillo.unique()))
        duplicados = data_season["Id_anillo"].duplicated(keep=False)
        data_anillos = data_season[duplicados]
        recaptures.append(len(data_anillos))

    data = {"temporada": seasons, "eventos": dates, "capturas": rings, "recapturas": recaptures}

    dataframe = pd.DataFrame(data=data)
    return dataframe
