#!/usr/bin/env python3

import os
import time
from multiprocessing import Process, Queue

usage = """[*]Author: Dion Bosschieter
[*]Gebruik: ./calc.py 
Geef een berekening op in de vorm '<getal1> <operator> <getal2>', 
 typ 'clear' om het scherm te legen of 'einde' om te stoppen:
 """

def consumer(q):
	while True:

		if q.empty():
			time.sleep(0.5)	# als de input niks is slaap
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
				consumerprint("dit zijn geen getallen")
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

				consumerprint(output) #print berekening op het scherm
			else:
				consumerprint("die operator ken ik niet!")

def consumerprint(msg):
	print("Consumer: ",msg)

if __name__ == '__main__':
	print(usage)

	val1 = ""
	q = Queue()
	p = Process(target=consumer, args=(q,))
	p.start()

	while True:
		val1 = input()

		if(val1 in ("einde","quit","exit")): break
		if(val1 in ("clear","cls","clearscreen")): os.system("clear")
		q.put(val1.split(' '), False)

	q.put("einde") # vertel andere thread om te sluiten
	p.join() # wacht op andere thread