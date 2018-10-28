import scrapy
from first_scrapy.items import NewCamp

from scrapy_splash import SplashRequest
class CampingSpider(scrapy.Spider):
	name = "CampingSpider"
	url = []
	def start_requests(self):

		allowed_domains = [
			'www.camping.hr',
		]

		start_urls = ['https://www.camping.hr/croatian-campsites']

		for url in start_urls:
			yield SplashRequest(url=url, callback=self.parse)
	
	def parse(self, response):
		for camp in response.xpath('//*[@id="the-serp"]/li'):
			item = NewCamp()
			item['name']=camp.xpath('div[2]/h2/strong/text()').extract() #różnią się linkiem

			yield item


		# for i in range(1,21):
		# 	item = NewCamp()
		# 	item['name']=response.xpath('//*[@id="the-serp"]/li[{}]/div[2]/h2/a/strong/text()'.format(i)).extract()
		# 	item['region']=response.xpath('//*[@id="the-serp"]/li[{}]/div[2]/div[1]/text()'.format(i)).extract()[0].split('(')[1].split(')')[0]
		# 	item['url']=response.xpath('//*[@id="the-serp"]/li[{}]/div[2]/h2/a/@href'.format(i)).extract()
		# 	item['capacity']=response.xpath('//*[@id="the-serp"]/li[{}]/div[2]/div[2]/ul/li[2]/strong/text()'.format(i)).extract()

		# 	yield item

		next_page = response.xpath('//*[@id="top-serp-nav"]/p[3]/a[6]/@href').extract_first()
		if next_page is not None:
			next_page = 'https://www.camping.hr' + str(next_page)
			self.url.append(next_page)
			print(self.url)
			yield scrapy.Request(next_page, callback=self.parse)