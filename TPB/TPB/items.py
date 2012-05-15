# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class TpbItem(Item):
    name = Field()
    magnet = Field()
    #match = Field()
    pass
