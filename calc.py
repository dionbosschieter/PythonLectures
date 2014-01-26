#!/usr/bin/env python3

import os
import time
import sys
from threading import Thread
from queue import Queue

usage = """[*]Author: Dion Bosschieter
[*]Gebruik: ./calc.py [bestandsnaam] [aantalthreads]
./calc.py sommen.txt 4
./calc.py sommen.txt
De berekeningen worden gelezen uit de file 'sommen.txt'
Read  (P): 6 + 4
Write (C): 6 + 4 = 10
Alle sommen zijn verwerkt, einde programma.
"""

def consumer(cq,mq,thrdn):
	while True:
		
		qitem = cq.get()
		#time.sleep(0.0001)
	
		if qitem=="exit": #check if this thread can shutdown
			mq.put_nowait("[*]Stopping consumer-thread["+str(thrdn+1)+"]") #shutdown message
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
				consumerprint("dit zijn geen getallen",mq,thrdn)
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

				consumerprint(output,mq,thrdn) #print berekening op het scherm
			else:
				consumerprint("die operator ken ik niet!",mq,thrdn)
		else: 
			consumerprint("Fout: geef een berekening op in de vorm '<getal1> <operator> <getal2>",mq,thrdn)

def monitor(mq):
	while True:
		msg = mq.get()
		if msg == "exit":
			break
		print(msg)

def consumerprint(msg,mq,thrdn):
	mq.put_nowait("Consumer["+str(thrdn+1)+"]: "+msg)

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

	print("De berekeningen worden gelezen uit de file", filename)
	print("Aantal threads", threadcount)

	cq = [] #calculator queue array
	mq = Queue() #monitor queue
	ct = [] #thread array
	mp = Thread(target=monitor, args=(mq,)) #monitor worker(thread)

	#create the Calculator queue(s) and thread(s)
	for i in range(0,threadcount):
		cq.append(Queue())
		t = Thread(target=consumer, args=(cq[i],mq,i,), daemon=True)
		ct.append(t)

	#read the file and close it
	lines = f.read().splitlines()
	count = 0
	for line in lines:
		mq.put_nowait("Read (P): "+line+" in queue:"+str(count))
		cq[count].put_nowait(line)
		count += 1
		if count == threadcount: count = 0
	f.close()

	#starting thread(s)
	for i in range(0,threadcount):
		mq.put_nowait("[*] Starting consumer-thread: "+str(i+1))
		ct[i].start()
	
	mp.start() #start de monitor thread

	#cleanup
	for i in range(0,threadcount):
		cq[i].put_nowait("exit") # tell the consumer thread(s) to close
		ct[i].join() # wait for thread
	
	mq.put("exit") # vertel de monitor thread om te sluiten
	mp.join() # wacht op thread