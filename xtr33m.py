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
#The information is stored in this form "Letter/Band/bandinfo.txt"
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
                    band_name = band_name.replace('/','\\')
                for child in soup.findAll('a'):
                    link = child.get('href')
                print link
                if not band_map.has_key(band_name):
                    band_map[band_name] = [link]
                else:
                    band_map[band_name].append(link)

                write_all_data(letter,band_name,link)

    for band in band_map:
        for link in band_map[band]:
            print band+'\n'+link+'\n'


def write_band_content(band_name,band_id):
    band_page ='http://www.metal-archives.com/bands/%s/%s' % (band_name,band_id)

    file1 = os.path.join('./', "%s-%s-content.txt" % (band_name,band_id))
    page_file = open(file1, "a")
    page_file_response = requests.get(band_page).content
    soup = BeautifulSoup(page_file_response)

    band_name = soup.select('.band_name')[0].text
    page_file.write('Band Name: '+band_name.encode('ascii','ignore')+'\n')
    country = soup.select('#band_stats dd:nth-of-type(1) a')[0].text
    page_file.write('Country: '+country.encode('ascii','ignore')+'\n')
    location = soup.select('#band_stats dd:nth-of-type(2)')[0].text
    page_file.write('Location: '+country.encode('ascii','ignore')+'\n')
    status = soup.select('#band_stats dd:nth-of-type(3)')[0].text
    page_file.write('Status: '+status.encode('ascii','ignore')+'\n')
    formation = soup.select('#band_stats dd:nth-of-type(4)')[0].text
    page_file.write('Formation: '+formation.encode('ascii','ignore')+'\n')
    genre = soup.select('#band_stats dd:nth-of-type(5)')[0].text
    page_file.write('Genre: '+genre.encode('ascii','ignore')+'\n')
    lyrical_themes = soup.select('#band_stats dd:nth-of-type(6)')[0].text
    page_file.write('Lyrical Themes: '+lyrical_themes.encode('ascii','ignore')+'\n')
    current_label = soup.select('#band_stats dd:nth-of-type(7)')[0].text
    page_file.write('Current Label: '+current_label.encode('ascii','ignore')+'\n')
    years_active = soup.select('#band_stats dd:nth-of-type(8)')[0].text.split()
    page_file.write('Years Active: \n')
    for active_info in years_active:
        page_file.write(active_info.encode('ascii','ignore')+'\n')
    if soup.find(id='band_tab_members_all') is not None:
        #All of the role info is a sibling to the band member itself
        lineup = soup.select('#band_members .lineupRow td a')
        roles = soup.select('.lineupRow td ~ td')
        page_file.write('LINEUP:\n')
        for member,role, in zip(lineup,roles):
            band_member = member.text+' - '+role.text.strip()
            page_file.write(band_member.encode('ascii','ignore')+'\n')
    page_file.close()

def write_band_description(band_name,band_id):
        band_description = 'http://www.metal-archives.com/band/read-more/id/%s' % band_id
        #Band Description
        file0 = os.path.join('./',"%s-%s-Description" % (band_name,band_id))
        description_file = open(file0,"w")
        description_response = requests.get(band_description).content
        soup = BeautifulSoup(description_response)
        for description in soup.find_all(text=True):
            band_description = description.strip()
            description_file.write(band_description.encode('ascii','ignore')+'\n')
        description_file.close()

def write_similar_artists(band_name,band_id):
    similar_artists = 'http://www.metal-archives.com/band/ajax-recommendations/id/%s/showMoreSimilar/1' % band_id

    #similar artists (Name, country of origin, genre)
    file2 = os.path.join('./', "%s-%s-similar-artists.txt" % (band_name,band_id))
    similar_artist_file = open(file2, "a")
    similar_artist_response = requests.get(similar_artists).content
    soup = BeautifulSoup(similar_artist_response)
    for artist  in soup.find_all('tbody'):
        for child in artist.find_all('td'):
            if not child.has_attr('colspan') and not child.find_all('span'):
                print 'Similar artists %s: ' % child.get_text()
                similar_artist_file.write(child.get_text().encode('ascii','ignore')+'\n')
    similar_artist_file.close()

