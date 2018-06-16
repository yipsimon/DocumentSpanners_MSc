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

def printgraph(auto):
	digraph = functools.partial(gv.Digraph, filename='automata', format='pdf')
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
    		if not auto.transition.has_key(item[0]):
    			auto.transition[item[0]] = []
    		tup = (item[1],item[2])
    		auto.transition[str(item[0])].append(tup)
    		auto.states = auto.states | {item[0],item[1]}

    		if item[0][-1] == 0:
    			auto.start = item[0]
    		if isinstance(item[1][-1], str):
    			auto.end = item[1]
    		elif auto.end[-1] < item[1][-1]:
    			auto.end = item[1]

    f.close()
    return auto

def functionalitychk(auto):
	openlist = {}
	closelist = {}
	for item in auto.states:
		item = str(item)
		if item[-1] == '0':
			seenlist = {str(item)}
			todolist = {str(item)}

		openlist[item] = set([])
		closelist[item] = set([])
	print 'openlist',openlist
	print 'closelist',closelist
	print 'seenlist',seenlist
	print 'todolist',todolist

	while todolist:
		origin = todolist.pop()
		print 'origin',origin
		print 'auto.transition[origin]',auto.transition[origin]
		for item in auto.transition[origin]:
			dest = str(item[0])
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

	return openlist, closelist


print 'Welcome to prototype 1, select your functions:'
print 'Option 1 : enter regex formula'
print 'Option 2 : Read from existing file'
x = input("Select: ")
while 1:
	if x == 1:
		automaton = sc2.main()
		print 'automaton',automaton.printauto()
		break
	elif x == 2:
		automaton = readauto()
		print 'automaton'
		automaton.printauto()
		break
	else:
		print 'error try again'

inputprint = input('Print Graph: yes=0, no=any \n')
if not inputprint:
	printgraph(automaton)
inputstr = raw_input('Enter your string: ')

oplist, clolist = functionalitychk(automaton)

print 'openlist',oplist
print 'closelist',clolist




