#from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from TPB.vodo_items import VodoItem
import re
import libtorrent
import urllib
class VodoSpider(CrawlSpider):
	name = "vodo"
	allowed_domains = ["vodo.net"]
	start_urls = [ "http://vodo.net/film/allfilms/downloads" ]
	rules = ( 
		Rule (SgmlLinkExtractor(restrict_xpaths=('//ul[@id="List"]/li/a[1]')), callback='parse_item', follow=True),
	)

	def parse_item(self, response):
		hxs = HtmlXPathSelector(response)
		#links = hxs.select('//a[@class="download"]/@href').extract()
		links = hxs.select('//a[contains(@href, ".torrent")]/@href').extract()
		items = []
                for link in links:
			item = VodoItem()
			torrent_url = "http://vodo.net" + link
			torrent = libtorrent.bdecode(urllib.urlopen(torrent_url).read())
			if not torrent:
				continue
			torrent_info = libtorrent.torrent_info(torrent)
			item['bith'] =  unicode(torrent_info.info_hash())
			print torrent_info.info_hash()
			items.append(item)
		return items
				
