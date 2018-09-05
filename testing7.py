import script2rev as sc2
import script3rev as sc3
import scriptgrph as sg
import script1rev as sc1
import threading, time, sys, copy, objgraph, random, inspect, re

#regex = 'a+,<x:b|c>,d*'
#automata = sc2.main(regex)
#automata = sc1.readauto('test.txt')
#sg.printgraph(automata1,'funchk')
#sc1.funchk(automata1)
#print('Before')
#print(automata1.transition)
#
#print('After')
#print(automata1.transition)

automata1 = sc2.automata(0,0,0)
automata1.reset()
automata1.states = ['0','1','2']
automata1.varstates = ['x']
automata1.transition['0'] = [('0','a'),('1','x+')]
automata1.transition['1'] = [('1','a'),('2','x-')]
automata1.transition['2'] = [('2','a')]
automata1.start = '0'
automata1.end = '2'
string = 'aaa'
sc1.funchk(automata1)
#sc1.csymtonulllong(automata1)
#finalgraph = sc1.generateAg(automata1,string)
#outputs = sc1.calcresults(finalgraph, len(string), automata1.varconfig)
#sg.printresultsv2(outputs,automata1,string,1,1)