import scrapy
from first_scrapy.items import NewCamp

class CampingSpider(scrapy.Spider):
	name = "CampingSpider"
	allowed_domains = [
		'www.camping.hr',
	]
	start_urls = ['https://www.camping.hr/croatian-campsites']

	def parse(self, response):
		for i in range(1,21):
			item = NewCamp()
			item['name']=response.xpath('//*[@id="the-serp"]/li[{}]/div[2]/h2/a/strong/text()'.format(i)).extract()
			item['region']=response.xpath('//*[@id="the-serp"]/li[{}]/div[2]/div[1]/text()'.format(i)).extract()[0].split('(')[1].split(')')[0]
			item['url']=response.xpath('//*[@id="the-serp"]/li[{}]/div[2]/h2/a/@href'.format(i)).extract()
			item['capacity']=response.xpath('//*[@id="the-serp"]/li[{}]/div[2]/div[2]/ul/li[2]/strong/text()'.format(i)).extract()

			yield item
		