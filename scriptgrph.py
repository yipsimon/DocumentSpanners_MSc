import graphviz as gv
import script1rev as sc1
import functools
import threading, time, sys, copy, re
import texttable as txttab 

import functools

#graphviz function for adding multiple nodes
def add_nodes(graph, nodes):
    for n in nodes:
        if isinstance(n, tuple):
            graph.node(n[0], **n[1])
            
        else:
            graph.node(n)
    return graph

#graphviz function for adding multiple edges
def add_edges(graph, edges):
    for e in edges:
        if isinstance(e[0], tuple):
            graph.edge(*e[0], **e[1])
        else:
            graph.edge(*e)
    return graph

#Output a graph by taking in an automaton object, reading the transitions edges
def printgraph(auto,name):
	digraph = functools.partial(gv.Digraph, filename=name)
	g = digraph()
	g.attr(rankdir='LR', size='8,5')
	g.attr('node', shape='doublecircle')
	print ('end',str(auto.end))
	add_nodes(g, [str(auto.end)])
	g.attr('node', shape='circle')
	edges = []
	for key, item in auto.transition.items():
		for line in item:
			if line[1] == '[epsi]':
				value = '&epsilon;'
			else: 
				value = line[1]
			tup = ((str(key),str(line[0])),{'label':str(value)})
			edges.append(tup)
	
	add_edges(g, edges)
	g.format = 'pdf'
	g.view()

def printrawgraph(graph,end,name):
	digraph = functools.partial(gv.Digraph, filename=name)
	g = digraph()
	g.attr(rankdir='LR', size='8,5')
	g.attr('node', shape='doublecircle')
	print ('end',end)
	add_nodes(g, [str(end)])
	g.attr('node', shape='circle')
	edges = []
	for key, item in graph.items():
		for line in item:
			if line[1] == '[epsi]':
				value = '&epsilon;'
			else: 
				value = line[1]
			tup = ((str(key),str(line[0])),{'label':str(value)})
			edges.append(tup)
	
	add_edges(g, edges)
	g.format = 'pdf'
	g.view()

def printgraphconfig(auto,finallist,name):
	digraph = functools.partial(gv.Digraph, filename=name)
	g = digraph()
	g.attr(rankdir='LR', size='8,5')
	g.attr('node', shape='doublecircle')
	print ('end',auto.end)
	add_nodes(g, [str(auto.end)])
	g.attr('node', shape='circle')
	edges = []
	for key, item in auto.transition.items():
		for line in item:
			if line[1] == '[epsi]':
				value = '&epsilon;'
			else: 
				value = line[1]
			tup = ((str(key),str(line[0])),{'label':str(value)+','+str(finallist[line[0]])})
			edges.append(tup)
	
	add_edges(g, edges)
	g.format = 'pdf'
	g.view()

"""
Create only the transition edges dictionary of the automata strictly for displaying the Ag graph in a proper format.
Input: Automata object, Graph (format: {name1: {name1.1: setvalues, name1.2: setvalues,...},...})
Output, Graph (format: {startnode: [(endnode1,edgevalue),(endnode2,edgevalue),...],...}), end node
"""
def finalauto(auto,graph):
	finalgraph = {}
	final = -1
	for positions, nodes in graph.items():
		for begining, ending in nodes.items():
			if positions == -1:
				start = 'q0'
			else:
				start = (positions, begining)

			sc1.ifnotlv1(finalgraph,str(start))
			for edge in ending:
				value = auto.varconfig[edge]
				end = (positions+1, edge)
				tup = (end,value)
				finalgraph[str(start)].append(tup)

			if positions > final:
				final = positions

	endnode = (final+1,str(auto.end))

	return finalgraph, endnode

"""
Function to print results only in waiting, open and close format (w,o,c format)
"""
def printresults(listofoutputs):
	print ('\n results')
	for i in range(len(listofoutputs)):
		print (listofoutputs[i])

