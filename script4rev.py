import script2rev as sc2
import script3rev as sc3
import scriptgrph as sg
import script1rev as sc1
import threading, time, sys, copy

start_time = time.time()
'''
string1 = 'a'*3
print(string1)
sc3.stringequality(string1)


string = 'aaa'
reg1 = '(a*),[x:(a*)],(a*)'
reg2 = '(a*),[x:(a*)],(a*)'
automata1 = sc3.convertregex(reg)
automata2 = sc3.convertregex(reg2)


automata = sc2.automata(0,0,0)
automata.reset()
automata.states = automata.states | {'0','1','2'}
automata.varstates = ['x']
automata.transition['0'] = [('0','a'),('1','x+')]
automata.transition['1'] = [('1','a'),('2','x-')]
automata.transition['2'] = [('2','a')]
automata.start = '0'
automata.end = '2'
automata.last = '2'
'''
string = 'aaa'
automata1 = sc2.automata(0,0,0)
automata2 = sc2.automata(0,0,0)
automata1.reset()
automata2.reset()
automata1.states = automata1.states | {'0','1','2'}
automata2.states = automata2.states | {'a','b','c'}
automata1.varstates = ['x']
automata2.varstates = ['y']
automata1.transition['0'] = [('0','a'),('1','x+')]
automata1.transition['1'] = [('1','a'),('2','x-')]
automata1.transition['2'] = [('2','a')]
automata2.transition['a'] = [('a','a'),('b','y+')]
automata2.transition['b'] = [('b','a'),('c','y-')]
automata2.transition['c'] = [('c','a')]
automata1.start = '0'
automata1.end = '2'
automata2.start = 'a'
automata2.end = 'c'

automata = sc2.automata(0,0,0)
automata.reset()

automata, varconfiglist, key = sc3.joinver1(automata1,automata2)

#varconfiglist, key = sc3.functionalcheck(automata)
print('\nvarconfiglist\n')
print(varconfiglist)
print('\nkey\n')
print(key)
automata.printauto()
sg.printgraph(automata,'g2')
sys.exit(1)
#data = sc3.projectionver2(automata,string,['x'],varconfiglist,key)

data = sc3.normalprocess(automata,string,varconfiglist)

sc3.printresults(data)

print("--- %s seconds ---" % (time.time() - start_time))
