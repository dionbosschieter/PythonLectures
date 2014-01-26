#!/usr/bin/env python3

import os
import time
import sys
import curses

from curses import panel
from threading import Thread
from multiprocessing import Queue

#custom classes
import terminal
from consumer import Consumer
from monitor import Monitor
from window import Window
from debugconsole import DebugConsole
from infocontainer import InfoContainer

usage = """[*]Author: Dion Bosschieter
[*]Gebruik: ./Calculator.py [bestandsnaam] [aantalthreads]
./Calculator.py sommen.txt 4
./Calculator.py sommen.txt

"""

class Calculator(object):

	def __init__(self, stdscreen):
		
		if(len(sys.argv) < 3 ):
			self.threadcount = 1
		elif(sys.argv[2].isdigit()):
			self.threadcount = int(sys.argv[2])

		self.screen = stdscreen
		curses.curs_set(0)

		#init of curses
		title = "Calculator - Dion Bosschieter - Version: 1"
		debug_console = DebugConsole(self.screen, "Debugging information")
		info_container = InfoContainer(self.screen, "Calc info", debug_console, self.threadcount)
		main_window = Window(title, self.screen)
		main_window.display()

		#main bussiness
		debug_console.log("De berekeningen worden gelezen uit de file " + filename)
		debug_console.log("Aantal threads " + str(self.threadcount))

		cq = [] #calculator queue array
		cqCount = [] #calculator queue array
		mq = Queue() #monitor queue
		ct = [] #thread array

		_monitor = Monitor(mq, debug_console, info_container)
		mp = Thread(target=_monitor.waitForMessage) #monitor worker(thread)
		mp.start() #start de monitor thread

		#create the Calculator queue(s) and thread(s)
		for i in range(0,self.threadcount):
			cq.append(Queue())
			cqCount.append(0)
			_consumer = Consumer(cq[i],mq,i, info_container, debug_console)
			t = Thread(target=_consumer.calculate)
			ct.append(t)

		#read the file and close it
		lines = f.read().splitlines()
		count = 0
		for line in lines:
			mq.put_nowait("Read (P): "+line+" in queue:"+str(count))
			cq[count].put_nowait(line)
			cqCount[count]+=1
			count += 1
			if count == self.threadcount: count = 0
		f.close()
		
		#starting thread(s)
		for i in range(0,self.threadcount):
			info_container.initTotalSums(cqCount[i], i) # tel info container the num of sums

			mq.put_nowait("[*] Starting consumer-thread: "+str(i+1))
			ct[i].start()

		#cleanup
		for i in range(0,self.threadcount):
			cq[i].put_nowait("exit") # tell the consumer thread(s) to close
			ct[i].join() # wait for thread
		
		#press q to quit
		while(True):
			debug_console.log("Press 'q' to quit")
			c = terminal.getch()
			if c == 'q': break

		mq.put_nowait("exit") # vertel de monitor thread om te sluiten
		mp.join() # wacht op thread


def error(msg):
	print(usage)
	print(msg)

if __name__ == '__main__':
	
	if(len(sys.argv) < 2):
		print(usage)
		quit()

	filename = sys.argv[1] 
	
	#check if file exists
	try: 
		f = open(filename,'r')
	except:
		error("Bestand bestaat niet")
		quit()
	
	#check if a threadcount argument is given
	#check if the given argument is a digit
	#else threadcount = 1
	if(len(sys.argv) < 3 ):
		threadcount = 1
	elif(sys.argv[2].isdigit() != True):
		error("ValueError: geef een cijfer op voor threadaantal")
		quit()
	elif(sys.argv[2].isdigit()):
		threadcount = int(sys.argv[2])

	curses.wrapper(Calculator)