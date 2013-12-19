#!/usr/bin/env python3

import os
import time
import sys
from multiprocessing import Process, Queue, Lock

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
		
		try:
			arr = cq.get(False)
		except:
			#queue is empty
			continue

		if arr=="exit": #voor het netjes afsluiten van de thread
			cq.put_nowait("exit") # vertel de "mogelijk" volgende thread om te sluiten
			mq.put_nowait("[*]Stopping consumer-thread["+str(thrdn+1)+"]") #geef aan dat je stopt
			break
		if len(arr) == 3: #als er 3 waardes zijn opgegeven, check of de 2de waarde een operator is 
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
		if mq.empty() != True:
			msg = mq.get(False)
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

	print("De berekeningen worden gelezen uit de file ", filename)
	print("Aantal threads", threadcount)

	cq = Queue() #calculator queue
	mq = Queue() #monitor queue
	cp = [] #thread array
	mp = Process(target=monitor, args=(mq,)) #monitor worker(thread)
	mp.start()


	for i in range(0,threadcount):
		mq.put_nowait("[*]Starting consumer-thread: "+str(i+1))
		cp.append(Process(target=consumer, args=(cq,mq,i,)))
		cp[i].start()

	#read the file and close it
	lines = f.read().splitlines()
	for line in lines:
		mq.put_nowait("Read (P): "+line)
		cq.put_nowait(line.split(' '))
	f.close()

	#cleanup
	cq.put_nowait("exit") # vertel de consumer thread(s) om te sluiten

	for i in range(0,threadcount):
		cp[i].join() # wacht op thread

	mq.put("exit") # vertel de monitor thread om te sluiten
	mp.join() # wacht op thread