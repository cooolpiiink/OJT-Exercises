import time, random, requests, os
from PIL import Image
from StringIO import StringIO
from bs4 import BeautifulSoup
from Queue import Queue
from threading import Thread, Semaphore

class Scraper(Thread):
	is_full = False
	def __init__(self, something, pwede):
		Thread.__init__(self)
		self.something = something
		self.pwede = pwede

	def run(self):
		while True:
			if self.is_full:
				print 'puno'
				break
			if_okay = self.pwede.acquire(False)
			if if_okay:
				r = requests.get('https://c.xkcd.com/random/comic/')
				y = r.url
				print y
				self.something.put(self)
				self.getIMG(r)
			else:
				break
				
	def getIMG(self, r):
		soup = BeautifulSoup(r.text, 'html.parser')
		selector = '#comic img'
		img = soup.select(selector)[0]

		img_url = 'https:' + img.attrs['src']
		r=requests.get(img_url)
		filename = img.attrs['src'].split('/')[-1]
		i = Image.open(StringIO(r.content))
		i.save('TrintGallery/' + filename)

def createFolder(directory):
	try:
		if not os.path.exists(directory):
			os.makedirs(directory)
	except OSError:
		print ('Error: creating directory. ' + directory)

def main():
	something = Queue()
	createFolder('./TrintGallery/')
	a = Scraper(something, Semaphore(12))
	b = Scraper(something, Semaphore(13))
	c = Scraper(something, Semaphore(12)) 
	d = Scraper(something, Semaphore(13))
	a.start()
	b.start()
	c.start()
	d.start()
	a.join()
	b.join()
	c.join()
	d.join()
	print 'mana'

main()