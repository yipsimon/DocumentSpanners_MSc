import script2rev as sc2
import script3rev as sc3
import scriptgrph as sg
import script1rev as sc1
import threading, time, sys, copy, objgraph, random, inspect, re

start_time = time.time()
'''
test = '~`!@#$%^&*()_+ "GET"{}|:<>/.,;\][?'

test2 = " 'GET' "
for letter in test:
	print(letter)
	matching = re.match("\W",letter)
	if matching:
		val1 = "(?="+"\\"+letter+")"
		print (val1[0:3])
		print (val1)
		matching2 = re.match(val1,letter)
		print(matching2.groups())

matching3 = re.match("(?=(.))(?=[\n])",'\n')
if matching3:
	print(matching3.groups())	
string = 'aaaa'
print(string[0:4])
sys.exit(1)


regex = '.*,<x:[a-z]*>,.*'
automata = sc2.main(regex)
string = 'aaa'
sg.printgraph(automata,'tes')


CONDITIONS = [(lambda i: i % 4 == 0, "four"),(lambda i: i % 6 == 0, "six"),(lambda i: i % 7 == 0, "seven")]

def apply_conditions(i):
	for cond, replace in CONDITIONS:
		print('c',cond)
		print('r',replace)
		print('i',i)
		if cond(i):
			return replace
	return i

ar = apply_conditions(6)
print(ar)
'''
'''
CONDITIONS = [(lambda s,i,j: s[j-1:j] in ['0','1','2','3','4','5','6','7','8','9'], 'true'),(lambda s,i,j: s[j+i-2:j+i-1] in ['0','1','2','3','4','5','6','7','8','9'], 'true')] #,(lambda i: i % 7 == 0, "seven")]

def apply_conditions(i):
	for cond, replace in CONDITIONS:
		if cond(i):
			return replace
	return i

ar = apply_conditions('0')
print(ar)
'''
def apply_conditions(s,i,j,conditions):
	temp = True
	for cond in conditions:
		print('c',bool(cond(s,i,j)))
		temp = temp and bool(cond(s,i,j))
	#print(temp,s[j-1:j+i-1])
	return temp

#condits = [(lambda s,i,j: re.match(r'^\d+\.\d+\.\d+\.\d+$',s[j-2:j+i-1]))]
condits = [(lambda s,i,j: re.match(r'^\d+\.\d+\.\d+\.\d+$',s[j-1:j+i-1])),\
			(lambda s,i,j: True if j-1 == 0 else (True if re.match(r'^[^0-9]$',s[j-2]) else False) ),\
			(lambda s,i,j: True if j+i-1 == len(string) else (True if re.match(r'^[^0-9]$',s[j+i-1]) else False) )]
string = '66.77.88.99'
i = 11
j = 1
print(string[j-1:j+i-1])
print(j+i-1,len(string))
othercond = apply_conditions(string,i,j,condits)
print('f',othercond)
'''
for i in range(11,12):
	for j in range(1,len(string)+2-i):
		for k in range(j+1,len(string)+2-i):
			if string[j-1:j+i-1] == string[k-1:k+i-1]:
				print ('j ',string[j-1:j+i-1],' k',string[k-1:k+i-1])
				othercond = apply_conditions(string,i,j,condits)
				print(othercond)
print("--- %s seconds ---" % (time.time() - start_time))
'''