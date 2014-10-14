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
    letters = ['X']
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

    main_page_path = os.path.join('./', "%s-%s-content.txt" % (band_name,band_id))
    main_page_file = open(main_page_path, "a")
    main_page_file_response = requests.get(band_page).content
    soup = BeautifulSoup(main_page_file_response)

    band_name = soup.select('.band_name')[0].text
    main_page_file.write('Band Name: '+band_name.encode('ascii','ignore')+'\n')
    country = soup.select('#band_stats dd:nth-of-type(1) a')[0].text
    main_page_file.write('Country: '+country.encode('ascii','ignore')+'\n')
    location = soup.select('#band_stats dd:nth-of-type(2)')[0].text
    main_page_file.write('Location: '+country.encode('ascii','ignore')+'\n')
    status = soup.select('#band_stats dd:nth-of-type(3)')[0].text
    main_page_file.write('Status: '+status.encode('ascii','ignore')+'\n')
    formation = soup.select('#band_stats dd:nth-of-type(4)')[0].text
    main_page_file.write('Formation: '+formation.encode('ascii','ignore')+'\n')
    genre = soup.select('#band_stats dd:nth-of-type(5)')[0].text
    main_page_file.write('Genre: '+genre.encode('ascii','ignore')+'\n')
    lyrical_themes = soup.select('#band_stats dd:nth-of-type(6)')[0].text
    main_page_file.write('Lyrical Themes: '+lyrical_themes.encode('ascii','ignore')+'\n')
    current_label = soup.select('#band_stats dd:nth-of-type(7)')[0].text
    main_page_file.write('Current Label: '+current_label.encode('ascii','ignore')+'\n')
    years_active = soup.select('#band_stats dd:nth-of-type(8)')[0].text.split()

    main_page_file.write('Years Active: \n')
    for active_info in years_active:
        main_page_file.write(active_info.encode('ascii','ignore')+'\n')

    if soup.find(id='band_tab_members_all') is not None:
        #All of the role info is a sibling to the band member itself
        main_page_file.write('COMPLETE LINEUP:\n')
        lineup = soup.select('#band_tab_members_all .lineupRow td a')
        roles = soup.select('.lineupRow td ~ td')
        for member,role, in zip(lineup,roles):
            band_member = member.text+' - '+role.text.strip()
            main_page_file.write(band_member.encode('ascii','ignore')+'\n')
        main_page_file.write('CURRENT LINEUP:\n')
        lineup = soup.select('#band_tab_members_current .lineupRow td a')
        roles = soup.select('.lineupRow td ~ td')
        for member,role, in zip(lineup,roles):
            band_member = member.text+' - '+role.text.strip()
            main_page_file.write(band_member.encode('ascii','ignore')+'\n')
        main_page_file.write('PAST LINEUP:\n')
        lineup = soup.select('#band_tab_members_past .lineupRow td a')
        roles = soup.select('.lineupRow td ~ td')
        for member,role, in zip(lineup,roles):
            band_member = member.text+' - '+role.text.strip()
            main_page_file.write(band_member.encode('ascii','ignore')+'\n')
        main_page_file.write('LIVE LINEUP:\n')
        lineup = soup.select('#band_tab_members_live .lineupRow td a')
        roles = soup.select('.lineupRow td ~ td')
        for member,role, in zip(lineup,roles):
            band_member = member.text+' - '+role.text.strip()
            main_page_file.write(band_member.encode('ascii','ignore')+'\n')
    main_page_file.close()

def write_band_description(band_name,band_id):
        band_description = 'http://www.metal-archives.com/band/read-more/id/%s' % band_id
        #Band Description
        band_description_path = os.path.join('./',"%s-%s-Description" % (band_name,band_id))
        description_file = open(band_description_path,"w")
        description_response = requests.get(band_description).content
        soup = BeautifulSoup(description_response)
        for description in soup.find_all(text=True):
            band_description = description.strip()
            description_file.write(band_description.encode('ascii','ignore')+'\n')
        description_file.close()

