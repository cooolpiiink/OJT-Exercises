import time, random, requests, os, glob, datetime
from PIL import Image
from StringIO import StringIO
from bs4 import BeautifulSoup
from Queue import Queue
from threading import Thread, Semaphore

class Scraper(Thread):
	def __init__(self, something, pwede, limit):
		Thread.__init__(self)
		self.something = something
		self.pwede = pwede
		self.limit = limit
		self.date = datetime.datetime.now().strftime ("%Y - %m - %d")
	def run(self):
		while True:
			if_okay = self.pwede.acquire(False)
			if not if_okay or len(self.something) > self.limit:
				break
			file = open('./xkcd/' + self.date + '/urls.text', "a")
			r = requests.get('https://c.xkcd.com/random/comic/')
			if self.check(r):
				y = r.url
				print y
				file.write("\n" + y)
				self.something.append(y)
				print len(self.something)
				self.getIMG(r)
			
	def check(self, r):
		file = open('./xkcd/' + self.date + '/urls.text', "r")
		lines = file.readlines()
		y = r.url
		if y in lines:
			return False
		return True


	def getIMG(self, r):
		if len(self.something) <= self.limit:
			soup = BeautifulSoup(r.text, 'html.parser')
			selector = '#comic img'
			img = soup.select(selector)[0]
			img_url = 'https:' + img.attrs['src']
			r=requests.get(img_url)
			filename = img.attrs['src'].split('/')[-1]
			i = Image.open(StringIO(r.content))
			i.save(('xkcd/' + self.date + '/') + filename)
			time.sleep(3)
			self.pwede.release()

def createFolder(directory):
	try:
		if not os.path.exists(directory):
			os.makedirs(directory)
	except OSError:
		print ('Error: creating directory. ' + directory)

def main():
	something = []
	limit = 50
	day = datetime.datetime.now().strftime ("%Y - %m - %d")
	createFolder('./xkcd/' + day +'/')
	file = open('./xkcd/' + day + '/urls.text', "w")
	file.write("List of urls \n")
	
	a = Scraper(something, Semaphore(5), limit)
	b = Scraper(something, Semaphore(5), limit)
	c = Scraper(something, Semaphore(5), limit)
	d = Scraper(something, Semaphore(5), limit)
	a.start()
	b.start()
	c.start()
	d.start()
	a.join()
	b.join()
	c.join()
	d.join()

	print 'mana'
	for x in range(0, len(something)):
		print something[x]
	file.close()

main()
