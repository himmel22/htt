import requesocks as requests
from bs4 import BeautifulSoup
import sys, os, time, re


proxies = {
	"https": "socks5://192.168.1.1:1234"
  }

def main():

    page_num = 1
    max_id = get_max_id()
    while 1:
        is_end = search_list('https://share.dmhy.org/topics/list/page/%d' % page_num, max_id)

        if is_end is True:
            page_num = 1
            max_id = get_max_id()
            print 'All done. Sleeping for 600s.'
            time.sleep(600)
        else:
            page_num = page_num + 1
            time.sleep(10)

        


def search_list(url, max_id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36'
    }
    try:
        result = requests.get(url, headers=headers, proxies=proxies)
    except Exception, e:
        print e
        return False
    else:
        result.encoding = 'utf-8'

        print url, result.status_code, result.headers['date']

        soup = BeautifulSoup(result.text, 'lxml')

        keywords = load_keywords()
        last_num_reg = re.compile('view/(\d+)_')
        is_end = False
        new_max_id = max_id

        for link in soup.select('#topic_list .title > a'):
            link_id = int(last_num_reg.findall(link['href'])[0])
            if link_id > max_id: 
                for key in keywords:
                    if key in link.text:
                        print key + ' hit'
                        dirname = '/mnt/c/Users/himmelmk10/Downloads/torrent/' + key.strip().replace("/", "")
                        if not os.path.exists(dirname):
                            os.makedirs(dirname)
			print link.text.strip()
                        filename = dirname + '/' + link.text.strip().replace("/", "") + '.torrent'
                        if not os.path.isfile(filename):
                            download_torrent('https://share.dmhy.org/' + link['href'], filename)
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
    try:
        result = requests.get(url, proxies=proxies)
        result.encoding = 'utf-8'
    except Exception, e:
        print e
        pass
    else:
        soup = BeautifulSoup(result.text, 'lxml')
        download_link = 'https:' + soup.select('#tabs-1 > p:nth-of-type(1) > a')[0]['href']
        try:
            torrent_file = requests.get(download_link, proxies=proxies)
        except Exception, e:
            print e
            pass
        else:
            with open(filename, 'wb') as torrent:
                torrent.write(torrent_file.content)
                torrent.close()
            print 'Saved!'
        
def get_max_id():
    with open('max_id') as max_id_file:
        max_id = max_id_file.read()
    return int(max_id)

def set_max_id(max_id):
    with open('max_id', 'wb') as max_id_file:
        max_id_file.write(str(max_id))
        max_id_file.close()

main()
