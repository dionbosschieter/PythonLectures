import time

class Consumer(object):
	
	def __init__(self, customerQueue, monitorQueue,threadNumber, info_container, debug_log):
		self.monitorQueue 	= monitorQueue
		self.customerQueue 	= customerQueue
		self.threadNumber 	= threadNumber
		self.info_container = info_container
		self.debug_log 		= debug_log

	def calculate(self):
		while True:

			qitem = self.customerQueue.get()
			time.sleep(0.1)

			if qitem=="exit": #check if this thread can shutdown
				self.debug_log.log("[*]Stopping consumer-thread["+str(self.threadNumber+1)+"]") #shutdown message
				self.info_container.taskDone()
				break
			else:
				arr = qitem.split(' ')
			if len(arr) == 3: #if 3 values, check if 2nd value is an operator
				operator = arr[1]
				
				try:
					getal1 = int(arr[0])
					getal2 = int(arr[2])
					output = arr[0] + " " +  arr[1] + " " + arr[2] + " = "
				except ValueError:
					self.consumerPrint("dit zijn geen getallen")
					continue
				
				if operator in ("+","-","*","/","^"):
					if operator == "+":
						output += str(getal1 + getal2)
					elif operator == "-":
						output += str(getal1 - getal2)
					elif operator == "*":
						output += str(getal1 * getal2)
					elif operator == "/":
						output += str(getal1 / getal2)
					elif operator == "^":
						output += str(getal1 ** getal2)

					self.consumerPrint(output) #print berekening op het scherm
				else:
					self.consumerPrint("die operator ken ik niet!")
			else: 
				self.consumerPrint("Fout: geef een berekening op in de vorm '<getal1> <operator> <getal2>")

			self.info_container.updateIndex(self.threadNumber) # update index

	def consumerPrint(self, message):
		self.monitorQueue.put_nowait("Consumer["+str(self.threadNumber+1)+"]: "+message)

