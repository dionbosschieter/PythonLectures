#!/usr/bin/env python3

import sys
from multiprocessing import Pool

usage = """
[*]Author: Dion Bosschieter
[*]Gebruik: ./fact.py 10 8
[*] output:
1! = 1
2! = 2*1 = 2
3! = 3*2*1 = 6
4! = 4*3*2*1 = 24
5! = 5*4*3*2*1 = 120
...

Waarbij de '10' het maximum aangeeft (dus t/m '10! = ...') en '8' het aantal workers in de Pool.
"""

def printusage():
	print(usage)
	quit()

def fct(x):
	x+=1; ret=1; a = []

	for i in range(x+1):
		if i == 0: continue
		a = [i] + a
		ret *= i
	
	return ret, a

def printfactorials(factorials):
	for i in factorials:
		printstr = str(i[1][0]) + "! = "
		for istr in i[1]:
			printstr += str(istr) 
			if(istr!=i[1][-1]): printstr+= "*"
		
		print(printstr,'=',i[0])
		

if __name__ == '__main__':
	
	if(len(sys.argv) < 3): 
		printusage()
		
	try: 
		f1 = int(sys.argv[1])
		f2 = int(sys.argv[2])
	except ValueError:
		print("Voer alstublieft nummers in!")
		printusage()
	p = Pool(f2)

	printfactorials(p.map(fct, range(f1)))
