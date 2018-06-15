import script2
import threading, time, random, traceback, uuid, json, Queue, sys, copy

s2_out = script2.main()
print 's2_out' 
s2_out.printauto()


import functools
import graphviz as gv

digraph = functools.partial(gv.Digraph, filename='automata', format='pdf')


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

g = digraph()
g.attr(rankdir='LR', size='8,5')
g.attr('node', shape='doublecircle')
add_nodes(g, ['qf'] )
g.attr('node', shape='circle')
edgess = []
for item in readdata:
	item = item.split(',')
	tup = ((item[0],item[1]),{'label':item[2]})
	edgess.append(tup)

add_edges(g, edgess)
g.view()

