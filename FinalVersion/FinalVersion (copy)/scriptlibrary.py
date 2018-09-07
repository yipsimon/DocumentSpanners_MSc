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
	f = open(name, 'r')
	string = f.read()
	f.close()
	return string

def initialprocess(auto):
	sc1.funchk(auto)
	sc1.csymtonulllong(auto)

def endprocess(auto,string,output=0,a=1,b=1,c=1,d=1,printnow=0):
	finalgraph = sc1.generateAg(auto,string)
	#print(finalgraph)
	if not finalgraph[-1]:
		print('No results')
		sys.exit(1)
	if output == 1:
		outputgraph = sg.finalauto(auto,finalgraph)
		sg.printgraph(outputgraph,'outputgraph')
	outputs = sc1.calcresults(finalgraph, len(string), auto.varconfig,auto,printnow)
	sg.printresultsv2(outputs,auto,string,a,b,c,d)

def autoprocess(auto,string,output=0,printnow=0):
	sc1.funchk(auto)
	sc1.csymtonulllong(auto)
	finalgraph = sc1.generateAg(auto,string)
	if not finalgraph[-1]:
		print('No results')
		sys.exit(1)
	if output == 1:
		outputgraph = sg.finalauto(auto,finalgraph)
		sg.printgraph(outputgraph,'outputgraph')
	outputs = sc1.calcresults(finalgraph, len(string), auto.varconfig,auto,printnow)
	sg.printresultsv2(outputs,auto,string,1,1,1,1)

def autostringequ(auto,string,mode,start=1,end=-1,condits=-1,output=0,printnow=0):
	sc1.funchk(auto)
	sc1.csymtonulllong(auto)
	stri, auto2 = sc3.stringequality(string,mode,start,end,condits)
	auto3 = sc3.joinver1(auto,auto2)
	auto3.rename()
	print('ok')
	finalgraph = sc1.generateAg(auto3,stri)
	print('ok')
	if not finalgraph[-1]:
		print('No results')
		sys.exit(1)
	if output == 1:
		outputgraph = sg.finalauto(auto,finalgraph)
		sg.printgraph(outputgraph,'outputgraph')
	outputs = sc1.calcresults(finalgraph, len(string), auto3.varconfig,auto,printnow)
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

def callrename(auto):
	auto.rename()

def callgenAg(auto,string):
	finalgraph = sc1.generateAg(auto,string)
	return finalgraph

def callfinalauto(auto,finalgraph):
	outputgraph = sg.finalauto(auto,finalgraph)
	return outputgraph

def callcalcresults(finalgraph, length, varconfig):
	outputs = sc1.calcresults(finalgraph, length, varconfig)
	return outputs

def calstringeq(string,mode,start=1,end=-1,condits=-1):
	stri, auto = sc3.stringequality(string,mode,start,end,condits)
	return stri, auto

def callunion(auto1,auto2):
	sc3.union(auto1,auto2)

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

def callprintresultsv2(outputs,auto,string,a=0,b=0,c=1,d=0):
	sg.printresultsv2(outputs,auto,string,a,b,c,d)

