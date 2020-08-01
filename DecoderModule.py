
# Decoder class to translate id to name or viceversa and get tations information.

# Methods:

# -get method:
# Using as input the value (name or id) and the columnName (name of attribute), the desired data is returned.

# -infoStation:
# Using as input the value (name or id), all attributes are returned.

# -generalInfo:
# Helper method, to check names of attributes

# Examples:

# ---Initialize : Decode = Decoder('IndiceBases.xlsx')

# -------------------Decode.get('Lavapiés', 'longitude')

# ------------------------ -3.7008803

# -------------------Decode.generalInfo()

#--------------------------Index(['name', 'total_bases', 'number', 'longitude', 'latitude', 'address'], dtype='object')

# -------------------Decode.infoStation(57)

# -------------------------Index(['name', 'total_bases', 'number', 'longitude', 'latitude', 'address'], dtype='object')
# -------------------------name             Plaza de Lavapiés
# -------------------------total_bases                     24
# -------------------------number                          53
# -------------------------longitude                 -3.70088
# -------------------------latitude                   40.4089
# --------------------------address        Calle Valencia nº 1
# --------------------------Name: 57, dtype: object

import pandas as pd


class Decoder:
    """Class for obtaining basic info of each station"""

    def __init__(self, filePath):
        # import pandas as pd
        self._obj = pd.read_excel(
            filePath,   sep=';', encoding='latin').set_index('id')

    def _index(self, name, ListOfNames):
        for ind in range(0, len(ListOfNames)):
            if name in ListOfNames[ind]:
                return ind

    def get(self, value, columnName):
        if type(value) == int:
            return self._obj.loc[value][columnName]

        if type(value) == str:
            ind = self._index(value, self._obj['name'].to_list())
            return self._obj.reset_index().iloc[ind][columnName]

    def generalInfo(self):
        print(self._obj.columns)

    def infoStation(self, value):

        if type(value) == int:
            return self._obj.loc[value]

        if type(value) == str:

            ind = self._index(value, self._obj['name'].to_list())
            return self._obj.reset_index().iloc[ind]
