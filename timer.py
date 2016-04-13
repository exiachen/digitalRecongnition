import threading
import time

mutex = threading.Lock()

class Timer(threading.Thread):
	def __init__(self, seconds, action, args):
		threading.Thread.__init__(self)
		self.daemon = True
		self.runTime = seconds
		self.keepRuning = True
		self.args = args
		self.action = action

	def countDown(self):
		if not self.runTime:
			return False
		while self.runTime:
			mutex.acquire()
			self.runTime -= 1
			mutex.release()
			time.sleep(1.0)
		return True

	def run(self):
		while self.keepRuning:
			if self.countDown():
				self.action(self.args)
			else:
				time.sleep(0.5)

	def modTimer(self, moreSec):
		mutex.acquire()
		self.runTime += moreSec
		mutex.release()

	def cancelTimer(self):
		mutex.acquire()
		self.keepRuning = False
		mutex.release()
