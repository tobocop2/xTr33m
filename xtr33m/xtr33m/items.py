# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class band_item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    id = scrapy.Field()
    description = scrapy.Field()
    country = scrapy.field()
    location = scrapy.field()
    status = scrapy.field()
    formation_year = scrapy.field()
    genre = scrapy.field()
    current_label = scrapy.field()
    years_active = scrapy.field()
    complete_lineup = scrapy.field()
    current_lineup = scrapy.field()
    past_lineup = scrapy.field()
    live_lineup = scrapy.field()
    official_links = scrapy.field()
    official_merch = scrapy.field()
    unofficial_links= scrapy.field()
    band_label_links = scrapy.field()
    band_tabs = scrapy.field()
    similar_artists = scrapy.field()
    #{releases: {'all': name: {tracks: {track_name,tracknum_length,lyrics} ,type,year,notes,{album_lineup: name,role}
    releases = scrapy.field()



