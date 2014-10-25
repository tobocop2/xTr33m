import scrapy
import json
from xtr33m.items import band_item
from bs4 import BeautifulSoup

class ma_spider(scrapy.Spider):
    name = "ma"
    allowed_domains = ["www.metal-archives.com"]
    start_urls = ['http://www.metal-archives.com/browse/ajax-letter/l/NBR/json/1?sEcho=1&iColumns=4&sColumns=&iDisplayStart=0&iDisplayLength=500&mDataProp_0=0&mDataProp_1=1&mDataProp_2=2&mDataProp_3=3&iSortCol_0=0&sSortDir_0=asc&iSortingCols=1&bSortable_0=true&bSortable_1=true&bSortable_2=true&bSortable_3=false&_=1414220342814']

    def parse(self, response):
        jsonresponse = json.loads(response.body)
        soup = BeautifulSoup(jsonresponse["aaData"][0][0])
        for item in range(0,len(jsonresponse["aaData"])):
            soup = BeautifulSoup(jsonresponse["aaData"][item][0])
            band_link = soup.select('a')[0]['href']
            print 'yielding %s: ' % band_link
            print scrapy.Request(band_link,callback=self.parse_band)
            yield scrapy.Request(band_link,callback=self.parse_band)

    def parse_band(self,response):
        print 'asdf'
        soup = BeautifulSoup(response.body)
        item = band_item()

        band_name = soup.select('.band_name')[0].text
        band_id = response.url.split('/')[-1]
        country = soup.select('#band_stats dd:nth-of-type(1) a')[0].text
        location = soup.select('#band_stats dd:nth-of-type(2)')[0].text
        status = soup.select('#band_stats dd:nth-of-type(3)')[0].text
        formation = soup.select('#band_stats dd:nth-of-type(4)')[0].text
        genre = soup.select('#band_stats dd:nth-of-type(5)')[0].text
        lyrical_themes = soup.select('#band_stats dd:nth-of-type(6)')[0].text
        current_label = soup.select('#band_stats dd:nth-of-type(7)')[0].text
        years_active = soup.select('#band_stats dd:nth-of-type(8)')[0].text
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
