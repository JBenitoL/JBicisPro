# Funciones para obtener el dataframe de la info sobre los trayectos.
# Esta por ver si esta es la mejor forma.
# Solamente hay que llamar a getCleanDataFrame para tener un dataframe limpio.
# Si hay cosas que veamos qeu se necesiten o sobren del dataframe se añade


import numpy as np
import pandas as pd


def getCleanDataframe(filePath):
    df = getRawDataFrame(filePath)
    df = cleanJsonformat(df)

    return dateFormatting(df)


def getRawDataFrame(filePath):
    df = pd.read_json(filePath, orient='records',
                      lines=True, encoding="ISO 8859-1")
    return df


def cleanJsonformat(df):
    df['_id'] = df['_id'].apply(lambda x: x['$oid'])
    df['unplug_hourTime'] = df['unplug_hourTime'].apply(lambda x: x['$date'])

    return df


def dateFormatting(df):
    df['unplug_hourTime'] = pd.to_datetime(
        df['unplug_hourTime'], format='%Y-%m-%dT%H:%M:%S')
    return df