def write_release_info(band_name,band_id):
    releases  = 'http://www.metal-archives.com/band/discography/id/%s/tab/all' % band_id
    lyrics_base_url = 'http://www.metal-archives.com/release/ajax-view-lyrics/id/'

    file3 = os.path.join('./', "%s-%s-releases.txt" % (band_name,band_id))
    releases_file = open(file3, "a")
    release_resp = requests.get(releases).content
    soup = BeautifulSoup(release_resp)
    release_info = [release_value.text for release_value in soup.find_all(class_=['single','demo','album','demo'])]
    #need to do this differently
    for album in release_info:
        release_name = release_info[0]
        release_type = release_info[1]
        release_year = release_info[2]
        releases_file.write('Name: %s - Type: %s - Year: %s\n' % (release_name.encode('ascii','ignore'),release_type,release_year))
        release_info.remove(release_name)
        release_info.remove(release_type)
        release_info.remove(release_year)
    releases_file.close()

    try:
        release_dir = 'Releases'
        os.makedirs(release_dir)
    except OSError:
        if not os.path.isdir(release_dir):
            raise
    os.chdir(release_dir)

    for release in soup.find_all('a',class_=['demo','album','single','other']):
        release_name = release.get_text().replace('/','\\')
        try:
            release_name_dir = release_name
            os.makedirs(release_name_dir)
        except OSError:
            if not os.path.isdir(release_name_dir):
                raise
        os.chdir(release_name_dir)
        print "Getting %s: %s\n" % (band_name,release_name)
        release_url = release.get('href')
        individual_release_path = os.path.join('./', release_name+'.txt')
        individual_release_file = open(individual_release_path, "a")
        release_response = requests.get(release_url).content
        soup = BeautifulSoup(release_response)
        track_count = 0;
        #Getting lyrics and track info
        for child in soup.find_all('tbody'):
            for tracks in child.find_all(class_=['odd','even']):
                #write info and lyrics then change back
                for track in tracks.select('.wrapWords'):
                    track_count += 1;
                    track_name = track.text.strip().encode('ascii','ignore').replace('/','-')
                    track_length = track.next_sibling.next_sibling.text
                    individual_release_file.write('%s - %s - %s\n' % (str(track_count),track_name.encode('ascii','ignore'),track_length))
                    try:
                        lyrics_dir = 'lyrics'
                        os.makedirs(lyrics_dir)
                    except OSError:
                        if not os.path.isdir(lyrics_dir):
                            raise
                    os.chdir(lyrics_dir)
                    #lyrics: for a in track.find_all(href=True):
                    lyrics_tag = track.next_sibling.next_sibling.next_sibling.next_sibling.find_all(href=True)
                    if len(lyrics_tag) > 0:
                        lyrics_path = os.path.join('./', track_name+'.txt')
                        lyrics_file = open(lyrics_path, "w")
                        lyrics_url_value = lyrics_tag[0].get('href')
                        lyrics_id = ''.join([char for char in lyrics_url_value if char.isdigit()])
                        lyrics_url = lyrics_base_url+lyrics_id
                        lyrics_resp = requests.get(lyrics_url).content
                        lyrics_soup = BeautifulSoup(lyrics_resp)
                        for lyrics in lyrics_soup.find_all(text=True):
                            lyrics_file.write(lyrics.strip().encode('ascii','ignore'))
                        lyrics_file.close()
                    os.chdir('../')
        os.chdir('../')

#This function takes the information from get_band_info() and dumps the txt from each band page.
#The structure of the 'Extreme Archives' will be heavily influenced by the metal-archives.
#Need to modulairze different types of requests for future debugging
def write_all_data(letter,band_name,link):
    band_id = link.split('/')[5]
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
        os.chdir(band_folder)

        write_band_content(band_name,band_id)
        write_band_description(band_name,band_id)
        write_similar_artists(band_name,band_id)
        write_release_info(band_name,band_id)

        os.chdir('../../../')
    except OSError:
        if not os.path.isdir(band_folder):
            raise

if __name__ == '__main__':
    get_band_info()
