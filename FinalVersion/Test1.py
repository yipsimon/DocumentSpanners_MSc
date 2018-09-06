import scriptlibrary as sp
import time, sys, copy, re

string = 'a'*3
test = input('Choose Test')
print (test)
testcase = int(test)
if testcase == 1:
	#Test 1 - Input Read File
	automata = sp.callreadauto('test.txt')
	automata.printauto()
	sp.callprintgraph(automata,'t1')
	wait = input('continue...')
	sp.autoprocess(automata,string,1)
if testcase == 2:
	#Test 2 - Input Read Regex
	regex = 'a*,<x:a*,<y:a*>,a*>,a*'
	automata = sp.regextoauto(regex)
	automata.printauto()
	sp.callprintgraph(automata,'t1')
	wait = input('continue...')
	sp.autoprocess(automata,string,1)
if testcase == 3:
	#Test 3 - Input Insert manally
	automata = sp.initauto(0,0,0)
	automata.reset()
	automata.states = ['0','1','2','3','4']
	automata.varstates = ['x','y']
	automata.transition['0'] = [('0','a'),('1','x+')]
	automata.transition['1'] = [('1','a'),('2','y+')]
	automata.transition['2'] = [('2','a'),('3','y-')]
	automata.transition['3'] = [('3','a'),('4','x-')]
	automata.transition['4'] = [('4','a')]
	automata.start = '0'
	automata.end = '4'
	automata.printauto()
	sp.callprintgraph(automata,'t1')
	wait = input('continue...')
	sp.autoprocess(automata,string,1)
if testcase == 4:
	#Test 4 - Spanner Algebra
	#Test 4.1 - Union
	automata1 = sp.initauto(0,0,0)
	automata1.reset()
	automata1.states = ['0','1','2']
	automata1.varstates = ['x']
	automata1.transition['0'] = [('0','a'),('1','x+')]
	automata1.transition['1'] = [('1','a'),('2','x-')]
	automata1.transition['2'] = [('2','a')]
	automata1.start = '0'
	automata1.end = '2'

	automata2 = sp.initauto(0,0,0)
	automata2.reset()
	automata2.states = ['0','1','2']
	automata2.varstates = ['x']
	automata2.transition['0'] = [('0','a'),('1','x+')]
	automata2.transition['1'] = [('1','a'),('2','x-')]
	automata2.transition['2'] = [('2','a')]
	automata2.start = '0'
	automata2.end = '2'

	sp.initialprocess(automata1)
	sp.initialprocess(automata2)
	sp.callunion(automata1,automata2)
	automata1.printauto()
	sp.callprintgraph(automata1,'test')
	#grph1 = sp.callgenAg(automata1,string)
	sp.endprocess(automata1,string,1)

if testcase == 5:
	#Test 4.2 - Projection
	automata1 = sp.initauto(0,0,0)
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
	sp.initialprocess(automata1)
	sp.callprintgraphconfig(automata1,automata1.varconfig,'t1')
	automata1.printauto()
	auto = sp.callprojection(automata1,['x'])
	sp.callprintgraphconfig(auto,auto.varconfig,'t2')
	auto.printauto()
	sp.endprocess(auto,string,1)

if testcase == 6:
	#Test 4.3 - Natural Join
	automata1 = sp.initauto(0,0,0)
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

	automata2 = sp.initauto(0,0,0)
	automata2.reset()
	automata2.states = ['0','1','2','3','4']
	automata2.varstates = ['x','y']
	automata2.transition['0'] = [('0','a'),('1','y+')]
	automata2.transition['1'] = [('1','a'),('2','x+')]
	automata2.transition['2'] = [('2','a'),('3','y-')]
	automata2.transition['3'] = [('3','a'),('4','x-')]
	automata2.transition['4'] = [('4','a')]
	automata2.start = '0'
	automata2.end = '4'

	sp.initialprocess(automata1)
	sp.initialprocess(automata2)
	automata1.printauto()
	sp.callprintgraph(automata1,'test1')
	automata2.printauto()
	sp.callprintgraph(automata2,'test2')
	auto = sp.calljoin(automata1,automata2)
	auto.printauto()
	sp.callprintgraph(auto,'test')
	sp.callrename(auto)
	sp.endprocess(auto,string,1)

if testcase == 7:
	#Test 4.4 - String Equality
	automata1 = sp.initauto(0,0,0)
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
	#sp.autostringequ(automata1,string,['x','y'],0)
	sp.initialprocess(automata1)
	automata1.printauto()
	sp.callprintgraph(automata1,'test1')
	string2, auto2 = sp.calstringeq(string,0)
	sp.callprintgraph(auto2,'test2')
	sp.callcepsilon(auto2)
	auto = sp.calljoin(automata1,auto2)
	sp.callprintgraph(auto,'test3')
	sp.callrename(auto)
	sp.endprocess(auto,string,1)



