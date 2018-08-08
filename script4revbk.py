import script2rev as sc2
import script3rev as sc3
import scriptgrph as sg
import script1rev as sc1
import threading, time, sys, copy, objgraph, random, inspect

start_time = time.time()


'''

reg1 = '(a*),[x:(a*)],(a*)'
reg2 = '(a*),[x:(a*)],(a*)'
automata1 = sc3.convertregex(reg1)
automata2 = sc3.convertregex(reg2)


automata = sc2.automata(0,0,0)
automata.reset()
automata.states = automata.states | {'0','1','2','3','4'}
automata.varstates = ['x','y']
automata.transition['0'] = [('0','a'),('1','x+')]
automata.transition['1'] = [('1','a'),('2','x-')]
automata.transition['2'] = [('2','a'),('3','y+')]
automata.transition['3'] = [('3','a'),('4','y-')]
automata.transition['4'] = [('4','a')]
automata.start = '0'
automata.end = '4'
automata.last = '4'


sys.exit(1)
#data = sc3.projectionver2(automata,string,['x'],varconfiglist,key)

data = sc3.normalprocess(automata,string,varconfiglist)

sc3.printresults(data)

auto2, varconfiglist, key = sc3.joinver1(automata,auto1)



string1 = 'a'*20
print(string1)
print(sys.getsizeof(string1))
print(sys.getsizeof([]*80))
auto1 = sc3.stringequality(string1)
print(sys.getsizeof(auto1))




#varconfiglist, key = sc3.functionalcheck(automata)
print('\nvarconfiglist\n')
print(varconfiglist)
print('\nkey\n')
print(key)
automata.printauto()
sg.printgraph(automata,'g1')

data = sc3.normalprocess(automata,string,varconfiglist)

sc3.printresults(data)

string = 'aaa'
automata1 = sc2.automata(0,0,0)
automata2 = sc2.automata(0,0,0)
automata1.reset()
automata2.reset()
automata1.states = automata1.states | {'0','1','2'}
automata2.states = automata2.states | {'A','B','C'}
automata1.varstates = ['x']
automata2.varstates = ['x']
automata1.transition['0'] = [('0','a'),('1','x+')]
automata1.transition['1'] = [('1','a'),('2','x-')]
automata1.transition['2'] = [('2','a')]
automata2.transition['A'] = [('A','a'),('B','x+')]
automata2.transition['B'] = [('B','a'),('C','x-')]
automata2.transition['C'] = [('C','a')]
automata1.start = '0'
automata1.end = '2'
automata2.start = 'A'
automata2.end = 'C'


automata = sc2.automata(0,0,0)
automata.reset()

automata, varconfiglist, key = sc3.joinver1(automata1,automata2)
for key, edges in automata.transition.items():
	print('key: ', key)
	for edge in edges:
		print(edge)
	print('\n')

sg.printgraph(automata,'g1')

data = sc3.normalprocess(automata,string,varconfiglist)

sc3.printresults(data)

string1 = 'a'*3
auto1 = sc3.stringequality(string1)

string = 'aaa'
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

automata = sc2.automata(0,0,0)
automata.reset()

automata, varconfiglist, key = sc3.joinver1(automata1,automata2)
for key, edges in automata.transition.items():
	print('key: ', key)
	for edge in edges:
		print(edge)
	print('\n')

sg.printgraph(automata,'g1')

data = sc3.normalprocess(automata,string,varconfiglist)

sc3.printresults(data)

string = 'aaa'

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

automata = sc2.automata(0,0,0)
automata.reset()

automata, varconfiglist, key = sc3.joinver1(automata1,automata2)
for key, edges in automata.transition.items():
	print('key: ', key)
	for edge in edges:
		print(edge)
	print('\n')

sg.printgraph(automata,'g1')

automata3 = sc2.automata(0,0,0)
automata3.reset()
automata3.states = automata1.states | {'0','1','2','3','4'}
automata3.varstates = ['x','y']
automata3.transition['0'] = [('0','a'),('1','x+')]
automata3.transition['1'] = [('1','a'),('2','y+')]
automata3.transition['2'] = [('2','a'),('3','x-')]
automata3.transition['3'] = [('3','a'),('4','y-')]
automata3.transition['4'] = [('4','a')]
automata3.start = '0'
automata3.end = '4'


automata0 = sc2.automata(0,0,0)
automata0.reset()

automata0, varconfiglist0, key0 = sc3.joinver1(automata,automata3)
for key, edges in automata0.transition.items():
	print('key: ', key)
	for edge in edges:
		print(edge)
	print('\n')

sg.printgraph(automata0,'g2')

string = 'a'*3
automata1 = sc2.automata(0,0,0)
automata1.reset()
automata1.states = automata1.states | {'0','1','2','3','4'}
automata1.varstates = ['x','y']
automata1.transition['0'] = [('0','a'),('1','x+')]
automata1.transition['1'] = [('1','a'),('2','y+')]
automata1.transition['2'] = [('2','a'),('3','x-')]
automata1.transition['3'] = [('3','a'),('4','y-')]
automata1.transition['4'] = [('4','a')]
automata1.start = '0'
automata1.end = '4'

automata2 = sc3.stringequality(string)

automata = sc2.automata(0,0,0)
automata.reset()

automata, varconfiglist, key = sc3.joinver1(automata1,automata2)
for key, edges in automata.transition.items():
	print('key: ', key)
	for edge in edges:
		print(edge)
	print('\n')

sg.printgraph(automata,'g1')

data = sc3.normalprocess(automata,string,varconfiglist)

sc3.printresults(data)
'''
string = 'aaa'
automata1 = sc2.automata(0,0,0)
automata2 = sc2.automata(0,0,0)
automata1.reset()
automata2.reset()
automata1.states = automata1.states | {'0','1','2'}
automata2.states = automata2.states | {'A','B','C'}
automata1.varstates = ['x']
automata2.varstates = ['y']
automata1.transition['0'] = [('0','a'),('1','x+')]
automata1.transition['1'] = [('1','a'),('2','x-')]
automata1.transition['2'] = [('2','a')]
automata2.transition['A'] = [('A','a'),('B','y+')]
automata2.transition['B'] = [('B','a'),('C','y-')]
automata2.transition['C'] = [('C','a')]
automata1.start = '0'
automata1.end = '2'
automata2.start = 'A'
automata2.end = 'C'

automata0 = sc2.automata(0,0,0)
automata0.reset()

automata0, varconfiglist0, key0 = sc3.joinver1(automata1,automata2)
for key, edges in automata0.transition.items():
	print('key: ', key)
	for edge in edges:
		print(edge)
	print('\n')

sg.printgraph(automata0,'g2')

data = sc3.normalprocess(automata0,string,varconfiglist0)

sc3.printresults(data)

print("--- %s seconds ---" % (time.time() - start_time))
objgraph.show_most_common_types()