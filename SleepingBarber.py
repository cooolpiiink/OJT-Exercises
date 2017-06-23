import time, random
from Queue import Queue
from threading import Thread, Semaphore

class Suki(Thread):
	is_last = False
	no_chair = False

	def __init__(self, name, numChair, priority):
		Thread.__init__(self)
		self.name = name
		self.numChair = numChair
		self.priority = priority
		self.tired = 0

	def run(self):
		while True:
			if self.no_chair:
				print '{} is leaving'.format(self.name)
				break
			okayna = self.priority.acquire(False)
			if okayna:
				self.numChair.put(self)
				print '{}  is in the waiting room'.format(self.name)
				break
			else:
				self.hope()

	def hope(self):
		print '{} is hoping for a miracle'.format(self.name)
		self.tired += 1
		if self.tired >=5:
			self.no_chair = True
		time.sleep(4)

class Barber(Thread):
	def __init__(self, name, numChair, priority):
		Thread.__init__(self)
		self.name = name
		self.numChair = numChair
		self.priority = priority
		self.type = type
		self.count = 0

	def run(self):
		something = None
		while True:
			customer = something
			if customer is None:
				print '{} is going to sleep'.format(self.name)
				time.sleep(2)
				print '{} is now awake!'.format(self.name)
			else:
				self.startCut(customer)
				if customer.is_last:
					print'{} is done and closes shop.'.format(self.name)
					break
			something = self.numChair.get()

	def startCut(self, customer):
		hair = random.randint(0,4)
		style = ['Mohawk','Barber','Random','Trim','Mushroom']
		self.type = style[hair]
		print '{} serves {} with a {} cut.'.format(self.name, customer.name, self.type)
		time.sleep(3)
		self.priority.release()
		print '{} is done with {}.'.format(self.name, customer.name)
		self.count +=1


def main():
	numChair = Queue()
	priority = Semaphore(4)
	barber = Barber('Trint', numChair, priority)
	barber.start()
	time.sleep(4)
	customer = ['Paul', 'Peter', 'Matthew', 'John', 'Andrew', 'James', 'Todoroki', 'Midoriya']
	customers = [Suki(x, numChair, priority, ) for x in customer]
	customers[-3].is_last = True

	for suki in customers:
		suki.start()
	barber.join()
	for suki in customers:
		suki.join()

	print 'Served {} customers for today'.format(barber.count)

main()