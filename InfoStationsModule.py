# Funciones para obtener el dataframe de la info sobre las estaciones.
# Esta por ver si esta es la mejor forma.
# Solamente hay que llamar a getCleanDataFrame para tener un dataframe limpio.
# Si hay cosas que veamos qeu se necesiten o sobren del dataframe se añade


import numpy as np
import pandas as pd
from pyunpack import Archive


def getCleanDataframe(filePath):
   # Unzip and save in save folder as .rar
    Archive(filePath).extractall("/".join(filePath.split("/")[0:3]))

    df = getRawDataFrame(filePath[0:-3]+"json")
    df = dateFormatting(df)
    table = rawDatatoTable(df)
    df = finalDataFrame(table)
    # SaveInPickle in new folder where rest of dataframes are
    saveInPickle(df, "../DataFrames/Stations/" +
                 filePath.split("/")[-1].split(".")[0]+".pkl")
    return 0


def getRawDataFrame(filePath):
    df = pd.read_json(filePath, orient='records',
                      lines=True, encoding="ISO 8859-1")
    return df


def dateFormatting(df):
    df['_id'] = pd.to_datetime(df['_id'], format='%Y-%m-%dT%H:%M:%S')

    return df


def rawDatatoTable(df):
    newDf = df.explode('stations')
    indexes = newDf['stations'].apply(lambda x: x['id'])
    table = pd.pivot_table(newDf, values='stations', index=['_id'],
                           columns=indexes, aggfunc=np.sum)
    return table


def chooseData(x, y):

    if type(x) == dict:

        return x[y]
    else:
        return float('NaN')


def finalDataFrame(table):
    Reservation = table.applymap(lambda x: chooseData(x, 'reservations_count'))
    Light = table.applymap(lambda x: chooseData(x, 'light'))
    FreeBases = table.applymap(lambda x: chooseData(x, 'free_bases'))
    no_available = table.applymap(lambda x: chooseData(x, 'no_available'))
    DockBikes = table.applymap(lambda x: chooseData(x, 'dock_bikes'))

    Reservation = Reservation.T
    Light = Light.T
    FreeBases = FreeBases.T
    no_available = no_available.T
    DockBikes = DockBikes.T

    Reservation['Name'] = 'reservations_count'
    Light['Name'] = 'light'
    FreeBases['Name'] = 'free_bases'
    no_available['Name'] = 'no_available'
    DockBikes['Name'] = 'dock_bikes'
    finalDf = pd.concat([Reservation, Light, FreeBases,
                         no_available, DockBikes],  names=['_id', 'Name'])
    finalDf = finalDf.reset_index().set_index(['stations', 'Name'])
    return finalDf


def saveInPickle(df, path):
    df.to_pickle(path)
