from threading import Thread, Lock
import time
import logging
import random


logging.basicConfig(level=logging.DEBUG,
	format='%(threadName)-1s %(message)s',
	)

spork = [Lock(), Lock(), Lock(), Lock(), Lock()]
full = []
def pick(i):
	j = i + 1
	if j == 5:
		j = 0
	left = spork[i]
	right = spork[j]
	value = random.randint(4,10)
	time.sleep(value)
	if left.acquire():
		logging.debug('acquired left spork-' + str(i))
		
		if right.acquire():
			time.sleep(random.randint(1,4))
			logging.debug('acquired right spork-' + str(j))
			time.sleep(2)
			logging.debug('starts eating')
			time.sleep(5)
			logging.debug('finished eating')
			logging.debug('released right spork-' + str(j))
			logging.debug('released left spork-' + str(i))
			right.release()
			left.release()
			time.sleep(2)
			logging.debug('is full')
			full.append("FULL")
			if len(full) == 5:
				print ('EVERYONE IS FULL')	
			else:
				pass
		else:
			logging.debug('cant get the right spork-' + str(j))
			loggind.debug('releasing the left spork-' + str(i))
			left.release()
	else:
		# left.wait()
		time.sleep(2)
		logging.debug('waiting')
	
def main():
	A = Thread(name = 'Aristotle', target=pick, args=(0,))
	K = Thread(name = 'Kant', target=pick, args=(1,))
	B = Thread(name = 'Buddha', target = pick, args=(2,)) 
	R = Thread(name = 'Russel', target=pick, args=(3,))
	M = Thread(name = 'Marx', target = pick, args=(4,)) 

	A.start()
	K.start()
	B.start()
	R.start()
	M.start()

	A.join()
	K.join()
	B.join()
	R.join()
	M.join()
main()