def write_similar_artists(band_name,band_id):
    similar_artists = 'http://www.metal-archives.com/band/ajax-recommendations/id/%s/showMoreSimilar/1' % band_id

    similar_artist_path = os.path.join('./', "%s-%s-similar-artists.txt" % (band_name,band_id))
    similar_artist_file = open(similar_artist_path, "a")
    similar_artist_response = requests.get(similar_artists).content
    soup = BeautifulSoup(similar_artist_response)
    similar_artist_list = [child.text for child in soup.find_all('td') if not child.has_attr('colspan') and not child.find_all('span')]
    #may want to do this differently
    bands = similar_artist_list[0:len(similar_artist_list):3]
    countries = similar_artist_list[1:len(similar_artist_list):3]
    genres = similar_artist_list[2:len(similar_artist_list):3]
    for band,country,genre in zip(bands,countries,genres):
        similar_artist_file.write('%s - %s - %s\n' % (band.encode('ascii','ignore'),country,genre))
    similar_artist_file.close()

def write_related_links(band_name,band_id):
    related_link_url = 'http://www.metal-archives.com/link/ajax-list/type/band/id/%s' % band_id
    related_link_resp = requests.get(related_link_url).content
    related_links_path = os.path.join('./', "%s-%s-related links.txt" % (band_name,band_id))
    related_links_file = open(related_links_path, "a")
    soup = BeautifulSoup(related_link_resp)
    related_links_file.write('OFFICIAL BAND LINKS\n')
    for child in soup.select('#band_links_Official a'):
        related_links_file.write('%s - %s\n' % (child.text.encode('ascii','ignore'),child['href'].encode('ascii','ignore')))
    related_links_file.write('OFFICIAL MERCH\n')
    for child in soup.select('#band_links_Official_merchandise a'):
        related_links_file.write('%s - %s\n' % (child.text.encode('ascii','ignore'),child['href'].encode('ascii','ignore')))
    related_links_file.write('UNOFFICIAL MERCH\n')
    for child in soup.select('#band_links_Unofficial a'):
        related_links_file.write('%s - %s\n' % (child.text.encode('ascii','ignore'),child['href'].encode('ascii','ignore')))
    related_links_file.write('BAND LABELS\n')
    for child in soup.select('#band_links_Labels a'):
        related_links_file.write('%s - %s\n' % (child.text.encode('ascii','ignore'),child['href'].encode('ascii','ignore')))
    related_links_file.write('BAND TABS\n')
    for child in soup.select('#band_links_Tablatures a'):
        related_links_file.write('%s - %s\n' % (child.text.encode('ascii','ignore'),child['href'].encode('ascii','ignore')))

def write_release_info(band_name,band_id,all_releases):
    release_resp = requests.get(all_releases).content
    soup = BeautifulSoup(release_resp)

    try:
        release_dir = 'Releases'
        os.makedirs(release_dir)
    except OSError:
        if not os.path.isdir(release_dir):
            raise

    os.chdir(release_dir)
    for release in soup.find_all('a',class_=['demo','album','single','other']):
        release_name = release.get_text().replace('/','\\')
        release_url = release.get('href')
        release_id = release_url.split('/')[6]
        full_release_name = '%s - %s' % (release_name,release_id)

        try:
            release_name_dir = full_release_name
            os.makedirs(release_name_dir)
        except OSError:
            if not os.path.isdir(release_name_dir):
                raise
        os.chdir(release_name_dir)

        print "Getting %s: %s\n" % (band_name,release_name)
        individual_release_path = os.path.join('./', full_release_name+'.txt')
        individual_release_file = open(individual_release_path, "a")
        release_response = requests.get(release_url).content
        soup = BeautifulSoup(release_response)
        track_count = 0
        #Getting lyrics and track info
        for child in soup.find_all('tbody'):
            for tracks in child.find_all(class_=['odd','even']):
                for track in tracks.select('.wrapWords'):
                    track_count += 1
                    track_name = track.text.strip().encode('ascii','ignore').replace('/','-')
                    track_length = track.next_sibling.next_sibling.text
                    individual_release_file.write('%s - %s - %s\n' % (str(track_count),track_name.encode('ascii','ignore'),track_length))
                    lyrics_tag = track.next_sibling.next_sibling.next_sibling.next_sibling.find_all(href=True)
                    write_lyrics(track_name,lyrics_tag)

        individual_release_file.write('\nALBUM LINEUP\n')
        band_members = soup.select('#album_members_lineup .lineupRow td a')
        member_roles = soup.select('.lineupRow td ~ td')
        for member,role, in zip(band_members,member_roles):
            band_member = member.text+' - '+role.text.strip()
            individual_release_file.write(band_member.encode('ascii','ignore')+'\n')

        individual_release_file.write('\nALBUM NOTES\n')
        for notes in soup.select('#album_tabs_notes'):
            individual_release_file.write(notes.text.strip().encode('ascii','ignore')+'\n')

        os.chdir('../')

