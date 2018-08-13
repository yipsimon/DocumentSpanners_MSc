import script2rev as sc2
import script3rev as sc3
import scriptgrph as sg
import script1rev as sc1
import threading, time, sys, copy, objgraph, random, inspect, re

start_time = time.time()
#regex = input('test')
#print(regex)
'''
regex = '[a-z]*,<x:[a-z]*>,[a-z]*'
automata = sc2.main(regex)
string = 'aaa'
#sg.printgraph(automata,'tes')
'''
string = 'a'*30
automata = sc3.stringequality(string)
sys.exit(1)
sc1.funchk(automata)
sc1.csymtonulllong(automata)
#sg.printgraph(automata,'tes2')


finalgraph = sc1.generateAg(automata,string)
automata.printauto()
for pos, trans in finalgraph.items():
	print ('position : ', pos)
	for start, item in trans.items():
		print ('start node : ', start)
		print ('destinations : ', item)

outputgraph, outputendnode = sc1.finalauto(automata,finalgraph)

sg.printrawgraph(outputgraph,outputendnode,'output')

outputs = sc1.calcresults(finalgraph, len(string), automata.varconfig)
sc1.printresultsv2(outputs,automata)
sys.exit(1)

'''

cond = '(.*)'

for let in string:
	print(let) 
	prog = re.compile(cond)
	matcho = re.match(cond, let)
	if matcho:
		print ('m',matcho.group(0))
'''
print("--- %s seconds ---" % (time.time() - start_time))