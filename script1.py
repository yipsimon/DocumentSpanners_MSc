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

	digraph = functools.partial(gv.Digraph, filename=name)
	g = digraph()
	g.attr(rankdir='LR', size='8,5')
	g.attr('node', shape='doublecircle')
	print 'end',auto.end
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
	g.format = 'pdf'
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
print 'Option 3 : Join'
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
	elif x == 3:
		autom = sc2.main()
		autom2 = sc2.main()
		print 'automaton2',autom2.printauto()
		print 'automaton',autom.printauto()
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

def chkexist(graph,pos,node):
	if not graph[pos].has_key(node):
		graph[pos][node] = set([])

def repeat(auto,graph,i,j,node):
	listedges = auto.transition[node]
	ext = ['+','-']
	for edge in listedges:
		if (edge[1][-1] in ext) or (edge[1] == '[epsi]'):
			chkexist(graph,i+1,edge[0])
			graph[i+1][edge[0]].add(j)
			repeat(auto,graph,i,j,edge[0])

graphing = {}
regraph = {}

for i in range(len(inputstr)):
	regraph[i] = {}
	graphing[i] = {}

regraph[len(inputstr)] = {}
graphing[-1] = {}

#all possible paths
ext = ['+','-']
node = set([])
for i in range(len(inputstr)):
	find = 0
	if i == 0:
		for key in autom.states:
			edges = autom.transition[key]
			print 'key',key
			print 'edges',edges
			for edge in edges:
				print 'edge',edge
				if edge[1] == '[epsi]':
					print 'true2'
					listedges = autom.transition[edge[0]]
					for edg in listedges:
						if edg[1] == inputstr[i]:
							chkexist(regraph,i+1,edg[0])
							regraph[i+1][edg[0]].add(key)
							find = 1
				elif edge[1] == inputstr[i]:
					print 'true'
					chkexist(regraph,i+1,edge[0])
					regraph[i+1][edge[0]].add(key)
					find = 1

		if find == 1:
			for key in regraph[i+1].keys():
				val = regraph[i+1][key]
				for item in val:
					repeat(autom,regraph,i,item,key)
			
		print 'regraph',regraph
	
	else:
		for key in regraph[i].keys():
			print 'key',key
			edges = autom.transition[key]
			print 'edges',edges
			for edge in edges:
				print 'edge',edge
				if edge[1] == '[epsi]':
					print 'true2'
					listedges = autom.transition[edge[0]]
					for edg in listedges:
						if edg[1] == inputstr[i]:
							chkexist(regraph,i+1,edg[0])
							regraph[i+1][edg[0]].add(key)
							find = 1

				elif edge[1] == inputstr[i]:
					print 'true'
					chkexist(regraph,i+1,edge[0])
					regraph[i+1][edge[0]].add(key)
					find = 1
		
		if find == 1:
			for key in regraph[i+1].keys():
				val = regraph[i+1][key]
				for item in val:
					repeat(autom,regraph,i,item,key)

		print 'regraph',regraph


print 'regraph',regraph

states = regraph[len(inputstr)][int(autom.end)]
for item in states:
	chkexist(graphing,len(inputstr)-1,item)
	graphing[len(inputstr)-1][item].add(int(autom.end))
print 'states',states
print 'graphing',graphing


for i in range(len(inputstr)-1,0,-1):
	print i,'i'
	temp = set([])
	for node in states:
		edges = regraph[i][node]
		print 'edges',edges
		for edge in edges:
			print 'edge',edge
			chkexist(graphing,i-1,edge)
			print 'graphing',graphing
			graphing[i-1][edge].add(node)
			temp.add(edge)
	states = temp

#print 'graphing',graphing
#print 'states',states
graphing[-1][0] = states
print 'graphing',graphing

finalgraph = {}

def ghaskey(graph,node):
	if not graph.has_key(node):
		graph[node] = []

for key, item in graphing.iteritems():
	for key2, item2 in item.iteritems():
		for item3 in item2:
			if key == -1:
				node1 = 'q0'
			else:
				node1 = (key,key2)
			node2 = (key+1,item3)
			value = varstates[item3]
			ghaskey(finalgraph,node1)
			finalgraph[node1].append([node2,value])

print finalgraph
enode = '('+str(len(inputstr))+', '+str(autom.end)+')'
autograph = sc2.automata(0,0,0)
autograph.reset()
autograph.start = 'q0'
autograph.end = str(enode)
autograph.transition = finalgraph
#printgraph(autograph,1)


s = {}
avali = {}
edging = {}

for i in range(-1,len(inputstr)):
	s[i] = set([])
	edging[i] = {}
	avali[i] = []

s[-1].add(0)
def haskey(graph,node):
	if not graph.has_key(node):
		graph[node] = set([])


def minString(num):
	tempedge = {}
	letter = []
	last = []
	leng = len(varstates[0])
	for i in range(num,len(inputstr)-1):
		print 'i',i
		print 's[i]',s[i]
		for item1 in s[i]:
			print 'item1',item1
			print 'graphing[i]',graphing[i]
			if graphing[i].has_key(int(item1)):
				for item in graphing[i][int(item1)]:
					temp = varstates[int(item)]
					if not temp in avali[i]:
						avali[i].append(temp)
					haskey(tempedge,str(temp))
					tempedge[str(temp)].add(item)
					edging[i] = tempedge

		for j in range(leng-1,0,-1):
			avali[i].sort(key=lambda tup: tup[j])
		print 'avali',avali
		print 'tempedge',tempedge

		letter.append(avali[i][0])

		print 'letter',letter

		s[i+1] = s[i+1] | tempedge[str(avali[i][0])]
		print 's',s
		print '\n'

	for j in range(leng):
		last.append(['c'])
	letter.extend(last)
	return letter

k = minString(-1)
print k
print 'edging',edging

def nextString(word):
	print 'start nextString'
	output = word
	output.pop()
	for i in range(len(inputstr)-2,-2,-1):
		print 'i',i
		let = word[i+1]
		print 'let',let
		output.pop()
		print 'output', output
		if len(avali[i]) != 1:
			print 'avali',avali[i]
			avali[i].remove(let)
			print 'avali removed',avali[i]
			output.append(avali[i][0])
			print 'output1',output
			s[i+1] = edging[i][str(avali[i][0])]
			print 's',s
			nk = minString(i+1)
			output.extend(nk)
			print 'outputfinal',output
			return output
		else:
			s[i+1] = set([])
			avali[i] = []
			edging[i]
			print 's',s
			print 'avali[i]',avali

	return output
listofout = []
while k != []:
	print 'k',k
	listofout.append(str(k))
	k = nextString(k)
print '\n results'
for i in range(len(listofout)):
	print listofout[i]