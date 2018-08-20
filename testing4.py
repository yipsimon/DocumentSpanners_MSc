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
CONDITIONS = [(lambda i: i in ['0','1','2','3','4','5','6','7','8','9'], 1),(lambda i: i % 6 == 0, "six"),(lambda i: i % 7 == 0, "seven")]

def apply_conditions(i):
	for cond, replace in CONDITIONS:
		print('c',cond)
		print('r',replace)
		print('i',i)
		if cond(i):
			return replace
	return i

ar = apply_conditions('0')
print(ar)



print("--- %s seconds ---" % (time.time() - start_time))
