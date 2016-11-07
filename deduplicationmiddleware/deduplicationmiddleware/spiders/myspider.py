import scrapy

def loadDomains():
	# open file and load allowed_domains separated by new line
	with open('allowed_domains','r') as f:
		for line in f:
			yield line.strip()

def loadSeeds():
	# open file and load seeds separated by new line
	with open('start_urls','r') as f:

		for line in f:
			yield line.strip()

class MySpider(scrapy.Spider):
	name = "MySpider"
	allowed_domains = loadDomains()
	start_urls = loadSeeds()
	
	def parse(self,response):
		for href in response.css("a::attr('href')"):
			url = response.urljoin(href.extract())
			yield scrapy.Request(url, callback=self.parse)