import graphviz as gv
import script1 as sc1
import script2 as sc2
import script3 as sc3
import scriptgrph as sg
import functools
import threading, time, sys, copy, re
import texttable as txttab 

import functools

def callreadauto(fname):
	auto = sc1.readauto(fname)
	return auto

def regextoauto(reg):
	auto = sc2.main(reg)
	return auto

def initauto(a,b,c):
	auto = sc2.automata(a,b,c)
	return auto

def readlogfile(name):
	f = open('access_log2', 'r')
	string = f.read()
	f.close()
	return string

def initialprocess(auto):
	sc1.funchk(auto)
	sc1.csymtonulllong(auto)

def endprocess(auto,string,output=0):
	finalgraph = sc1.generateAg(auto,string)
	if not finalgraph[-1]:
		print('No results')
		sys.exit(1)
	if output == 1:
		outputgraph = sg.finalauto(auto,finalgraph)
		sg.printgraph(outputgraph,'outputgraph')
	outputs = sc1.calcresults(finalgraph, len(string), auto.varconfig)
	sg.printresultsv2(outputs,auto,string,1,1,1,1)

def autoprocess(auto,string,output=0):
	sc1.funchk(auto)
	sc1.csymtonulllong(auto)
	finalgraph = sc1.generateAg(auto,string)
	if not finalgraph[-1]:
		print('No results')
		sys.exit(1)
	if output == 1:
		outputgraph = sg.finalauto(auto,finalgraph)
		sg.printgraph(outputgraph,'outputgraph')
	outputs = sc1.calcresults(finalgraph, len(string), auto.varconfig)
	sg.printresultsv2(outputs,auto,string,1,1,1,1)

def autostringequ(auto,string,variables,mode,start=1,end=-1,condits=-1,output=0):
	sc1.funchk(auto)
	sc1.csymtonulllong(auto)
	stri, auto2 = sc3.stringequality(string,variables,mode,start,end,condits)
	auto3 = sc3.joinver1(auto,auto2)
	finalgraph = sc1.generateAg(auto3,stri)
	if not finalgraph[-1]:
		print('No results')
		sys.exit(1)
	if output == 1:
		outputgraph = sg.finalauto(auto,finalgraph)
		sg.printgraph(outputgraph,'outputgraph')
	outputs = sc1.calcresults(finalgraph, len(string), auto3.varconfig)
	sg.printresultsv2(outputs,auto,string,1,1,1,1)

def callfunck(auto):
	sc1.funchk(auto)

def callcepsilon(auto):
	sc1.csymtonulllong(auto)

def callprojection(automata,listofprojections,before=0):
	auto = sc3.projection(automata,listofprojections,before)
	return auto

def calljoin(auto1,auto2):
	auto = sc3.joinver1(auto1,auto2)
	return auto

def callgenAg(auto,string):
	finalgraph = sc1.generateAg(auto,string)
	return finalgraph

def callfinalauto(auto,finalgraph):
	outputgraph = sg.finalauto(auto,finalgraph)
	return outputgraph

def callcalcresults(finalgraph, length, varconfig):
	outputs = sc1.calcresults(finalgraph, length, varconfig)
	return outputs

def calstringeq(string,variables,mode,start=1,end=-1,condits=-1):
	stri, auto = sc3.stringequality(string,variables,mode,start,end,condits)
	return stri, auto

def callunion(auto1,auto2,f1=0,f2=0,string=0,mode=0):
	sc3.union(auto1,auto2,f1,f2,string,mode)

def callconcat(auto1,auto2):
	sc3.concat(auto1,auto2)

def callalpha(listings,varstates):
	auto = sc3.alpha(listings,varstates)
	return auto

def callprintgraph(auto,name):
	sg.printgraph(auto,name)

def callprintrawgraph(graph,end,name):
	sg.printrawgraph(graph,end,name)

def callprintgraphconfig(auto,finallist,name):
	sg.printgraphconfig(auto,finallist,name)

def callprintresultsv2(outputs,auto,string):
	sg.printresultsv2(outputs,auto,string,1,1,1,1)


'''
print(grph1)
u1 = sp.callfinalauto(automata1,grph1)
u1.printauto()
u2 = sp.callfinalauto(automata2,grph2)
u2.printauto()
ref = {}
i = 0
for stat in u1.states:
	if stat != 'q0' and (not stat[1] in ref):
		ref[str(stat[1])] = i
		i += 1
print(ref)
tempst = ['q0']
print(i)
for item in u1.states:
	if item != 'q0':
		le = (int(item[0]),ref[str(item[1])])
		tempst.append(le)

print (tempst)
temptr = {}
temptr['q0'] = []
for item in u1.transition.keys():
	if item != 'q0':
		temptr[(int(item[0]),ref[str(item[1])])] = []
		for item2 in u1.transition[item]:
			temptr[(int(item[0]),ref[str(item[1])])].append( ((item2[0][0],ref[str(item2[0][1])]),item2[1]) )
	else:
		for item2 in u1.transition[item]:
			temptr['q0'].append( ((item2[0][0],ref[str(item2[0][1])]),item2[1]) )
newv = {}
for item in u1.varconfig.keys():
	newv[ref[str(item)]] = u1.varconfig[item]
u1.varconfig = newv
te = u1.end
u1.end = (te[0],ref[str(te[1])])
u1.states = tempst
u1.transition = temptr
u1.last = i
u1.printauto()
sp.callprintgraph(u1,'t')


ref2 = {}
for stat in u1.states:
	if stat != 'q0' and (not stat[1] in ref):
		ref2[str(stat[1])] = i
		i += 1


tempst = ['q0']
print(i)
for item in u2.states:
	if item != 'q0':
		le = (int(item[0]),ref2[str(item[1])])
		u1.states.append(le)

for item in u2.transition.keys():
	if item != 'q0':
		u1.transition[(int(item[0]),ref2[str(item[1])])] = []
		for item2 in u2.transition[item]:
			if item2[0] == u2.end:
				u1.transition[(int(item[0]),ref2[str(item[1])])].append( ((u1.end[0],u1.end[1]),item2[1]) )
			else:
				u1.transition[(int(item[0]),ref2[str(item[1])])].append( ((item2[0][0],ref2[str(item2[0][1])]),item2[1]) )
	else:
		for item2 in u2.transition[item]:
			if item2[0] == u2.end:
				u1.transition['q0'].append( ((u1.end[0],u1.end[1]),item2[1]) )
			else:
				u1.transition['q0'].append( ((item2[0][0],ref2[str(item2[0][1])]),item2[1]) )

for item in u2.varconfig.keys():
	print(ref2[str(item)])
	u1.varconfig[ref2[str(item)]] = u2.varconfig[item]

u1.printauto()
sp.callprintgraph(u1,'t')
sys.exit(1)
fgrph = {}
for pos in u1.transition.keys():
	if pos == 'q0':
		fgrph[-1] = {}
		fgrph[-1]['0'] = set([])
		for item in u1.transition['q0']:
			fgrph[-1]['0'].add(str(item[0][1]))
	else:
		if not pos[0] in fgrph:
			fgrph[pos[0]] = {}
		fgrph[pos[0]][pos[1]] = set([])
		print(u1.transition[pos])
		for item in u1.transition[pos]:

			fgrph[pos[0]][pos[1]].add(str(item[0][1]))


print(fgrph)

outputs = sp.callcalcresults(fgrph,len(string),u1.varconfig)
print(outputs)
sp.callprintresultsv2(outputs,u1,string)

'''