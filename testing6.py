import script2rev as sc2
import script3rev as sc3
import scriptgrph as sg
import script1rev as sc1
import threading, time, sys, copy, objgraph, random, inspect, re
'''
automata1 = sc2.automata(0,0,0)
automata1.reset()
automata1.states = ['0','1','2']
automata1.varstates = ['x']
automata1.transition['0'] = [('0','a'),('1','x+')]
automata1.transition['1'] = [('1','a'),('2','x-')]
automata1.transition['2'] = [('2','a')]
automata1.start = '0'
automata1.end = '2'


automata2 = sc2.automata(0,0,0)
automata2.reset()
automata2.states = ['0','1','2']
automata2.varstates = ['x']
automata2.transition['0'] = [('0','a'),('1','x+')]
automata2.transition['1'] = [('1','a'),('2','x-')]
automata2.transition['2'] = [('2','a')]

automata2.start = '0'
automata2.end = '2'

string = 'aaa'
sc1.funchk(automata1)
sc1.csymtonulllong(automata1)

sc1.funchk(automata2)
sc1.csymtonulllong(automata2)
sg.printgraph(automata1,'union1')
sg.printgraph(automata1,'union2')
sc3.union(automata1,automata2)

sg.printgraph(automata1,'unioned')
'''

automata1 = sc2.automata(0,0,0)
automata1.reset()
automata1.states = ['0','1','2','3','4']
automata1.varstates = ['x','y']
automata1.transition['0'] = [('0','a'),('1','x+')]
automata1.transition['1'] = [('1','a'),('2','y+')]
automata1.transition['2'] = [('2','a'),('3','x-')]
automata1.transition['3'] = [('3','a'),('4','y-')]
automata1.transition['4'] = [('4','a')]
automata1.start = '0'
automata1.end = '4'
sc1.funchk(automata1)
sc1.csymtonulllong(automata1)
print(automata1.varconfig)
auto = sc3.projection(automata1,['y'])
print(auto.varconfig)
#finalgraph = sc1.generateAg(auto,string)
#outputs = sc1.calcresults(finalgraph, len(string), auto.varconfig)
#sg.printresultsv2(outputs,auto,string,1,1)

#finalgraph1 = sc1.generateAg(automata1,string)
#finalgraph2 = sc1.generateAg(automata2,string)

#sc3.union(automata1,automata2,finalgraph1,finalgraph2,string,1)

#outputs = sc1.calcresults(finalgraph1, len(string), automata1.varconfig)
#sg.printresultsv2(outputs,automata1,string,1,1)
'''
sc3.union(automata1,automata2)
#automata1.printauto()
sg.printgraph(automata1,'o')
finalgraph = sc1.generateAg(automata1,string)
#if not finalgraph[-1]:
#	print('No results')
#	sys.exit(1)
outputgraph1, outputendnode1 = sg.finalauto(automata1,finalgraph)
sg.printrawgraph(outputgraph1, outputendnode1,'t1')
outputs = sc1.calcresults(finalgraph, len(string), automata1.varconfig)
sg.printresultsv2(outputs,automata1,string,1,1)
'''
'''
finalgraph1 = sc1.generateAg(automata1,string)
finalgraph2 = sc1.generateAg(automata2,string)
outputgraph1, outputendnode1 = sg.finalauto(automata1,finalgraph1)
outputgraph2, outputendnode2 = sg.finalauto(automata2,finalgraph2)
#sg.printrawgraph(outputgraph1, outputendnode1,'t1')
#sg.printrawgraph(outputgraph2, outputendnode2,'t2')
print(finalgraph1)
print(finalgraph2)
auto1 = copy.deepcopy(automata1)
auto2 = copy.deepcopy(automata2)
auto1.toint()
ref = auto2.toint(1)
for key in ref.keys():
	ref[key] += int(auto1.end)+1
ref[str(auto2.end)] += 1
temp = {}
for pos in finalgraph2.keys():
	temp[pos] = {}
	for keys in finalgraph2[pos].keys():
		temp[pos][str(ref[keys])] = set([])
		for item in finalgraph2[pos][keys]:
			temp[pos][str(ref[keys])].add(str(ref[item]))
last = int(auto2.end) + int(auto1.end)+1 +1
print('l',last)
for item in finalgraph1[len(string)-1].keys():
	finalgraph1[len(string)-1][item] = set(str(last))

#for item in newfinalgraph2[len(string)-1].keys():
#	newfinalgraph2[len(string)-1][item] = set(str(last))

for pos in finalgraph1.keys():
	finalgraph1[pos].update(temp[pos])
print(finalgraph1)
#outputgraph1, outputendnode1 = sg.finalauto(automata1,finalgraph)
#sg.printrawgraph(outputgraph1, outputendnode1,'t1')
outputs = sc1.calcresults(finalgraph1, len(string), automata1.varconfig)
sg.printresultsv2(outputs,automata1,string,1,1)

'''