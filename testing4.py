import script2rev as sc2
import script3rev as sc3
import scriptgrph as sg
import script1rev as sc1
import threading, time, sys, copy, objgraph, random, inspect, re

start_time = time.time()
test = '~`!@#$%^&*()_+ "GET"{}|:<>/.,;\][?'
'''
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
'''
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

print("--- %s seconds ---" % (time.time() - start_time))
