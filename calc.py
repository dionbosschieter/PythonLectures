#!/usr/bin/env python3

import os
import time
from multiprocessing import Process, Queue, Lock

usage = """[*]Author: Dion Bosschieter
[*]Gebruik: ./calc.py 
Geef een berekening op in de vorm '<getal1> <operator> <getal2>', 
 typ 'clear' om het scherm te legen of 'einde' om te stoppen:"""

def consumer(q, l):
	while True:

		if q.empty():
			time.sleep(0.05)	# als de input niks is slaap
			continue		# dan een seconde en ga weer verder
		else: 
			arr = q.get(False)

		if arr=="einde": #voor het netjes afsluiten van de thread
			break
		elif len(arr) == 3: #als er 3 waardes zijn opgegeven, check of de 2de waarde een operator is 
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

				consumerprint(output, l) #print berekening op het scherm
			else:
				consumerprint("die operator ken ik niet!", l)
		else: 
			consumerprint("Fout: geef een berekening op in de vorm '<getal1> <operator> <getal2>", l)

def consumerprint(msg, l):
	l.acquire()
	print("Consumer: ",msg)
	l.release()

def mainprint(msg, l):
	l.acquire()
	print(msg)
	l.release()

if __name__ == '__main__':
	
	val1 = ""
	q = Queue()
	l = Lock()
	p = Process(target=consumer, args=(q,l))
	p.start()

	mainprint(usage, l)

	while True:
		val1 = input("")
		
		if(val1 in ("einde","quit","exit")): break
		if(val1 in ("clear","cls","clearscreen")): os.system("clear"); continue
		if(val1 == ""): continue

		# als de queue leeg is plaats berekening
		# geef dit anders weer op het scherm
		if q.empty(): q.put(val1.split(' '), False)
		else: mainprint("Consumer moet de vorige berekening nog uitvoeren",l)

	q.put("einde") # vertel andere thread om te sluiten
	p.join() # wacht op andere thread