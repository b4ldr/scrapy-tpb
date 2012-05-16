#from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from TPB.items import TpbItem
import re

class TpbSpider(CrawlSpider):
	name = "tpb"
	allowed_domains = ["thepiratebay.se"]
	start_urls = [ "http://thepiratebay.se/browse/300/1/3" ]
	rules = ( 
		Rule (SgmlLinkExtractor(restrict_xpaths=('//td[@colspan="9"]/a[last()]')), callback='parse_item', follow=True),
	)

	def parse_item(self, response):
		hxs = HtmlXPathSelector(response)
		items = []
		item = TpbItem()
		links = hxs.select('//td')
                items = []
		pattern = re.compile('(linux|bsd|l?gpl|apache|mit|free|isc)', re.IGNORECASE)
                for link in links:
                        item = TpbItem()
                        item['name'] = link.select('div/a/text()').extract()
                        if not item['name']:
                                continue
			match = pattern.match(item['name'][0])
			if not match:
				continue
			item['match'] = match.group()
                        if not item['match']:
                                continue
                        item['magnet'] = link.select('a[@title="Download this torrent using magnet"]/@href').extract()
                        items.append(item)
                return items
