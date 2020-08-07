# Funciones para obtener el dataframe de la info sobre las estaciones.
# Esta por ver si esta es la mejor forma.
# Solamente hay que llamar a getCleanDataFrame para tener un dataframe limpio.
# Si hay cosas que veamos qeu se necesiten o sobren del dataframe se añade


import numpy as np
import pandas as pd
from pyunpack import Archive
from os import listdir


def ChooseInterval(df, StartDate, EndDate, Value):
    c0 = df.index.to_series().between(StartDate, EndDate)
    return df[c0][Value]


def ChooseAccuracy(df, Accuracy):
    return df.resample(Accuracy).median()


def ChooseComparison(df, Comparator, Interval=''):
    Decisions = {'Y': df.index.year,
                 'M': df.index.month,
                 'd': df.index.day,
                 'dow': df.index.dayofweek,
                 'h': df.index.hour,
                 'bd': df.index.dayofweek < 5
                 }
    if Comparator == '':
        return df.groupby([Decisions[Comparator]]).median()
    else:

        return df.groupby([Decisions[Comparator], Decisions[Interval]]).median()


class Ploteo:
    def __init__(self, df, decoder):
        self.Index = df.dropna().index.tolist()
        self.Date = str(df.dropna().name)
        self.Value = df.dropna().tolist()
        self.Latitude = []
        self.Longitude = []
        self.Address = []
        for i in self.Index:
            self.Latitude.append(decoder.get(i, 'Latitude'))
            self.Longitude.append(decoder.get(i, 'Longitude'))
            self.Address.append(decoder.get(i, 'Address'))


def error(x):
    return x.dropna()[0]


def SaveDecoderList():

    data = concatenateAll(
        "../DataFrames/Stations/")
    print('Concatenado')
    Address = data['Address'].apply(lambda x: error(x), axis=0)
    Longitude = data['Longitude'].apply(lambda x: error(x), axis=0)
    Latitude = data['Latitude'].apply(lambda x: error(x), axis=0)
    Number = data['Number'].apply(lambda x: error(x), axis=0)
    Tabla = pd.DataFrame([Number, Address, Latitude, Longitude]).T
    Tabla['Number'] = Tabla[0]
    Tabla['Address'] = Tabla[1]
    Tabla['Latitude'] = Tabla[2]
    Tabla['Longitude'] = Tabla[3]
    Tabla.drop([0, 1, 2, 3], axis=1).to_csv(
        '../DataFrames/DatosEstaticos.txt', encoding='latin1')
    data = 0
    return 0


def concatenateAll(filePath):
    ListFiles = listdir(filePath)
    print('1')
    ListFiles = ListFiles[:-1]
    print(ListFiles)
    return pd.concat(load_files([filePath + str(s) for s in ListFiles]), axis=0)


def load_files(filenames):
    for filename in filenames:
        yield pd.read_pickle(filename)


def fromJSONtoPickle(filePath):
    ListFiles = listdir(filePath)
    for file in ListFiles:
        if ("json" in file) & (not (alreadyToStations(file.split(".")[0]+".pkl"))):
            getCleanDataframe(filePath + "/"+file)
            writeToPickleStationsList(file.split(".")[0]+".pkl")
            print(file + " Correctly transformed")
    print('Finished!')


def list_files(directory, extension):
    return (f for f in listdir(directory) if f.endswith('.' + extension))


def alreadyToStations(link):
    f = open("../DataFrames/Stations/PickleIndex.txt", "r")
    saved = f.read()
    if link in saved:
        return True
    else:
        return False
    f.close()


def writeToPickleStationsList(link):
    f = open("../DataFrames/Stations/PickleIndex.txt", "a")
    f.writelines("\n" + link)
    f.close()
    return 0


def getCleanDataframe(filePath):

    df = getRawDataFrame(filePath)

    df = finalDataFrame(df)
    # SaveInPickle in new folder where rest of dataframes are
    saveInPickle(df, "../DataFrames/Stations/" +
                 filePath.split("/")[-1].split(".")[0]+".pkl")
    return 0


def getRawDataFrame(filePath):

    return pd.read_json(filePath, orient='records',
                        lines=True, encoding="ISO 8859-1")


def chooseData(x, y):

    if type(x) == dict:

        return x[y]
    else:
        return float('NaN')


def finalDataFrame(df):
    a = df.explode('stations')
    a['Reservation'] = a['stations'].apply(
        lambda x: chooseData(x, 'reservations_count'))
    a['Light'] = a['stations'].apply(lambda x: chooseData(x, 'light'))
    a['FreeBases'] = a['stations'].apply(lambda x: chooseData(x, 'free_bases'))
    a['no_available'] = a['stations'].apply(
        lambda x: chooseData(x, 'no_available'))
    a['DockBikes'] = a['stations'].apply(lambda x: chooseData(x, 'dock_bikes'))
    a['Latitude'] = a['stations'].apply(lambda x: chooseData(x, 'latitude'))
    a['Longitude'] = a['stations'].apply(lambda x: chooseData(x, 'longitude'))
    a['ID'] = a['stations'].apply(lambda x: chooseData(x, 'id'))
    a['Number'] = a['stations'].apply(lambda x: chooseData(x, 'number'))
    a['Address'] = a['stations'].apply(lambda x: chooseData(x, 'address'))
    a['Date'] = pd.to_datetime(a['_id'], format='%Y-%m-%dT%H:%M:%S')
    a = a.drop(['stations', '_id'], axis=1)
    return pd.pivot(a, index='Date', columns='ID')


def saveInPickle(df, path):
    df.to_pickle(path)
