# nospr.py

import scrapy
from first_scrapy.items import NewConcert

from scrapy_splash import SplashRequest
class CampingSpider(scrapy.Spider):
	name = "nospr"
	
	def start_requests(self):

		allowed_domains = [
			'www.nospr.org.pl',
		]

		start_urls = ['http://www.nospr.org.pl/pl/kalendarz?page=1&series__title=&room=SKC&season=&subscriptions__name=&date=']

		for url in start_urls:
			yield SplashRequest(url=url, callback=self.parse)
	
	# control indicates which tr we are analysing. Every even tr is empty on website.
	control = 1 
	def parse(self, response):
		SET_XPATH = '/html/body/div[1]/div[2]/div[2]/div/table/tbody/tr'

		for concert in response.xpath(SET_XPATH):
			NAME_XPATH = 'td[3]/div/h2/a/text()'
			URL_XPATH = 'td[3]/div/h2/a/@href'
			DATE_XPATH = 'td[2]/span[1]/span[1]/text()'

			if self.control == 1:
				item = NewConcert()
				item['name']=concert.xpath(NAME_XPATH).extract()
				item['url']='www.nospr.org.pl' + concert.xpath(URL_XPATH).extract()[0]
				item['date']=concert.xpath(DATE_XPATH).extract()
				self.control = self.control * -1

				yield item
			else:
				self.control = self.control * -1

		NEXT_PAGE_XPATH = '/html/body/div[1]/div[2]/div[2]/div/div[2]/a/@href'
		next_page = response.xpath(NEXT_PAGE_XPATH)[-1].extract()


		print('*' * 10)

		if next_page:
			next_page = 'http://www.nospr.org.pl/pl/kalendarz' + str(next_page)
			yield scrapy.Request(next_page, callback=self.parse)
