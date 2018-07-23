import script2 as sc2
import functools
import graphviz as gv
import threading, time, random, traceback, uuid, json, Queue, sys, copy

def add_nodes(graph, nodes):
    for n in nodes:
        if isinstance(n, tuple):
            graph.node(n[0], **n[1])
            
        else:
            graph.node(n)
    return graph

def add_edges(graph, edges):
    for e in edges:
        if isinstance(e[0], tuple):
            graph.edge(*e[0], **e[1])
        else:
            graph.edge(*e)
    return graph

def printgraph(auto,mode):
	if mode == 1:
		name = 'automata'
	elif mode == 2:
		name = 'Agraph'
	digraph = functools.partial(gv.Digraph, filename=name, format='dot')
	g = digraph()
	g.attr(rankdir='LR', size='8,5')
	g.attr('node', shape='doublecircle')
	
	add_nodes(g, [str(auto.end)])
	g.attr('node', shape='circle')
	edges = []
	for key, item in auto.transition.iteritems():
		for line in item:
			if line[1] == '[epsi]':
				value = '&epsilon;'
			else: 
				value = line[1]
			tup = ((str(key),str(line[0])),{'label':str(value)})
			edges.append(tup)
	
	add_edges(g, edges)
	#print g
	g.view()


def readauto():
    #filename = raw_input('Please enter a file name: ')
    fname = 'test'+'.txt'
    f = open(fname, 'r')
    auto = sc2.automata(0,0,0)
    auto.reset()
    for line in f:
    	temp = line.split(';')
    	del temp[-1]
    	for item in temp:
    		item = item.split(',')
    		if not auto.transition.has_key(int(item[0])):
    			auto.transition[int(item[0])] = []
    		if not auto.transition.has_key(int(item[1])):
    			auto.transition[int(item[1])] = []
    		tup = (int(item[1]),item[2])
    		auto.transition[int(item[0])].append(tup)
    		auto.states = auto.states | {int(item[0]),int(item[1])}
    		if str(item[2][-1]) == '+':
    			auto.varstates.add(str(item[2][0]))
    		if item[0] == 0:
    			auto.start = item[0]
    		if item[1] > auto.end:
    			auto.end = item[1]

    f.close()
    return auto

def functionalitychk(auto):
	openlist = {}
	closelist = {}
	varconfig = {}
	temp = []
	for config in auto.varstates:
		temp.append(config)

	for item in auto.states:
		openlist[item] = set([])
		closelist[item] = set([])
		varconfig[item] = []

		for config in auto.varstates:
			varconfig[item].append('w')

	seenlist = {auto.start}
	todolist = {auto.start}
		

	print 'openlist',openlist
	print 'closelist',closelist
	print 'varconfig',varconfig
	print 'seenlist',seenlist
	print 'todolist',todolist
	print 'temp', temp
	print 'varstates',auto.varstates

	while todolist:
		origin = todolist.pop()
		print 'origin',origin
		for item in auto.transition[int(origin)]:
			dest = item[0]
			letter = item[1][0]
			op = openlist[dest]
			oq = openlist[origin]
			cp = closelist[dest]
			cq = closelist[origin]
			if item[1][-1] == '+':
				if oq & {letter}:
					print 'not function already in open'
					sys.exit(1)
				if seenlist & {dest}:
					if op != (oq | {letter}) or cp != cq:
						print 'not function different states for one node'
						sys.exit(1)
				else:
					seenlist.add(dest)
					todolist.add(dest)
					openlist[dest] = (openlist[origin] | {letter})
					closelist[dest] = closelist[origin]
					for k in range(len(temp)):
						if temp[k] == letter:
							varconfig[dest] = []
							varconfig[dest].extend(varconfig[origin])
							varconfig[dest][k] = 'o'

			elif item[1][-1] == '-':
				if {letter} - oq or cq & {letter}:
					print 'not function already in close, not opened'
					sys.exit(1)
				if seenlist & {dest}:
					if op != oq  or cp != (cq | {letter}):
						print 'not function different states for one node'
						sys.exit(1)
				else:
					seenlist.add(dest)
					todolist.add(dest)
					openlist[dest] = openlist[origin] 
					closelist[dest] = (closelist[origin] | {letter})
					for k in range(len(temp)):
						if temp[k] == letter:
							varconfig[dest] = []
							varconfig[dest].extend(varconfig[origin])
							varconfig[dest][k] = 'c'

			else:
				if seenlist & {dest}:
					if op != oq  or cp != cq:
						print 'not function different states for one node'
						sys.exit(1)
				else:
					seenlist.add(dest)
					todolist.add(dest)
					openlist[dest] = openlist[origin] 
					closelist[dest] = closelist[origin]	
					varconfig[dest] = varconfig[origin]

	return openlist, closelist, varconfig


print 'Welcome to prototype 1, select your functions:'
print 'Option 1 : enter regex formula'
print 'Option 2 : Read from existing file'
x = input("Select: ")
while 1:
	if x == 1:
		autom = sc2.main()
		print 'automaton',autom.printauto()
		break
	elif x == 2:
		autom = readauto()
		print 'automaton'
		autom.printauto()
		break
	else:
		print 'error try again'

inputprint = input('Print Graph: yes=0, no=any \n')
if not inputprint:
	printgraph(autom,1)
inputstr = raw_input('Enter your string: ')

oplist, clolist, varstates = functionalitychk(autom)

print 'openlist',oplist
print 'closelist',clolist
print 'varstates',varstates