def write_lyrics(track_name,lyrics_tag):
    lyrics_base_url = 'http://www.metal-archives.com/release/ajax-view-lyrics/id/'

    try:
        lyrics_dir = 'lyrics'
        os.makedirs(lyrics_dir)
    except OSError:
        if not os.path.isdir(lyrics_dir):
            raise

    os.chdir(lyrics_dir)
    if len(lyrics_tag) > 0:
        lyrics_path = os.path.join('./', track_name+'.txt')
        lyrics_file = open(lyrics_path, "w")
        lyrics_url_value = lyrics_tag[0].get('href')
        lyrics_id = ''.join([char for char in lyrics_url_value if char.isdigit()])
        lyrics_url = lyrics_base_url+lyrics_id
        lyrics_resp = requests.get(lyrics_url).content
        soup = BeautifulSoup(lyrics_resp)
        lyrics_file.write(soup.text.encode('ascii','ignore'))
        lyrics_file.close()
    os.chdir('../')

def write_all_releases(band_name,band_id):
    all_releases  = 'http://www.metal-archives.com/band/discography/id/%s/tab/all' % band_id
    live_releases = 'http://www.metal-archives.com/band/discography/id/%s/tab/lives' % band_id
    demo_releases = 'http://www.metal-archives.com/band/discography/id/%s/tab/demos' % band_id
    misc_releases = 'http://www.metal-archives.com/band/discography/id/%s/tab/misc' % band_id
    main_releases = 'http://www.metal-archives.com/band/discography/id/%s/tab/main' % band_id

    release_resp = requests.get(all_releases).content
    release_file_path = os.path.join('./', "%s-%s-releases.txt" % (band_name,band_id))
    releases_file = open(release_file_path, "a")

    soup = BeautifulSoup(release_resp)
    #may want to do this differently
    release_info = [release_value.text for release_value in soup.find_all(class_=['single','demo','album','demo'])]
    release_names = release_info[0:len(release_info):3]
    release_types = release_info[1:len(release_info):3]
    release_years = release_info[2:len(release_info):3]

    releases_file.write('ALL RELEASES\n')
    for release_name,release_type,release_year in zip(release_names,release_types,release_years):
        releases_file.write('Name: %s - Type: %s - Year: %s\n' % (release_name.encode('ascii','ignore'),release_type,release_year))

    releases_file.write('LIVE RELEASES\n')
    write_release_files(releases_file,live_releases)
    releases_file.write('DEMO RELEASES\n')
    write_release_files(releases_file,demo_releases)
    releases_file.write('MISC RELEASES\n')
    write_release_files(releases_file,misc_releases)
    releases_file.write('MAIN RELEASES\n')
    write_release_files(releases_file,main_releases)

    releases_file.close()
    write_release_info(band_name,band_id,all_releases)

def write_release_files(releases_file,releases_url):
    release_resp = requests.get(releases_url).content
    soup = BeautifulSoup(release_resp)
    #below commented code only works for all_releases
    release_info = [child.text.strip() for child in soup.select('tbody td') if '%' not in child.text and len(child.text.strip()) != 0]
    #may want to do this differently
    release_names = release_info[0:len(release_info):3]
    release_types = release_info[1:len(release_info):3]
    release_years = release_info[2:len(release_info):3]
    for release_name,release_type,release_year in zip(release_names,release_types,release_years):
        releases_file.write('Name: %s - Type: %s - Year: %s\n' % (release_name.encode('ascii','ignore'),release_type,release_year))

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
        write_related_links(band_name,band_id)
        write_similar_artists(band_name,band_id)
        write_all_releases(band_name,band_id)

        os.chdir('../../../')
    except OSError:
        if not os.path.isdir(band_folder):
            raise

if __name__ == '__main__':
    get_band_info()
