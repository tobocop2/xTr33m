import collections
import requests
import os
from bs4 import BeautifulSoup

#This function gets the json for every letter band on The Metal Archives. Each json request returns a list of 500 bands.
#Every list is paired with a key representing the letter
#Once every list of bands is retrieved for the letter, the process is repeated for bands #-Z
#The result in the form: 'letter': [[list of bands],[list of bands]....]
def build_band_list():
    result = {}
    #letters = ['NBR','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    letters = ['NBR']
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

def get_band_info():
    result = build_band_list()

    for letter in result:
        try:
            os.makedirs(letter)
        except OSError:
            if not os.path.isdir(letter):
                raise
        for band_list in result[letter]:
            for i in range (0,len(band_list)):
                soup = BeautifulSoup((band_list[i][0]))
                band_name = soup.get_text()
                print band_name
                for child in soup.findAll('a'):
                    link = child.get('href')
                    print link
                    file_name = os.path.join(letter+'/', str(band_name)+".html")
                    band_file = open(file_name, "w")
                    to_file = requests.get(link).content
                    band_file.write(to_file)
                    band_file.close()

get_band_info()
