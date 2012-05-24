#from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from TPB.tpb_items import TpbItem
import re
import json

class TpbSpider(CrawlSpider):
	name = "tpb_vodo"
	allowed_domains = ["thepiratebay.se"]
	start_urls = [ "http://thepiratebay.se/search/vodo/0/" ]
	rules = ( 
		#Rule (SgmlLinkExtractor(restrict_xpaths=('//td[@colspan="9"]/a[last()]')), callback='parse_item', follow=True),
		Rule (SgmlLinkExtractor(restrict_xpaths=('//div[@align="center"]')), callback='parse_item', follow=True),
	)

	def parse_item(self, response):
	        vodo_json = json.loads(open("/home/jbond/json").read())
		hxs = HtmlXPathSelector(response)
		items = []
		item = TpbItem()
		links = hxs.select('//td')
                items = []
		btih = re.compile("urn:btih:([a-f0-9]+)")
                for link in links:
                        item = TpbItem()
                        item['name'] = link.select('div/a/text()').extract()
                        if not item['name']:
                                continue
                        item['magnet'] = link.select('a[@title="Download this torrent using magnet"]/@href').extract()
			match = btih.search(item['magnet'][0])
			if match:
				item['btih'] = match.group(1)
			for bith_vodo in vodo_json['hashlist']:
				if item['btih'] ==  bith_vodo['bith']:
                        		items.append(item)
					print item['magnet'][0]
					break
					
                return items
