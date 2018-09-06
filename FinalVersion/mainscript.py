import scriptlibrary as sp
import time, sys, copy

string = 'a'*3
'''
#Test 1 - Input Read File
automata = sp.callreadauto('test.txt')
automata.printauto()
sp.autoprocess(automata,string,0)
'''
'''
#Test 2 - Input Read Regex
regex = 'a*,<x:a*>,a*'
automata = sp.regextoauto(regex)
automata.printauto()
sp.autoprocess(automata,string,1)
'''
'''
#Test 3 - Input Insert manally
automata = sp.initauto(0,0,0)
automata.reset()
automata.states = ['0','1','2']
automata.varstates = ['x']
automata.transition['0'] = [('0','a'),('1','x+')]
automata.transition['1'] = [('1','a'),('2','x-')]
automata.transition['2'] = [('2','a')]
automata.start = '0'
automata.end = '2'
automata.printauto()
sp.autoprocess(automata,string,0)
'''

#Test 4 - Spanner Algebra
'''
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
grph1 = sp.callgenAg(automata1,string)
grph2 = sp.callgenAg(automata2,string)


sp.callunion(automata1,automata2)
sp.callprintgraph(automata1,'test')

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
automata1.printauto()
auto = sp.callprojection(automata1,['x'])
auto.printauto()

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
auto = sp.calljoin(automata1,automata2)
sp.callprintgraph(auto,'test')

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
sp.autostringequ(automata1,string,['x','y'],0)
'''

#Example 1




'''
string = 'aaa'
sp.initialprocess(automata1)
automata1.printauto()
'''

#automata1.printauto()
#sp.printgraph(automata1,'test00')
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
'''