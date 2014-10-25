# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class band_item(scrapy.Item):
    # define the Fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    id = scrapy.Field()
    link = scrapy.Field
    description = scrapy.Field()
    country = scrapy.Field()
    location = scrapy.Field()
    status = scrapy.Field()
    formation_year = scrapy.Field()
    lyrical_themes = scrapy.Field()
    genre = scrapy.Field()
    current_label = scrapy.Field()
    years_active = scrapy.Field()
    complete_lineup = scrapy.Field()
    current_lineup = scrapy.Field()
    past_lineup = scrapy.Field()
    live_lineup = scrapy.Field()
    official_links = scrapy.Field()
    official_merch = scrapy.Field()
    unofficial_links= scrapy.Field()
    band_label_links = scrapy.Field()
    band_tabs = scrapy.Field()
    similar_artists = scrapy.Field()
    #{releases: {'all': name: {tracks: {track_name,tracknum_length,lyrics} ,type,year,notes,{album_lineup: name,role}
    releases = scrapy.Field()


