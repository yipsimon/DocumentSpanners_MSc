import scriptlibrary as sp
import time, sys, copy, re

#Searching IP addresses and dates with log File

import scriptlibrary as sp
import time, sys, copy, re

#Searching IP addresses with log File

regt = input('usereg?')
reg = int(regt)
if reg == 0:
	automata1 = sp.initauto(0,0,0)
	automata1.reset()
	automata1.states = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17']
	automata1.varstates = ['x']
	automata1.transition['0'] = [('0','(.)'),('1','x+')]
	automata1.transition['1'] = [('2','[0-9]')]
	automata1.transition['2'] = [('3','[0-9]'),('4','[epsi]')]
	automata1.transition['3'] = [('4','[0-9]'),('4','[epsi]')]
	automata1.transition['4'] = [('5','.')]
	automata1.transition['5'] = [('6','[0-9]')]
	automata1.transition['6'] = [('7','[0-9]'),('8','[epsi]')]
	automata1.transition['7'] = [('8','[0-9]'),('8','[epsi]')]
	automata1.transition['8'] = [('9','.')]
	automata1.transition['9'] = [('10','[0-9]')]
	automata1.transition['10'] = [('11','[0-9]'),('12','[epsi]')]
	automata1.transition['11'] = [('12','[0-9]'),('12','[epsi]')]
	automata1.transition['12'] = [('13','.')]
	automata1.transition['13'] = [('14','[0-9]')]
	automata1.transition['14'] = [('15','[0-9]'),('16','[epsi]')]
	automata1.transition['15'] = [('16','[0-9]'),('16','[epsi]')]
	automata1.transition['16'] = [('17','x-')]
	automata1.transition['17'] = [('17','(.)')]
	automata1.start = '0'
	automata1.end = '17'
	automata1.last = 17
if reg == 1:
	regex = '(.)*,<x:[0-9],[0-9]*,.,[0-9],[0-9]*,.,[0-9],[0-9]*,.,[0-9],[0-9]*>,(.)*'
	automata1 = sp.regextoauto(regex)


regex2 = '(.)*,<y:[0-9],[0-9]*,(.),[A-za-z],[A-za-z]*,(.),[0-9],[0-9]*>,(.)*'
automata2 = sp.regextoauto(regex2)

sp.initialprocess(automata1)
sp.initialprocess(automata2)

#sp.callprintgraph(automata1,'test1')
#automata1.printauto()
auto4 = sp.calljoin(automata1,automata2)
sp.callrename(auto4)

string = sp.readlogfile('access_log2')

cod = input('with cond?')
cood = int(cod)
condits = [(lambda s,i,j: True if re.match(r'^[0-9]$',s[j-1]) else (False) ),\
			(lambda s,i,j: True if re.match(r'^[0-9]$',s[j+i-2]) else (False))]
strrt = input('start length')
eeed = input('end length')
start_prctime = time.time()
start_time = time.time()

if cood == 1:
	string2, auto2 = sp.calstringeq(string,1,int(strrt),int(eeed),condits)
if cood == 0:
	string2, auto2 = sp.calstringeq(string,1,int(strrt),int(eeed))

print("stringeq : %s seconds" % (time.time() - start_time))
start_time = time.time()
#sp.callprintgraph(auto2,'test2')
sp.callcepsilon(auto2)
auto = sp.calljoin(auto4,auto2)
print("Join : %s seconds" % (time.time() - start_time))

start_time = time.time()
#sp.callprintgraph(auto,'test3')
sp.callrename(auto)
sp.endprocess(auto,string2,0,0,0,1,1,1)
print("Algorithm : %s seconds" % (time.time() - start_time))
print("Algorithm Total : %s seconds" % (time.time() - start_prctime))
