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
	digraph = functools.partial(gv.Digraph, filename=name, format='pdf')
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
		for item in auto.transition[origin]:
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
savedata = {}
for i in range(-1,len(inputstr)):
	graphing[i] = {}

def reach(auto,graph,i,start,end,repeat,lookup,prevsave):
	ext = ['+','-']
	done = 0
	states = set([])
	save = prevsave
	if repeat == 1:
		done = 1
		listedges = auto.transition[lookup]
		for item in listedges:
			if i == end-1:
				if (item[1][-1] == '+') or (item[1] == '[epsi]'):
					print 'find sym0'
					reach(auto,graph,i,start,end,1,item[0],save)
				elif item[1][-1] == '-':
					print 'find sym1'
					graph[i][start].append(item[0])
					print 'graph[i][start].append(item[0])', graph[i][start]
			else:
				if (item[1][-1] in ext) or (item[1] == '[epsi]'):
					print 'find sym'
					graph[i][start].append(item[0])
					reach(auto,graph,i,start,end,1,item[0],save)
	elif i > 0 and repeat == 0:
		print 'i', i
		if save.has_key(inputstr[i]) and i != end-1:
			graph[i] = save[inputstr[i]]
			done = 1
			print 'done1'
		else:
			for key, liste in graph[int(i-1)].iteritems():
				states = states | set(liste)
			print 'states1',states
	elif i == 0:
		states = auto.states
		print 'states0',states
	
	if done == 0:
		print 'done',done
		for node in states:
			listedges = auto.transition[node]
			print 'listedges', listedges
			for edge in listedges:
				print 'edge',edge
				if edge[1] == inputstr[i]:
					if not graph[i].has_key(node):
						graph[i][node] = []

					if i != end-1:
						graph[i][node].append(edge[0])
					else:
						if int(node) == int(auto.end):
							graph[i][node].append(edge[0])
					reach(auto,graph,i,node,end,1,edge[0],save)
		prevsave[inputstr[i]] = graph[i]
		print 'graph[i]', graph[i]
		print 'prevsave',prevsave


	
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

stackS = {}
seenstack = {}
for i in range(len(inputstr)+1):
	stackS[i] = []
	seenstack[i] = set()
print 'stackS',stackS
print 'seenstack', seenstack
print len(inputstr)
stackS[0].append(0)

def minString(start):
	output = ''
	for i in range(start,len(inputstr)):
		for j in range(len(stackS[i])):
			currentnode = stackS[i][j]
			minletter = graphing[i-1][currentnode][0][1]
			for k in range(len(graphing[i-1][currentnode])):
				newval = graphing[i-1][currentnode][k][1]
				if newval != minletter:
					for m in range(len(minletter)):
						if newval[m] != minletter[m]:

					


					if tup[1] != minletter:
						if tup[1] == 'w':
							minletter = 'w'
						elif tup[1] == 'o' and minletter != 'w':
							minletter = 'o'

		#print minletter
		seenstack[i] = seenstack[i] | set(minletter)
		output = output+minletter
		for j in range(len(stackS[i])):
			currentnode = stackS[i][j]
			for k in range(len(agraph[i-1][currentnode])):
				tup = agraph[i-1][currentnode][k]
				if tup[1] == minletter:
					stackS[i+1].append(tup[2])
	output = output+'c'
	return output

def nextString(kstring):
	for i in range(len(inputstr)-1,-1,-1):
		cletter = kstring[i]
		#print i
		#print cletter
		#time.sleep(5)
		xletter = 0
		if cletter == 'w' or cletter == 'o':
			xletter = 1
		if xletter:
			nextletter = 0
			findletter = ''

			for j in range(len(stackS[i])):
				currentnode = stackS[i][j]
				for k in range(len(agraph[i-1][currentnode])):
					tup = agraph[i-1][currentnode][k]

					if tup[1] != cletter:
						if seenstack[i] != (seenstack[i] | set(tup[1])):
							if not findletter:
								findletter = tup[1]
							elif tup[1] == 'o':
								findletter = tup[1]
							nextletter = 1
			
			if nextletter == 1:
				seenstack[i] = seenstack[i] | set(findletter)
				for j in range(len(stackS[i])):
					currentnode = stackS[i][j]
					for k in range(len(agraph[i-1][currentnode])):
						tup = agraph[i-1][currentnode][k]
						if tup[1] == findletter:
							stackS[i+1].append(tup[2])
				#print 'kstring[i:]',kstring[:i]
				newk = kstring[:i]+findletter+minString(i+1)
				#print newk
				return newk
		else:
			stackS[i] = []
			seenstack[i] = set()

	return ''


stackS[0].append('q0')
kstr = minString(0)
print seenstack
while kstr:
	print kstr
	kstr = nextString(kstr)
'''