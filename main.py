import requesocks as requests
from bs4 import BeautifulSoup
import sys, os, time, re


proxies = {
	"http": "socks5://192.168.11.100:3128"
  }

def main():

    page_num = 1
    max_id = get_max_id()
    while 1:
        is_end = search_list('http://sukebei.nyaa.se/?offset=%d' % page_num, max_id)

        if is_end is True:
            page_num = 1
            max_id = get_max_id()
            time.sleep(600)
        else:
            page_num = page_num + 1
            time.sleep(10)

        


def search_list(url, max_id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36'
    }
    result = requests.get(url, headers=headers, proxies=proxies)
    result.encoding = 'utf-8'

    print url, result.status_code, result.headers['date']

    soup = BeautifulSoup(result.text)

    keywords = load_keywords()
    last_num_reg = re.compile('\\d+$')
    is_end = False
    new_max_id = max_id

    for link in soup.select('.tlistname a'):
        link_id = int(last_num_reg.findall(link['href'])[0])
        if link_id > max_id: 
            for key in keywords:
                if key in link.text:
                    filename = '/Users/himmel/Downloads/torrent/' + link.text.replace("/", "").replace(" ", "") + '.torrent'
                    if not os.path.isfile(filename):
                        download_torrent(link['href'], filename)
			time.sleep(5)
        if link_id < max_id:
            is_end = True
        if link_id > new_max_id:
            new_max_id = link_id

    if new_max_id > get_max_id(): 
        set_max_id(new_max_id)

    return is_end

def load_keywords():
    keywords = list()

    with open('keywords') as keyword_file:
        keywords = keyword_file.read().splitlines()

    keywords = [key.decode('utf8') for key in keywords]
    return keywords


def download_torrent(url, filename):
    result = requests.get(url, proxies=proxies)
    result.encoding = 'utf-8'

    soup = BeautifulSoup(result.text)

    download_link = soup.select('.viewdownloadbutton a')[0]['href']

    torrent_file = requests.get(download_link, proxies=proxies)
    with open(filename, 'wb') as torrent:
        torrent.write(torrent_file.content)
        torrent.close()
    print filename

def get_max_id():
    with open('max_id') as max_id_file:
        max_id = max_id_file.read()
    return int(max_id)

def set_max_id(max_id):
    with open('max_id', 'wb') as max_id_file:
        max_id_file.write(str(max_id))
        max_id_file.close()

main()
