import script2rev as sc2
import script3rev as sc3
import scriptgrph as sg
import script1rev as sc1
import threading, time, sys, copy, objgraph, random, inspect, re

start_time = time.time()
#regex = input('test')
#print(regex)

#regex = '("[a-z]"*),<x:("[a-z]"*)>,("[a-z]"*)'
regex = '[A-Z]*,<x:[a-z]*>,[0-9]*'
automata = sc2.main(regex)
'''
string = 'aaa'
#sg.printgraph(automata,'tes')
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


cond = '(.*)'

for let in string:
	print(let) 
	prog = re.compile(cond)
	matcho = re.match(cond, let)
	if matcho:
		print ('m',matcho.group(0))


tab = texttable.Texttable()
headings = ['Names','Weights','Costs','Unit_Costs']
tab.header(headings)
names = ['bar', 'chocolate','chips']
weights = [0.05, 0.1, 0.25]
costs = [2.0, 5.0, 3.0]
unit_costs = [40.0, 50.0, 12.0]

for row in zip(names, weights, costs, unit_costs):
	tab.add_row(row)

s = tab.draw()

print(s)
'''
print("--- %s seconds ---" % (time.time() - start_time))
sys.exit(1)