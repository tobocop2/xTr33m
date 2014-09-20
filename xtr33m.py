import collections
import requests
from bs4 import BeautifulSoup

#This function gets the json for every letter band on The Metal Archives. Each json request returns a list of 500 bands. Every list is paired with a key representing the letter
#Once every list of bands is retrieved for the letter, the process is repeated for bands #-Z
#The result in the form: 'letter': [[list of bands],[list of bands]....]
def get_all_bands():
    result = {}
    letters = ['NBR','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    index = 0
    count = 0

    while len(letters) > 0:
        resp = requests.get('http://www.metal-archives.com/browse/ajax-letter/l/'+letters[index]+'/json/1?sEcho=1&iColumns=4&sColumns=&iDisplayStart='+str(count)+'&iDisplayLength=&mDataProp_0=0&mDataProp_1=1&mDataProp_2=2&mDataProp_3=3&iSortCol_0=0&sSortDir_0=asc&iSortingCols=1&bSortable_0=true&bSortable_1=true&bSortable_2=true&bSortable_3=false&_=1410751488887')
        for key in resp.json():
            if isinstance(resp.json()[key],collections.Iterable):
                if len(resp.json()[key]) > 0:
                    if not result.has_key(letters[index]):
                        print "getting bands for letter: %s" % letters[index]
                        result[letters[index]] = [resp.json()[key]]
                    else:
                        result[letters[index]].append([resp.json()[key]])
                        print "getting bands for letter: %s" % letters[index]
                    count += 500
                else:
                    letters.remove(letters[index])
                    count = 0

    return result
'''
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
'''
result = get_all_bands()
print result


