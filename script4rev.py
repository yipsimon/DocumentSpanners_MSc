import script2rev as sc2
import script3rev as sc3
import scriptgrph as sg
import script1rev as sc1
import threading, time, sys, copy

start_time = time.time()
'''
string1 = 'a'*40
print(string1)
stringequality(string1)
'''

string = 'aaa'
reg = '(a*),[x:(a*)],(a*)'
#automata = sc3.convertregex(reg)

automata = sc2.automata(0,0,0)
automata.reset()
automata.states = automata.states | {'0','1','2'}
automata.varstates = ['x']
automata.transition['0'] = [('0','a'),('1','x+')]
automata.transition['1'] = [('1','a'),('2','x-')]
automata.transition['2'] = [('2','a')]
automata.start = 0
automata.end = 2
automata.last = 2


varconfiglist, key = sc3.functionalcheck(automata)

data = sc3.normalprocess(automata,string,varconfiglist)

sc3.printresults(data)


print("--- %s seconds ---" % (time.time() - start_time))
