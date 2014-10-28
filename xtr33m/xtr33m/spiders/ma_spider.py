from scrapy.spider import Spider
from scrapy.http import Request
from xtr33m.items import band_item
from bs4 import BeautifulSoup
import string
import time
import json

START_URL_FMT = 'http://www.metal-archives.com/browse/ajax-letter/l/{}/json/1?sEcho=1&iColumns=4&sColumns=&iDisplayStart=0&iDisplayLength=500&mDataProp_0=0&mDataProp_1=1&mDataProp_2=2&mDataProp_3=3&iSortCol_0=0&sSortDir_0=asc&iSortingCols=1&bSortable_0=true&bSortable_1=true&bSortable_2=true&bSortable_3=false&_={}'
NEXT_URL_FMT = 'http://www.metal-archives.com/browse/ajax-letter/l/{}/json/1?sEcho=1&iColumns=4&sColumns=&iDisplayStart={}&iDisplayLength=500&mDataProp_0=0&mDataProp_1=1&mDataProp_2=2&mDataProp_3=3&iSortCol_0=0&sSortDir_0=asc&iSortingCols=1&bSortable_0=true&bSortable_1=true&bSortable_2=true&bSortable_3=false&_={}'

class ma_spider(Spider):
    name = "ma"
    allowed_domains = ["www.metal-archives.com"]

    def start_requests(self):
        #letters = ['NBR']+list(string.uppercase)
        letters = ['J']
        #for letter in letters:
        #    #passing in the letter and the time into the url
        #    url = START_URL_FMT.format(letter,int(time.time()))
        #    #using this for the next url format
        #    meta = {'letter': letter}
        #    yield Request(url,callback=self.parse_json,meta=meta)
        for letter in letters:
            #passing in the letter and the time into the url
            url = START_URL_FMT.format(letter,int(time.time()))
            #using this for the next url format
            meta = {'letter': letter}
            yield Request(url,callback=self.parse_first,meta=meta)


    def parse_first(self, response):
        jsonresponse = json.loads(response.body)
        total = jsonresponse['iTotalRecords']
        display = 500
        current = 0
        #if total > display:
        #   remain = total - display
        #   while current < remain:
        #       # yield requests with..
        #       current += display
        #       url = NEXT_URL_FMT.format(response.meta['letter'], current, int(time.time()))
        #       print url
        #       yield Request(url, callback=self.parse_json)
        for i in range(0,total,500):
            url = NEXT_URL_FMT.format(response.meta['letter'], i, int(time.time()))
            print url
            yield Request(url, callback=self.parse_json)


    def parse_json(self,response):
        jsonresponse = json.loads(response.body)
        for item in range(0,len(jsonresponse["aaData"])):
            soup = BeautifulSoup(jsonresponse["aaData"][item][0])
            band_link = soup.select('a')[0]['href']
            print 'yielding %s: ' % band_link
            print Request(band_link,callback=self.parse_band)
            yield Request(band_link,callback=self.parse_band)

    def parse_band(self,response):
        soup = BeautifulSoup(response.body)
        item = band_item()

        band_name = soup.select('.band_name')[0].text
        print band_name
        band_id = response.url.split('/')[-1]
        country = soup.select('#band_stats dd')[0].text
        location = soup.select('#band_stats dd')[1].text
        status = soup.select('#band_stats dd')[2].text
        formation = soup.select('#band_stats dd')[3].text
        genre = soup.select('#band_stats dd')[4].text
        lyrical_themes = soup.select('#band_stats dd')[5].text
        current_label = soup.select('#band_stats dd')[6].text
        years_active = soup.select('#band_stats dd')[7].text
        years_active = ''.join([c for c in years_active if c not in '\n\t '])
        item['name'] = band_name
        item['id'] = band_id
        item['country'] =country
        item['location'] = location
        item['status'] = status
        item['formation_year'] = formation
        item['genre'] = genre
        item['lyrical_themes'] =lyrical_themes
        item['current_label'] = current_label
        item['years_active'] = years_active
        print 'printing the item: %s: ' % item
        yield item

        #Need to figure out how to nest items
        #if soup.find(id='band_tab_members_all') is not None:
        #    #All of the role info is a sibling to the band member itself
        #    #complete linup
        #    lineup = soup.select('#band_tab_members_all .lineupRow td a')
        #    roles = soup.select('.lineupRow td ~ td')
        #    for member,role, in zip(lineup,roles):
        #        band_member = member.text+' - '+role.text.strip()
        #    #current linup
        #    lineup = soup.select('#band_tab_members_current .lineupRow td a')
        #    roles = soup.select('.lineupRow td ~ td')
        #    for member,role, in zip(lineup,roles):
        #        band_member = member.text+' - '+role.text.strip()
        #    #past lineup
        #    lineup = soup.select('#band_tab_members_past .lineupRow td a')
        #    roles = soup.select('.lineupRow td ~ td')
        #    for member,role, in zip(lineup,roles):
        #        band_member = member.text+' - '+role.text.strip()
        #    #live lineup
        #    lineup = soup.select('#band_tab_members_live .lineupRow td a')
        #    roles = soup.select('.lineupRow td ~ td')
        #    for member,role, in zip(lineup,roles):
        #        band_member = member.text+' - '+role.text.strip()

    def parse_description(self,response):
        pass
    def parse_similar_artists(self,response):
        pass
    def parse_all_release(self,response):
        pass
    def parse_other_release(self,response):
        pass
    def parse_lyrics(self,response):
        pass
    def parse_related_lnks(self,response):
        pass
