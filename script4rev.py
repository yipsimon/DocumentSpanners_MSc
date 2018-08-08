import script2rev as sc2
import script3rev as sc3
import scriptgrph as sg
import script1rev as sc1
import threading, time, sys, copy, objgraph, random, inspect

start_time = time.time()

automata = sc2.automata(0,0,0)
automata.reset()
automata.states = automata.states | {'0','1','2','3','4'}
automata.varstates = ['x','y']
automata.transition['0'] = [('1','x+')]
automata.transition['1'] = [('1','a'),('2','x-')]
automata.transition['2'] = [('3','y+')]
automata.transition['3'] = [('3','a'),('4','y-')]
automata.transition['4'] = []
automata.start = '0'
automata.end = '4'
automata.last = '4'

sc1.funchk(automata)

sc1.csymtonulllong(automata)

string = 'aaa'

finalgraph = sc1.generateAg(automata,string)

automata.printauto()
for pos, trans in finalgraph.items():
	print ('position : ', pos)
	for start, item in trans.items():
		print ('start node : ', start)
		print ('destinations : ', item)

outputgraph, outputendnode = sc1.finalauto(automata,finalgraph)
#sg.printrawgraph(outputgraph,outputendnode,'output')


outputs = sc1.calcresults(finalgraph, len(string), automata.varconfig)
sc1.printresults(outputs)

tempoutputs = [ [['o','w'],['o','w'],['c','o'],['c','c']], [['o','w'],['c','o'],['c','o'],['c','c']] ]
sc1.printresultsv2(outputs,automata)
sys.exit(1)
print("--- %s seconds ---" % (time.time() - start_time))
#objgraph.show_most_common_types()