"""
Function to print results in a table format
"""
def printresultsv2(listofoutputs,auto,string,showstring=0,showconfig=0,showposstr=0):
	print ('\nResults Table')
	key1 = {}	#key correspond from int to w,o,c format
	key2 = {}	#key correspond from int to string format
	key3 = {}	#key correspond from int to varstate positions format x:[1,2], y:[2,4] etc
	
	tempkey = {}	#Temporary store varpos value 
	for item in auto.varstates:
		tempkey[str(item)] = []
		
	#Initialise and link keys
	for i in range(len(listofoutputs)):
		key1[i] = listofoutputs[i]
		key3[i] = {}
		key2[i] = {}

	#Iterate outputs
	for i in range(len(listofoutputs)):
		tempkey2 = []	#Termporary store string format
		#Iterate within output of w.o.c format
		for j in range(len(listofoutputs[i])):
			#Check for changes
			if j == 0 or listofoutputs[i][j] != listofoutputs[i][j-1]:
				#Iterate within w,o,c format i.e [w,w],[w,o],..., 
				for k in range(len(listofoutputs[i][j])):
					if listofoutputs[i][j][k] == 'o':
						if j == 0:
							tempkey[auto.varstates[k]].append(j+1) #+1 since we start from 0 and want 1 for pos
							tempkey2.append(auto.varstates[k]+'+')
						else:
							#Compare individual variable states
							if listofoutputs[i][j-1][k] != listofoutputs[i][j][k]:
								tempkey[auto.varstates[k]].append(j+1)
								tempkey2.append(auto.varstates[k]+'+')
					
					elif listofoutputs[i][j][k] == 'c':
						if j == 0:
							#Closed immediately
							tempkey[auto.varstates[k]].append(j+1)
							tempkey[auto.varstates[k]].append(j+1)
							tempkey2.append(auto.varstates[k]+'+')
							tempkey2.append(auto.varstates[k]+'-')
						else:
							if listofoutputs[i][j-1][k] != listofoutputs[i][j][k]:
								tempkey[auto.varstates[k]].append(j+1)
								tempkey2.append(auto.varstates[k]+'-')
								#Closed immediately if length == 1 otherwise it would have been == 2
								if len(tempkey[auto.varstates[k]]) == 1:
									tempkey[auto.varstates[k]].append(j+1)
									tempkey2.remove(auto.varstates[k]+'-')
									tempkey2.append(auto.varstates[k]+'+')
									tempkey2.append(auto.varstates[k]+'-')
			#Add placeholder letter for string
			if j != len(listofoutputs[i])-1:
				tempkey2.append('a')
		#Convert varpos format to tuple
		for key, item in tempkey.items():
			tempkey[key] = tuple(item)
		#Add to resp keys
		key3[i] = copy.deepcopy(tempkey)
		key2[i] = copy.deepcopy(tempkey2)
		#Initialise
		for item in auto.varstates:
			tempkey[str(item)] = []
	
	tab = txttab.Texttable()
	headings = ['No.']
	if showstring == 1:
		headings.append('String')
	if showconfig == 1:
		headings.append('w,o,c format')
	for v in range(len(auto.varstates)):
		headings.append(auto.varstates[v])
	if showposstr == 1:
		for v in range(len(auto.varstates)):
			headings.append(auto.varstates[v]+'str')

	tab.header(headings)
	for i in range(len(listofoutputs)):
		temp = [i]
		if showstring == 1:
			temp.append(key2[i])
		if showconfig == 1:
			temp.append(key1[i])
		#temp = [i,key2[i],key1[i]]
		for v in range(len(auto.varstates)):
			temp.append(key3[i][auto.varstates[v]])
		if showposstr == 1:
			for v in range(len(auto.varstates)):
				start = int(key3[i][auto.varstates[v]][0])-1
				end = int(key3[i][auto.varstates[v]][1])-1
				#print('s',start,'e',end)
				temp2 = string[start:end]
				temp.append([temp2])
		tab.add_row(temp)
	
	s = tab.draw()
	print(s)

