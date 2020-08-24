from bs4 import BeautifulSoup
import re
import urllib.request as request

DATA_URL = "https://opendata.emtmadrid.es/Datos-estaticos/Datos-generales-(1)"

def loadControlFile(cli, bucket, key):

    path_column = 1
    paths_saved = []
    response = cli.get_object(
        Bucket=bucket,
        Key=key
    )

    lines = response['Body'].read().decode('utf-8').split('\n')
    for line in lines[1:]:
        content = line.split(',')
        paths_saved.append(content[path_column])
    return paths_saved
    

def createFile(cli, bucket, key):
    headers = 'timestamp,path,file'
    cli.put_object(
        Body=headers.encode('utf-8'),
        Bucket=bucket,
        Key=key
    )

def getLinks():
    html_page = request.urlopen(DATA_URL)
    soup = BeautifulSoup(html_page)
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


def checkNewStations

if __name__ == '__main__':

    links = getLinks()
    print(len(links))
    print(links)