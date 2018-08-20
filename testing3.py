import script2rev as sc2
import script3rev as sc3
import scriptgrph as sg
import script1rev as sc1
import threading, time, sys, copy, objgraph, random, inspect, re

start_time = time.time()
'''
automata1 = sc2.automata(0,0,0)
automata1.reset()
automata1.states = ['0','1','2','3','4','5','6','7','8','9']
automata1.varstates = ['x']
automata1.transition['0'] = [('0','(.)'),('1','x+')]
automata1.transition['1'] = [('1','[0-9]'),('2','[0-9]')]
automata1.transition['2'] = [('3','.')]
automata1.transition['3'] = [('3','[0-9]'),('4','[0-9]')]
automata1.transition['4'] = [('5','.')]
automata1.transition['5'] = [('5','[0-9]'),('6','[0-9]')]
automata1.transition['6'] = [('7','.')]
automata1.transition['7'] = [('7','[0-9]'),('8','[0-9]')]
automata1.transition['8'] = [('9','x-')]
automata1.transition['9'] = [('9','(.)')]
automata1.start = '0'
automata1.end = '9'
automata1.last = 9
'''
automata1 = sc2.automata(0,0,0)
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
sc1.funchk(automata1)
sc1.csymtonulllong(automata1)

f = open('access_log2', 'r')
string = f.read()
f.close()
#with open('access_log2') as f:
#readdata = ''
#for line in f:
#	readdata = readdata + line

#print(len(string))
count = 0
#string = 'aaa\naaaa'
stor = []
for i in range(12,13):
	for j in range(1,len(string)+2-i):
		skip = 1
		for k in range(j+1,len(string)+2-i):
			if skip == 0:
				if string[k+i-2:k+i-1] == '\n':
					skip = 1
				elif string[j-1:j+i-1] == string[k-1:k+i-1]:
					if count == 0:
						autostring, deststring, shortcut = sc3.createauto((i,j,k),string,['x','y'],0)	
					else:
						autostring,deststring,shortcut = sc3.combinationauto(autostring,deststring,shortcut,(i,j,k),string,['x','y'])
					count += 1
					stor.append( (j,string[j-1:j+i-1],k,string[k-1:k+i-1]) )
			if skip == 1:
				if string[k-1:k] == '\n':
					skip = 0

print (count)
#print("--- %s seconds ---" % (time.time() - start_time))
#start_time = time.time()
'''
for item in stor:
	print (repr(item))
'''
autostring.start = str(autostring.start)
autostring.end = str(autostring.end)
autostring.states = []
for i in range(autostring.last+1):
	autostring.states.append(str(i))

for key, items in autostring.transition.items():
	if not isinstance(items, list):
		autostring.transition[key] = [items]

autostring.tostr()
#print("--- %s seconds ---" % (time.time() - start_time))
#start_time = time.time()
sc1.funchk(autostring)
sc1.csymtonulllong(autostring)
#sg.printgraphconfig(autostring,autostring.varconfig,'test1')
#sys.exit(1)
automata = sc3.joinver1(automata1,autostring)
#print("--- %s seconds ---" % (time.time() - start_time))
#start_time = time.time()
'''
positems = []
for key, items in automata.transition.items():
	for item in items:
		if not item[1] in positems:
			positems.append(item[1])
for item in positems:
	print(item)
'''
#automata.rename()
#automata.printauto()
string = string.replace('\n','')
#print(string)

finalgraph = sc1.generateAg(automata,string)

#print('finalgraph',finalgraph)
#print('autoend',automata.end)

#sys.exit(1)
outputgraph, outputendnode = sc1.finalauto(automata,finalgraph)
outputs = sc1.calcresults(finalgraph, len(string), automata.varconfig)
sc1.printresultsv2(outputs,automata,string)



print("--- %s seconds ---" % (time.time() - start_time))
sys.exit(1)

'''
for line in f:
	print(line)

whole = ''
for j in readdata:
	for k in readdata:

	whole = whole+let
	ip = '64.242.88.10'
	if let == '\n':
		print(whole)
		whole = ''

'''


sys.exit(1)