graphing = {}
regraph = {}

for i in range(-1,len(inputstr)):
	graphing[i] = {}

for i in range(1,len(inputstr)+1):
	regraph[i] = {}

def chkexist(graph,cpos,node):
	if not graph[cpos].has_key(node):
		graph[cpos][node] = []

def add(graph,cpos,start,edge):
	temp = set(graph[cpos][start])
	temp = temp | {edge}
	graph[cpos][start] = list(temp)


def repeat(auto,graph,reverse,node,start,cpos,mode):
	listedges = auto.transition[node]
	ext = ['+','-']
	for edge in listedges:
		if mode == 1:
			if int(edge[0]) == int(auto.end):
				chkexist(graph,cpos,node)
				chkexist(reverse,cpos+1,edge[0])
				add(graph,cpos,start,edge[0])
				#graph[cpos][start].append(edge[0])
				reverse[cpos+1][edge[0]].append(start)	
			elif (edge[1][-1] in ext) or (edge[1] == '[epsi]'):
				repeat(auto,graph,reverse,edge[0],start,cpos,mode)
			'''
			if edge[1][-1] == '+':
				print 'find sym0'
				repeat(auto,graph,reverse,edge[0],start,cpos,mode)
			elif (edge[1][-1] == '-') or (edge[1] == '[epsi]'):
				if edge[0] == auto.end:
					chkexist(graph,cpos,node)
					chkexist(reverse,cpos+1,edge[0])
					graph[cpos][start].append(edge[0])
					reverse[cpos+1][edge[0]].append(start)	
					print 'find sym1'
				else:
					repeat(auto,graph,reverse,edge[0],start,cpos,mode)
			'''
		else:
			if (edge[1][-1] in ext) or (edge[1] == '[epsi]'):
				chkexist(graph,cpos,node)
				chkexist(reverse,cpos+1,edge[0])
				add(graph,cpos,start,edge[0])
				#graph[cpos][start].append(edge[0])
				reverse[cpos+1][edge[0]].append(start)
				repeat(auto,graph,reverse,edge[0],start,cpos,mode)


def findletter(auto,graph,reverse,inputletter,cpos,mode):
	find = 0
	if cpos == 0:
		listnodes = auto.states
	else:
		listnodes = reverse[cpos].keys()

	for node in listnodes:
		print 'node', node
		listedges = auto.transition[node]
		print 'listedges',listedges
		for edge in listedges:
			print 'edge',edge
			if edge[1] == inputletter[cpos]:
				print 'edge = letter'
				chkexist(graph,cpos,node)
				chkexist(reverse,cpos+1,edge[0])
				if mode == 1:
					print 'mode 1'
					if int(edge[0]) == int(auto.end):
						#graph[cpos][node].append(edge[0])
						add(graph,cpos,start,edge[0])
						reverse[cpos+1][edge[0]].append(node)
					else:
						repeat(auto,graph,reverse,node,node,cpos,mode)
					find = 1
				else:
					print 'mode 0'
					#graph[cpos][node].append(edge[0])
					add(graph,cpos,node,edge[0])
					print 'graph, pos',cpos,'node',node,'edge',edge[0]
					reverse[cpos+1][edge[0]].append(node)
					repeat(auto,graph,reverse,node,node,cpos,mode)
					find = 1
		print 'find',find
		if find == 0 and cpos != 0:
			print 'find == 0'
			links = reverse[cpos][node]
			print 'links',links
			for link in links:
				graph[cpos-1][link].remove(node)
			print 'pos',cpos-1, 'graph',graph[cpos-1]
			#del reverse[cpos][node]
			find = 0


for i in range(len(inputstr)):
	print 'i',i
	if i == len(inputstr)-1:
		findletter(autom,graphing,regraph,inputstr,i,1)
	else:
		findletter(autom,graphing,regraph,inputstr,i,0)


print graphing
print regraph
print len(inputstr)

def reverse(graph,rgraph,inputstr):
	last = len(inputstr)
	inital = rgraph[last][last-1]



'''	
for i in range(len(inputstr)):
	reach(autom,graphing,i,0,len(inputstr),0,0,savedata)
	print 'savedata',savedata
	print 'graphing', graphing
states = set([])
sta = []
print graphing
for key, liste in graphing[0].iteritems():
	states = states | set(liste)
print 'states-1',states
graphing[-1][0] = []
for state in states:
	graphing[-1][0].append(state)
print 'graphing',graphing

agraph = sc2.automata(0,0,0)

agraph.reset()

agraph.start = 'q0'
agraph.end = (len(inputstr),'q'+str(autom.end))
agraph.states = agraph.states | {agraph.start} | {agraph.end}
for i in range(-1,len(inputstr)):
	if i == -1:
		temp = graphing[-1][0]
		agraph.transition['q0'] = []
		for node in temp:
			endnode = (0,'q'+str(node))
			value = varstates[node]
			tup = (str(endnode),str(value))
			agraph.transition['q0'].append(tup)
			agraph.states = agraph.states | {str(endnode)}
	else:
		temp = graphing[i]
		for node, edges in temp.iteritems():
			startn = (i,'q'+str(node))
			if not agraph.transition.has_key(str(startn)):
				agraph.transition[str(startn)] = []
			for dest in edges:
				endnode = (i+1,'q'+str(dest))
				value = varstates[dest]
				tup = (str(endnode),str(value))
				agraph.transition[str(startn)].append(tup)
				agraph.states = agraph.states | {str(endnode)}

printgraph(agraph,2)
'''