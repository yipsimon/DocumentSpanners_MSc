import scriptgrph as sp
import time, sys, copy

#Read File
automata1 = sp.callreadauto('test.txt')
#Or Read Regex
regex = 'a*,<x:a*,<y:a*>,a*>,a*'
automata1 = sp.regextoauto(regex)
#Or insert manally
automata1 = sp.initauto(0,0,0)
automata1.reset()
automata1.states = ['0','1','2','3','4']
automata1.varstates = ['x','y']
automata1.transition['0'] = [('0','a'),('1','x+')]
automata1.transition['1'] = [('1','a'),('2','y+')]
automata1.transition['2'] = [('2','a'),('3','y-')]
automata1.transition['3'] = [('3','a'),('4','x-')]
automata1.transition['4'] = [('4','a')]
automata1.start = '0'
automata1.end = '4'

string = 'aaa'
sp.initialprocess(automata1)
automata1.printauto()


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