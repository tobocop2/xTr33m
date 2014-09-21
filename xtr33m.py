import collections
import requests
import os
from bs4 import BeautifulSoup

#This function gets the json for every letter band on The Metal Archives. Each json request returns a list of 500 bands.
#Every list is paired with a key representing the letter
#Once every list of bands is retrieved for the letter, the process is repeated for bands #-Z
#The result in the form: {'letter': [[list of bands],[list of bands]....]}
def build_band_list():
    result = {}
    #letters = ['NBR','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    letters = ['Q']
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
                        result[letters[index]].append(resp.json()[key])
                        print "getting bands for letter: %s" % letters[index]
                    count += 500
                else:
                    letters.remove(letters[index])
                    count = 0
    return result

#This function goes through the all of the bands on the Archives #-Z and gets information from each band page
#The information is stored in this form "Letter/Band/bandinfo.html"
#A map of bands with their respective links is then generated
def get_band_info():
    result = build_band_list()
    band_map = {}

    for letter in result:
        for band_list in result[letter]:
            for i in range (0,len(band_list)):
                soup = BeautifulSoup((band_list[i][0]))
                band_name = soup.get_text()
                print band_name
                if band_name.find('/'):
                    band_name = band_name.replace('/','%slash%')
                for child in soup.findAll('a'):
                    link = child.get('href')
                    print link
                    if not band_map.has_key(band_name):
                        band_map[band_name] = [link]
                    else:
                        band_map[band_name].append(link)

                    write_band_info(letter,band_name,link)

    for band in band_map:
        for link in band_map[band]:
            print band+'\n'+link+'\n'

#This function takes the information from get_band_info() and dumps the html from each band page.
#The structure of the 'Extreme Archives' will be heavily influenced by the metal-archives
def write_band_info(letter,band_name,link):
    band_id = link.split('\\')[5]
    band_folder = band_name+'-'+band_id

    try:
        os.makedirs(letter)
    except OSError:
        if not os.path.isdir(letter):
            raise
    try:
        os.chdir(letter)
        if not os.path.exists(band_folder):
            os.makedirs(band_folder)

        band_page ='http://www.metal-archives.com/bands/%s/%s' % (band_name,band_id)
        releases  = 'http://www.metal-archives.com/band/discography/id/%s/tab/all' % band_id
        similar_artists  = 'http://www.metal-archives.com/band/ajax-recommendations/id/%s' % band_id

        file1 = os.path.join('/', "%s-%s.html" % (band_name,band_id))
        page_file = open(file1, "w")
        to_file1 = requests.get(band_page).content
        page_file.write(to_file1)
        page_file.close()

        file2 = os.path.join('/', "%s-%s-releases.html" % (band_name,band_id))
        releases_file = open(file2, "w")
        to_file2 = requests.get(releases).content
        releases_file.write(to_file1)
        releases_file.close()
        #need to get albums, singles, demos, and other
        for release in soup.find_all(class_=['demo','album','single','other']):
            print release.get('href')


        file3 = os.path.join('/', "%s-%s-similar-artists.html" % (band_name,band_id))
        sa_file = open(file2, "w")
        to_file3 = requests.get(similar_artists).content
        sa_file.write(to_file1)
        sa_file.close()

    except OSError:
        if not os.path.isdir(band_folder):
            raise

if __name__ == '__main__':
    get_band_info()
