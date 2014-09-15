import collections
import requests
from bs4 import BeautifulSoup

def map_bands():
    result = {}

    resp = requests.get('http://www.metal-archives.com/browse/ajax-letter/l/A/json/1?sEcho=1&iColumns=4&sColumns=&iDisplayStart=0&iDisplayLength=500&mDataProp_0=0&mDataProp_1=1&mDataProp_2=2&mDataProp_3=3&iSortCol_0=0&sSortDir_0=asc&iSortingCols=1&bSortable_0=true&bSortable_1=true&bSortable_2=true&bSortable_3=false&_=1410751488887')

    for key in resp.json():
        if isinstance(resp.json()[key],collections.Iterable):
            for list in resp.json()[key]:
                soup = BeautifulSoup(list[0])
                band = soup.get_text()
                print band
                for child in soup.findAll('a'):
                    link = child.get('href')
                    result[band] = link

    return result

result = map_bands()
for band in result:
    print band+'\n'+result[band]+'\n\n'
