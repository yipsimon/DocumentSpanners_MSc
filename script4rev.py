import script2rev as sc2
import script3rev as sc3
import scriptgrph as sg
import script1rev as sc1
import threading, time, sys, copy, objgraph, random, inspect

start_time = time.time()

automata1 = sc2.automata(0,0,0)
automata2 = sc2.automata(0,0,0)
automata1.reset()
automata2.reset()
automata1.states = automata1.states | {'0','1','2','3','4'}
automata2.states = automata2.states | {'A','B','C','D',"E"}
automata1.varstates = ['x','y']
automata2.varstates = ['x','y']
automata1.transition['0'] = [('0','a'),('1','x+')]
automata1.transition['1'] = [('1','a'),('2','y+')]
automata1.transition['2'] = [('2','a'),('3','x-')]
automata1.transition['3'] = [('3','a'),('4','y-')]
automata1.transition['4'] = [('4','a')]
automata2.transition['A'] = [('A','a'),('B','y+')]
automata2.transition['B'] = [('B','a'),('C','x+')]
automata2.transition['C'] = [('C','a'),('D','y-')]
automata2.transition['D'] = [('D','a'),('E','x-')]
automata2.transition['E'] = [('E','a')]
automata1.start = '0'
automata1.end = '4'
automata2.start = 'A'
automata2.end = 'E'

sc1.funchk(automata1)
sc1.csymtonulllong(automata1)
sc1.funchk(automata2)
sc1.csymtonulllong(automata2)
automata = sc3.joinver1(automata1,automata2)
automata.rename()
automata.printauto()
sg.printgraph(automata,'output')

automata3 = sc2.automata(0,0,0)
automata3.reset()
automata3.states = automata3.states | {'a','b','c'}
automata3.varstates = ['z']
automata3.transition['a'] = [('a','a'),('b','z+')]
automata3.transition['b'] = [('b','a'),('c','z-')]
automata3.transition['c'] = [('c','a')]
automata3.start = 'a'
automata3.end = 'c'
sc1.funchk(automata3)
sc1.csymtonulllong(automata3)
automata = sc3.joinver1(automata,automata3)
#sg.printgraph(automata,'output2')

automata.rename()
automata.printauto()
sg.printgraph(automata,'output2')



sys.exit(1)
'''

finalgraph = sc1.generateAg(automata,string)

automata.printauto()
for pos, trans in finalgraph.items():
	print ('position : ', pos)
	for start, item in trans.items():
		print ('start node : ', start)
		print ('destinations : ', item)

outputgraph, outputendnode = sc1.finalauto(automata,finalgraph)
sg.printrawgraph(outputgraph,outputendnode,'output')
automata = sc3.projectionver1(automata,string,['x','z'])

outputs = sc1.calcresults(finalgraph, len(string), automata.varconfig)
sc1.printresults(outputs)





tempoutputs = [ [['o','w'],['o','w'],['c','o'],['c','c']], [['o','w'],['c','o'],['c','o'],['c','c']] ]
sc1.printresultsv2(outputs,automata)
sys.exit(1)
'''
print("--- %s seconds ---" % (time.time() - start_time))
#objgraph.show_most_common_types()