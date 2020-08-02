# UpdateFiles() does:
# ---For new links not saved in a text file:
# ----Download rar file to ../Raw/{Stations or Tracks}/
# ----Unrar to obtain json file in same folder
# ----Write in text file, link is downlaoded. Text file is located in ../Raw
# ----Open json to pandas clean and formatting
# ----Save it in ../DataFrames/{Stations or Tracks}/ as pickle
# ----Write the name file located in ../DataFrames/{Stations or Tracks}/


import pandas as pd
import numpy as np
import InfoTrayectosModule as Tracks
import InfoStationsModule as Stations
from bs4 import BeautifulSoup
import urllib.request as request
import re
import requests


def updateFiles():
    links = getLinks()
    for link in links:
        if not (alreadyDownloaded(link)):
            print(link + " is downloading.....")
            filePath = downloadAndSave(link)
            writeToDownloadedList(link)
            print(link + " is downloaded")

            if isTracks(link):
                Tracks.getCleanDataframe(filePath)
                writeToPickleTrackList(link.split("/")[-1].split(".")[0])

            if isStations(link):
                Stations.getCleanDataframe(filePath)
                writeToPickleStationsList(link.split("/")[-1].split(".")[0])

        else:
            print(link + " is already saved")


def getLinks():
    html_page = request.urlopen(
        "https://opendata.emtmadrid.es/Datos-estaticos/Datos-generales-(1)")
    soup = BeautifulSoup(html_page)
    links = []
    # print(soup)
    for link in soup.findAll('a', attrs={'href': re.compile("/get")}):
        links.append(link.get('href'))
    return links


def writeToDownloadedList(link):
    f = open("../Raw/DownloadedFiles.txt", "a")
    f.writelines("\n" + link)
    f.close()
    return 0


def writeToPickleTrackList(link):
    f = open("../DataFrames/Tracks/PickleIndex.txt", "a")
    f.writelines("\n" + link)
    f.close()
    return 0


def writeToPickleStationsList(link):
    f = open("../DataFrames/Stations/PickleIndex.txt", "a")
    f.writelines("\n" + link)
    f.close()
    return 0


def alreadyDownloaded(link):
    f = open("../Raw/DownloadedFiles.txt", "r")
    saved = f.read()
    if link in saved:
        return True
    else:
        return False
    f.close()


def downloadAndSave(link):
    url = "https://opendata.emtmadrid.es" + link
    r = requests.get(url, allow_redirects=True)
    if isStations(link):
        folder = "../"+"Raw/"+"Stations/"
        open(folder + url.split("/")[-1].split(".")
             [0] + ".rar", 'wb').write(r.content)
        return folder + url.split("/")[-1].split(".")[0] + ".rar"

    if isTracks(link):
        folder = "../"+"Raw/"+"Tracks/"
        open(folder + url.split("/")[-1].split(".")
             [0] + ".rar", 'wb').write(r.content)
        return folder + url.split("/")[-1].split(".")[0] + ".rar"

    return 0


def isStations(link):
    if ('Stations' in link) | ('Estacions' in link) | ('stations' in link):
        return True
    else:
        return False


def isTracks(link):
    if ('Usage' in link) | ('movements' in link):
        return True
    else:
        return False
