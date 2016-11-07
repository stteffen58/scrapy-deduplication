import sys
reload(sys)
sys.setdefaultencoding('UTF8')
import scrapy

from preprocessing import HashVect
from preprocessing import HTMLPreprocessing
sys.path.append('SparseLSH-master/sparselsh/')
from lsh import LSH

class DeduplicationMiddleware(object):
	def  process_spider_input(self,response, spider):
		content = HTMLPreprocessing(response.body).getText()
		for object in self._lsh.query(self._hashvect.getVect(content),distance_func='cosine'):
			if float(object[1]) < self._dTrehold:
				raise  scrapy.exceptions.DropItem('Item has been identified as duplicate by LSH. Distance: ' + str(object[1]))
		self._lsh.index(self._hashvect.getVect(content),extra_data=response.url)
		return None

	def process_spider_output(self,response, result, spider):
		return result

	def process_spider_exception(self,response, exception, spider):
		return None

	def __init__(self,digest_length,num_hashtables,dTreshold): 
		self._dTrehold = dTreshold
		self._lsh = LSH(digest_length,2**20,storage_config=None,num_hashtables=num_hashtables)
		self._hashvect = HashVect()

	@classmethod
	def from_crawler(cls, crawler):
		if not crawler.settings.getint('DIGEST_LENGTH'):
			raise scrapy.exceptions.NotConfigured('DIGEST_LENGTH missing')
		if not crawler.settings.getint('NUM_HASHTABLES'):
			raise scrapy.exceptions.NotConfigured('NUM_HASHTABLES missing')
		if not crawler.settings.getfloat('DIST_TRESHOLD'):
			raise scrapy.exceptions.NotConfigured('DIST_THRESHOLD missing')

		digest_length = crawler.settings.getint('NUM_HASHTABLES')
		num_hashtables = crawler.settings.getint('DIGEST_LENGTH')
		dTreshold = crawler.settings.getfloat('DIST_TRESHOLD')

		ext = cls(digest_length,num_hashtables,dTreshold)
		return ext

