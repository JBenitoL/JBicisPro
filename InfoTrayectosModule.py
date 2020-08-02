# Funciones para obtener el dataframe de la info sobre los trayectos.
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
    df = cleanJsonformat(df)
    df = dateFormatting(df)
    # SaveInPickle in new folder where rest of dataframes are
    saveInPickle(df, "../DataFrames/Tracks/" +
                 filePath.split("/")[-1].split(".")[0]+".pkl")
    return 0


def getRawDataFrame(filePath):
    df = pd.read_json(filePath, orient='records',
                      lines=True, encoding="ISO 8859-1")
    return df


def cleanJsonformat(df):
    df['_id'] = df['_id'].apply(lambda x: x['$oid'])
    if type(df['unplug_hourTime'][0]) == dict:
        df['unplug_hourTime'] = df['unplug_hourTime'].apply(
            lambda x: x['$date'])

    return df


def dateFormatting(df):
    df['unplug_hourTime'] = pd.to_datetime(
        df['unplug_hourTime'], format='%Y-%m-%dT%H:%M:%S')
    df["unplug_date"] = df["unplug_hourTime"].dt.date
    df["unplug_time"] = df["unplug_hourTime"].dt.time
    df["unplug_dayOfWeek"] = df["unplug_hourTime"].dt.dayofweek

    return df


def saveInPickle(df, path):
    df.to_pickle(path)
