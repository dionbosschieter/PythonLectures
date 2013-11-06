def whatToDo(prompt, options=('y', 'n'), default='n'):
	while True:
		invoer = input(prompt)
		if len(invoer) < 1:
			return default
		elif int(invoer) in options:
			return int(invoer)

def getCijfer(prompt):
	while True:
		invoer = input(prompt)
		if type(int(invoer)) == type(1):
			return int(invoer)
		else: print("voer een cijfer in")

wildoen = whatToDo("""Wat wil je doen? 
1: keer
2: gedeeld door
3: plus
4: min
> """, (1,2,3,4), 1)

numcijfers = getCijfer("Hoeveel cijfers wil je gebruiken? ")
array = []
	
for i in  range(numcijfers):
	array.append(getCijfer("#"+str(i+1)+"> "))

if wildoen == 1:
	answer = array[0]
	for i in range(len(array)-1):
		answer = answer * array[i+1]
	print("antwoord is ", answer)
		
elif wildoen == 2:
	answer = array[0]
	for i in range(len(array)-1):
		answer = answer / array[i+1]
	print("antwoord is ", answer)
	
elif wildoen == 3: 
	print("antwoord is ", sum(array))
elif wildoen == 4:
	answer = array[0]
	for i in range(len(array)-1):
		answer = answer - array[i+1]
	print("antwoord is ", answer)
	
