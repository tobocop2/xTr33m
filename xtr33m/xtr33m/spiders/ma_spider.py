import scrapy
from tutorial.items import DmozItem

class ma_spider(scrapy.Spider):
    name = "ma"
    allowed_domains = ["http://www.metal-archives.com"]
    start_urls = []

    def parse_ajax(self, response):
        pass
    def parse_band(self,response):
        pass
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
