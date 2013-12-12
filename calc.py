#!/usr/bin/env python3

import os
import time
import sys
from multiprocessing import Process, Queue, Lock

usage = """[*]Author: Dion Bosschieter
[*]Gebruik: ./calc.py sommen.txt
De berekeningen worden gelezen uit de file 'sommen.txt'
Read  (P): 6 + 4
Write (C): 6 + 4 = 10
Alle sommen zijn verwerkt, einde programma.
"""

def consumer(cq,mq):
	while True:
		
		if cq.empty(): #check queue zodat we geen exception krijgen
			continue
		else: 
			arr = cq.get(False)

		if arr=="exit": #voor het netjes afsluiten van de thread
			break
		if len(arr) == 3: #als er 3 waardes zijn opgegeven, check of de 2de waarde een operator is 
			operator = arr[1]
			
			try:
				getal1 = int(arr[0])
				getal2 = int(arr[2])
				output = arr[0] + " " +  arr[1] + " " + arr[2] + " = "
			except ValueError:
				consumerprint("dit zijn geen getallen", l)
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

				consumerprint(output,mq) #print berekening op het scherm
			else:
				consumerprint("die operator ken ik niet!",mq)
		else: 
			consumerprint("Fout: geef een berekening op in de vorm '<getal1> <operator> <getal2>",mq)

def monitor(mq):
	while True:
		if mq.empty() != True:
			msg = mq.get(False)
			if msg == "exit":
				break
			print(msg)

def consumerprint(msg,mq):
	mq.put(("Consumer: "+msg),False)

if __name__ == '__main__':
	
	if(len(sys.argv) < 2):
		print(usage)
		quit()

	filename = sys.argv[1]

	cq = Queue()
	mq = Queue()

	cp = Process(target=consumer, args=(cq,mq,))
	mp = Process(target=monitor, args=(mq,))
	mp.start()
	cp.start()

	#open ZEH file
	f = open(filename,'r')
	lines = f.read().splitlines()
	for line in lines:
		mq.put(("Read (P): "+line), False)
		cq.put(line.split(' '),False)

	f.close()

	#cleanup
	cq.put("exit") # vertel andere thread om te sluiten
	cp.join() # wacht op thread
	mq.put("exit") # vertel thread om te sluiten
	mp.join() # wacht op thread