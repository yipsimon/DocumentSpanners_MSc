import script2
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
    data = []
    for line in f:
        data.extend(line.split(';'))
        del data[-1]

    f.close()

    auto = automata('q0','qf',0)
    auto.transition = {}
    for edge in data:
    	edge = edge.split(',')
		if not auto.transition.has_key(edge[0]):
			auto.transition[edge[0]] = []
		tup = (edge[1],edge[2])
		auto.transition[edge[0]].append(tup)

    return auto

print 'Welcome to prototype 1, select your functions:'
print 'Option 1 : enter regex formula'
print 'Option 2 : Read from existing file'
x = input("Select: ")
while 1:
	if x == 1:
		automaton = script2.main()
		print 'automaton',automaton.printauto()
		break
	elif x == 2:
		automaton = readauto()
		print 'automaton',automaton.printauto()
		break
	else:
		print 'error try again'








