import script2rev as sc2
import script3rev as sc3
import scriptgrph as sg
import script1rev as sc1
import threading, time, sys, copy, objgraph, random, inspect

start_time = time.time()
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


automata2 = sc2.automata(0,0,0)
automata2.reset()
automata2.states = ['A','B','C','D',"E"]
automata2.varstates = ['x','y']
automata2.transition['A'] = [('A','a'),('B','y+')]
automata2.transition['B'] = [('B','a'),('C','x+')]
automata2.transition['C'] = [('C','a'),('D','y-')]
automata2.transition['D'] = [('D','a'),('E','x-')]
automata2.transition['E'] = [('E','a')]

automata2.start = 'A'
automata2.end = 'E'

string = 'aaa\naaa'
sc1.funchk(automata1)
#sc1.csymtonulllong(automata1)
proauto = sc3.projection(automata1,['x'],1)
sg.printgraph(automata1,'pre2')
sg.printgraph(proauto,'pre')
sys.exit(1)

sc1.funchk(automata2)
sc1.csymtonulllong(automata2)
automata = sc3.joinver1(automata1,automata2)
automata.rename()
string, automata3 = sc3.stringequality(string,1)
#sc1.funchk(automata3)
#sys.exit(1)
#sg.printgraphconfig(automata3,automata3.varconfig,'test1')
sc1.csymtonulllong(automata3)
automata = sc3.joinver1(automata,automata3)
automata.printauto()
automata.rename()
finalgraph = sc1.generateAg(automata,string)
if not finalgraph[-1]:
	print('No results')
	sys.exit(1)
outputgraph, outputendnode = sc1.finalauto(automata,finalgraph)
outputs = sc1.calcresults(finalgraph, len(string), automata.varconfig)
sc1.printresultsv2(outputs,automata,string,1,1)

print("--- %s seconds ---" % (time.time() - start_time))