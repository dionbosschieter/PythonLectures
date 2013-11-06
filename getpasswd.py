class GetPassword:

	def __init__(self):
		self.pwdlist = {}
		with open("/etc/passwd") as f: 
			for line in f: 
				temparr = line.split(':')
				if len(temparr) > 1:
					temparr = {'name': temparr[0],'home': temparr[5]}
					self.pwdlist[temparr['name']] = temparr

	def printList(self):
		print(self.pwdlist)

	def getUser(self,user):
		return self.pwdlist[user]

pwdrdr = GetPassword()

#for debuggin
#pwdrdr.printList()

user = pwdrdr.getUser('root')
print(user['home'])