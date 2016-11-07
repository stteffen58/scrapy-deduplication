from __future__ import division, unicode_literals
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

from sklearn.feature_extraction.text import HashingVectorizer
from bs4 import BeautifulSoup

class HTMLPreprocessing():
	def __init__(self,html_doc):
		self._html_doc = html_doc
		self._soup = BeautifulSoup(self._html_doc, 'html.parser')
		for script in self._soup(["script", "style"]):
			script.extract()
	
	def getText(self):
         text = self._soup.get_text()
         return text

class HashVect():
	def __init__(self):
		self._vectorizer = HashingVectorizer(stop_words='english')

	def getVect(self,content):
		l = [content]
		return self._vectorizer.fit_transform(l)

    
