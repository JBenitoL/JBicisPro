from bs4 import BeautifulSoup
import re
import urllib.request as request
import logging
import boto3

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

DATA_URL = "https://opendata.emtmadrid.es/Datos-estaticos/Datos-generales-(1)"

s3_cli = boto3.client('s3')
BUCKET = 'bicimad-project'

def loadControlFile(cli, bucket, key):

    path_column = 1
    paths_saved = []
    response = s3_cli.get_object(
        Bucket=bucket,
        Key=key
    )

    lines = response['Body'].read().decode('utf-8').split('\n')
    for line in lines[1:]:
        content = line.split(',')
        paths_saved.append(content[path_column])
    return paths_saved
    

def createFile(bucket, key):
    headers = 'timestamp,path,file'
    s3_cli.put_object(
        Body=headers.encode('utf-8'),
        Bucket=bucket,
        Key=key
    )

def getLinks():
    html_page = request.urlopen(DATA_URL)
    soup = BeautifulSoup(html_page, features="html.parser")
    links = []
    # print(soup)
    for link in soup.findAll('a', attrs={'href': re.compile("/get")}):
        links.append(link.get('href'))
    return filterStations(links)

def filterStations(links):
    filtered = []
    for link in links:
        if ('Stations' in link) | ('Estacions' in link) | ('stations' in link):
            filtered.append(link)
    return filtered


def checkNewStations(downloaded_stations, all_stations):
    for station in all_stations:
        if station in downloaded_stations:
            logger.info("{} found in control csv".format(station))
        else:
            logger.info("New file {} founded. Downloading...")
            downloadData(station)



if __name__ == '__main__':
    logger.addHandler(logging.StreamHandler())

    links = getLinks()
    downloaded = loadControlFile(s3_cli, BUCKET, 'Control/stations.csv')

    checkNewStations(downloaded, links)
    #print(links)
    #print(downloaded)