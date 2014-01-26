import time

class Monitor(object):
	
	def __init__(self, monitorQueue, debug_log, info_container):
		self.monitorQueue 	= monitorQueue
		self.debug_log 		= debug_log
		self.info_container = info_container
		self.debug_log.log("Monitor thread initiating")

		self.info_container.refresh()
		self.debug_log.refresh()
		self.refreshtime = time.time()

	def waitForMessage(self):
		while True:
			try:
				msg = self.monitorQueue.get(False)
			except:
				time.sleep(0.1)
				self.refresh()
				continue
			if msg == "exit":
				break
			#print msg and refresh window
			self.debug_log.log(msg)
			self.refresh()

	def refresh(self):
		if((time.time()-self.refreshtime)>0.1):
			#update once per second.
			self.info_container.refresh()
			self.debug_log.refresh()
			self.refreshtime = time.time()