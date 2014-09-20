import collections
import requests
from bs4 import BeautifulSoup

def get_all_bands():
    result = {}
    letters = ['NBR','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','X','Y','Z']
    while True:
        for letter in letters:
            count = 0;
            resp = requests.get('http://www.metal-archives.com/browse/ajax-letter/l/'+letter+'/json/1?sEcho=1&iColumns=4&sColumns=&iDisplayStart='+count+'&iDisplayLength=&mDataProp_0=0&mDataProp_1=1&mDataProp_2=2&mDataProp_3=3&iSortCol_0=0&sSortDir_0=asc&iSortingCols=1&bSortable_0=true&bSortable_1=true&bSortable_2=true&bSortable_3=false&_=1410751488887')
            for key in resp.json():
                if isinstance(resp.json()[key],collections.Iterable):
                    if len(response.json()[key] > 0:
                        if not result.has_key(letter):
                            result['letter'] = [resp.json()[key]]
                        else:
                            result['letter'].append([resp.json()[key]]

            count+=500



def map_bands():
    result = {}

    resp = requests.get('http://www.metal-archives.com/browse/ajax-letter/l/A/json/1?sEcho=1&iColumns=4&sColumns=&iDisplayStart='+count+'&iDisplayLength=&mDataProp_0=0&mDataProp_1=1&mDataProp_2=2&mDataProp_3=3&iSortCol_0=0&sSortDir_0=asc&iSortingCols=1&bSortable_0=true&bSortable_1=true&bSortable_2=true&bSortable_3=false&_=1410751488887')
    print len(resp.json()['aaData'])

    for key in resp.json():
        if isinstance(resp.json()[key],collections.Iterable):
            for list in resp.json()[key]:
                print len(list)
                soup = BeautifulSoup(list[0])
                band = soup.get_text()
                #print band
                for child in soup.findAll('a'):
                    link = child.get('href')
                    #result[band] = link

    return result

result = map_bands()
for band in result:
    print band+'\n'+result[band]+'\n\n'
