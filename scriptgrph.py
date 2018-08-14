import graphviz as gv
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

def printgraph3(auto,name):
	digraph = functools.partial(gv.Digraph, filename=name)
	g = digraph()
	g.attr(rankdir='LR', size='8,5')
	g.attr('node', shape='doublecircle')
	print ('end',str(auto.end))
	add_nodes(g, [str(auto.end)])
	g.attr('node', shape='circle')
	edges = []
	for key, item in auto.transition.items():
		if isinstance(item,list):
			for line in item:
				if line[1] == '[epsi]':
					value = '&epsilon;'
				else: 
					value = line[1]
				tup = ((str(key),str(line[0])),{'label':str(value)})
				edges.append(tup)
		else:
			if item[1] == '[epsi]':
				value = '&epsilon;'
			else: 
				value = item[1]
			tup = ((str(key),str(item[0])),{'label':str(value)})
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