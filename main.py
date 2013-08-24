import requests
from bs4 import BeautifulSoup
import sys, os, time


def main():
    result = requests.get('http://sukebei.nyaa.se/')

    print result.status_code, result.headers['date']

    result.encoding = 'utf-8'

    soup = BeautifulSoup(result.text)

    keywords = load_keywords()

    for link in soup.select('.tlistname a'):
        for key in keywords:
            if key in link.text: 
                filename = 'torrents/' + link.text + '.torrent'
                if not os.path.isfile(filename):
                    download_torrent(link['href'], filename)

def load_keywords():
    keywords = list()

    with open('keywords') as keyword_file:
        keywords = keyword_file.read().splitlines()

    keywords = [key.decode('utf8') for key in keywords]

    return keywords


def download_torrent(url, filename):
    result = requests.get(url)
    result.encoding = 'utf-8'

    soup = BeautifulSoup(result.text)

    download_link = soup.select('.viewdownloadbutton a')[0]['href']

    torrent_file = requests.get(download_link)

    output = open(filename,'wb')
    output.write(torrent_file.content)
    output.close()
    print filename


while 1:
    main()
    time.sleep(10)