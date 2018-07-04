import script2 as sc2
import functools
import graphviz as gv
import threading, time, sys, copy

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
	else:
		name = str(mode)

	digraph = functools.partial(gv.Digraph, filename=name)
	g = digraph()
	g.attr(rankdir='LR', size='8,5')
	g.attr('node', shape='doublecircle')
	print ('end',auto.end)
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
    		if not int(item[0]) in auto.transition:
    			auto.transition[int(item[0])] = []
    		if not int(item[1]) in auto.transition:
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
    auto.tostr()

    return auto

def functionalitychk(auto, var):
	openlist = {}
	closelist = {}
	varconfig = {}
	temp = []
	for config in auto.varstates:
		temp.append(str(config))

	for item in auto.states:
		openlist[str(item)] = set([])
		closelist[str(item)] = set([])
		varconfig[str(item)] = []

		for config in auto.varstates:
			varconfig[str(item)].append('w')

	seenlist = {str(auto.start)}
	todolist = {str(auto.start)}
		

	print ('openlist',openlist)
	print ('closelist',closelist)
	print ('varconfig',varconfig)
	print ('seenlist',seenlist)
	print ('todolist',todolist)
	print ('temp', temp)
	print ('var', var)
	print ('varstates',auto.varstates)

	while todolist:
		origin = todolist.pop()
		print ('origin',origin)
		for item in auto.transition[origin]:
			dest = str(item[0])
			letter = item[1][0]
			op = openlist[dest]
			oq = openlist[str(origin)]
			cp = closelist[dest]
			cq = closelist[str(origin)]
			print ('item',item)
			if item[1][-1] == '+':
				if var == '-1' or letter == str(var):
					print ('normal')
					if oq & {letter}:
						print ('not function already in open')
						sys.exit(1)
					if seenlist & {dest}:
						if op != (oq | {letter}) or cp != cq:
							print ('not function different states for one node')
							sys.exit(1)
					else:
						seenlist.add(dest)
						todolist.add(dest)
						
						openlist[dest] = (openlist[origin] | {letter})
						closelist[dest] = closelist[origin]
						for k in range(len(temp)):
							print ('temp[k]',temp[k])
							if temp[k] == letter:
								varconfig[dest] = []
								varconfig[dest].extend(varconfig[origin])
								varconfig[dest][k] = 'o'
								print ('varconfig',varconfig[dest])
				
				elif letter != str(var):
					print ('abnormal')
					auto.transition[origin].remove(item)
					tuptemp = (dest,'[epsi]')
					auto.transition[origin].append(tuptemp)
					seenlist.add(dest)
					todolist.add(dest)
					openlist[dest] = openlist[origin] 
					closelist[dest] = closelist[origin]	
					varconfig[dest] = varconfig[origin]


			elif item[1][-1] == '-':
				if var == '-1' or letter == str(var):
					print ('normal')
					if {letter} - oq or cq & {letter}:
						print ('not function already in close, not opened')
						sys.exit(1)
					if seenlist & {dest}:
						if op != oq  or cp != (cq | {letter}):
							print ('not function different states for one node')
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
				
				elif letter != str(var):
					print ('abnormal')
					auto.transition[origin].remove(item)
					tuptemp = (dest,'[epsi]')
					auto.transition[origin].append(tuptemp)
					seenlist.add(dest)
					todolist.add(dest)
					openlist[dest] = openlist[origin] 
					closelist[dest] = closelist[origin]	
					varconfig[dest] = varconfig[origin]

			else:
				if seenlist & {dest}:
					if op != oq  or cp != cq:
						print ('not function different states for one node')
						sys.exit(1)
				else:
					seenlist.add(dest)
					todolist.add(dest)
					openlist[dest] = openlist[origin] 
					closelist[dest] = closelist[origin]	
					varconfig[dest] = varconfig[origin]

	print ('openlistf',openlist)
	print ('closelistf',closelist)

	return varconfig

def chkexist(graph,pos,node):
	if not node in graph[pos]:
		graph[pos][node] = set([])

def repeat(auto,graph,i,j,node):
	listedges = auto.transition[node]
	ext = ['+','-']
	for edge in listedges:
		if (edge[1][-1] in ext) or (edge[1] == '[epsi]'):
			chkexist(graph,i+1,edge[0])
			graph[i+1][edge[0]].add(j)
			repeat(auto,graph,i,j,edge[0])

def ifepsi(autom,inputstr,regraph,i,find,edge,key):
	print ('true2')
	listedges = autom.transition[edge[0]]
	for edg in listedges:
		if edg[1] == inputstr[i]:
			chkexist(regraph,i+1,edg[0])
			regraph[i+1][edg[0]].add(key)
			find = 1
		elif edg[1] == '[epsi]':
			ifepsi(autom,inputstr,regraph,i,find,edg,key)


def gengraphs(autom,inputstr):

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
	for i in range(-1,len(inputstr)):
		find = 0
		if i == -1:
			chkexist(regraph,i+1,str(autom.start))
			regraph[i+1][str(autom.start)].add('0')
			
			todos = set([str(autom.start)])
			while todos:
				item = todos.pop()
				edges = autom.transition[item]
				for edge in edges:
					if edge[1][-1] in ext or edge[1] == '[epsi]':
						print ('edgeffff',edge)
						chkexist(regraph,i+1,edge[0])
						regraph[i+1][edge[0]].add('0')
						todos.add(edge[0])
				
			print ('regraph00000',regraph)

		else:
			for key in regraph[i].keys():
				edges = autom.transition[key]
				for edge in edges:
					if edge[1] == '[epsi]':
						ifepsi(autom,inputstr,regraph,i,find,edge,key)

					elif edge[1] == inputstr[i]:
						chkexist(regraph,i+1,edge[0])
						regraph[i+1][edge[0]].add(key)
						find = 1
			
			if find == 1:
				for key in regraph[i+1].keys():
					val = regraph[i+1][key]
					for item in val:
						repeat(autom,regraph,i,item,key)

	print ('regraph',regraph)

	print (str(autom.end))
	states = regraph[len(inputstr)][str(autom.end)]
	for item in states:
		chkexist(graphing,len(inputstr)-1,str(item))
		graphing[len(inputstr)-1][str(item)].add(str(autom.end))
	print ('states',states)
	print ('graphing',graphing)


	for i in range(len(inputstr)-1,-1,-1):
		print (i,'i')
		temp = set([])
		for node in states:
			edges = regraph[i][node]
			print ('edges',edges)
			for edge in edges:
				print ('edge',edge)
				chkexist(graphing,i-1,str(edge))
				print ('graphing',graphing)
				graphing[i-1][str(edge)].add(str(node))
				temp.add(str(edge))
		states = temp

	#print 'graphing',graphing
	#print 'states',states
	#graphing[-1][str(0)] = states
	print ('graphingffff',graphing)

	return graphing



def ghaskey(graph,node):
	if not node in graph.has_key:
		graph[node] = []

def final(autom,graphing,varstates,num):
	finalgraph = {}
	for key, item in graphing.items():
		for key2, item2 in item.items():
			for item3 in item2:
				if key == -1:
					node1 = 'q0'
				else:
					node1 = (str(key),str(key2))
				node2 = (str(key+1),str(item3))
				value = varstates[str(item3)]
				ghaskey(finalgraph,node1)
				finalgraph[node1].append([node2,value])

	print (finalgraph)
	enode = "('"+str(len(inputstr))+"', '"+str(autom.end)+"')"
	autograph = sc2.automata(0,0,0)
	autograph.reset()
	autograph.start = 'q0'
	autograph.end = str(enode)
	autograph.transition = finalgraph
	printgraph(autograph,num)

	return autograph

def haskey(graph,node):
	if not node in graph:
		graph[node] = set([])

def minString(num,s,avali,edging,graphing,varstates,inputstr,auto,num2):
	tempedge = {}
	letter = []
	last = []
	if num2 == -1:
		leng = len(varstates[str(auto.start)])
	else:
		leng = 1
	for i in range(num,len(inputstr)-1):
		print ('i',i)
		print ('s[i]',s[i])
		for item1 in s[i]:
			print ('item1',item1)
			print ('graphing[i]',graphing[i])
			if str(item1) in graphing[i]:
				for item in graphing[i][str(item1)]:
					if num2 == -1:
						temp = varstates[str(item)]
					else:
						temp = [str(varstates[str(item)][num2])]

					if not temp in avali[i]:
						avali[i].append(temp)
					haskey(tempedge,str(temp))
					tempedge[str(temp)].add(item)
					edging[i] = tempedge

		for j in range(leng-1,0,-1):
			avali[i].sort(key=lambda tup: tup[j])
		print ('avali',avali)
		print ('tempedge',tempedge)

		letter.append(avali[i][0])

		print ('letter',letter)

		s[i+1] = s[i+1] | tempedge[str(avali[i][0])]
		print ('s',s)
		print ('\n')
	temp2 = []
	for j in range(leng):
		temp2.append('c')

	letter.append(temp2)
	return letter

def nextString(word,s,avali,edging,graphing,varstates,inputstr,auto,num2):
	print ('start nextString')
	output = word
	output.pop()
	print ('word',word)
	for i in range(len(inputstr)-2,-2,-1):
		print ('i',i)
		let = word[i+1]
		print ('let',let)
		output.pop()
		print ('output', output)
		if len(avali[i]) != 1:
			print ('avali',avali[i])
			avali[i].remove(let)
			print ('avali removed',avali[i])
			output.append(avali[i][0])
			print ('output1',output)
			s[i+1] = edging[i][str(avali[i][0])]
			print ('s',s)
			nk = minString(i+1,s,avali,edging,graphing,varstates,inputstr,auto,num2)
			output.extend(nk)
			print ('outputfinal',output)
			return output
		else:
			s[i+1] = set([])
			avali[i] = []
			edging[i]
			print ('s',s)
			print ('avali[i]',avali)

	return output


def outputing(graphing, varstate, inputstr, auto, num2):
	s = {}
	avali = {}
	edging = {}

	for i in range(-1,len(inputstr)):
		s[i] = set([])
		edging[i] = {}
		avali[i] = []

	s[-1].add(0)
	k = minString(-1,s,avali,edging,graphing,varstates,inputstr,auto,num2)
	print (k)
	print ('edging',edging)

	listofout = []
	while k != []:
		print ('k',k)
		listofout.append(str(k))
		k = nextString(k,s,avali,edging,graphing,varstates,inputstr,auto,num2)
	print ('\n results')
	for i in range(len(listofout)):
		print (listofout[i])




print ('Welcome to prototype 1, select your functions:')
print ('Option 1 : enter regex formula')
print ('Option 2 : Read from existing file')
print ('Option 3 : Join version 1')
print ('Option 4 : Join version 2')
print ('Option 5 : Projection version 1')
print ('Option 6 : Projection version 2')
x = input("Select: ")
if int(x) == 1:
	autom = sc2.main()
	print ('automaton',autom.printauto())

elif int(x) == 2:
	autom = readauto()
	print ('automaton')
	autom.printauto()
	
elif int(x) == 3 or int(x) == 4:
	#autom = sc2.main()
	#autom2 = sc2.main()
	#print 'automaton2',autom2.printauto()
	#print 'automaton',autom.printauto()
	print ('something')
elif int(x) == 5 or int(x) == 6:
	print ('not done')

else:
	print ('error try again')

if int(x) <= 2:
	inputprint = input('Print Graph: yes=0, no=any \n')
	if not inputprint:
		printgraph(autom,1)
	
	inputstr = input('Enter your string: ')

	varstates = functionalitychk(autom,'-1')

	print ('varstates',varstates)

	graph = gengraphs(autom,inputstr)

	finalauto = final(autom,graph,varstates,2)

	outputing(graph, varstates, inputstr, autom, -1)

elif int(x) > 2 and int(x) <= 4:
	autom1 = sc2.automata(0,0,0)
	autom2 = sc2.automata(0,0,0)
	autom1.reset()
	autom2.reset()
	autom1.states = autom1.states | {'0','1','2'}
	autom2.states = autom2.states | {'0','1','2','3'}
	autom1.varstates = autom1.varstates | {'x'}
	autom2.varstates = autom2.varstates | {'x'}
	autom1.transition['0'] = [('0','a'),('1','x+')]
	autom1.transition['1'] = [('1','a'),('2','x-')]
	autom1.transition['2'] = [('2','a')]
	autom2.transition['0'] = [('0','a'),('1','a')]
	autom2.transition['1'] = [('1','a'),('2','x+')]
	autom2.transition['2'] = [('2','a'),('3','x-')]
	autom2.transition['3'] = [('3','a')]
	autom1.start = 0
	autom1.end = 2
	autom2.start = 0
	autom2.end = 3
	#ext = ['+','-']
	if int(x) == 3:
		auto = sc2.automata(0,0,0)
		auto.reset()
		stup = (0,0)
		auto.start = str(stup)
		stup = (autom1.end,autom2.end)
		auto.end = str(stup)
		auto.varstates = autom1.varstates | autom2.varstates
		inittup = (0,0)
		nextnode = set([inittup])
		seened = set([inittup])
		while nextnode:
			node = nextnode.pop()
			seened.add(node)
			edges1 = autom1.transition[str(node[0])]
			edges2 = autom2.transition[str(node[1])]
			ghaskey(auto.transition, str(node))
			varop = set()
			for i in range(-1, len(edges1)):
				for j in range(len(edges2)):
					if i == -1:
						dest = (node[0],int(edges2[j][0]))
					else:
						dest = (int(edges1[i][0]),int(edges2[j][0]))

					
					newtup = (dest,edges2[j][1])
					if dest == node:
						if newtup not in auto.transition[str(node)]:
							auto.transition[str(node)].append(newtup)
					else:
						auto.transition[str(node)].append(newtup)
					
					if not seened & {dest}:
						nextnode.add(dest)


			for i in range(-1, len(edges2)):
				for j in range(len(edges1)):
					if i == -1:
						dest = (int(edges1[j][0]),node[0])
					else:
						dest = (int(edges1[j][0]),int(edges2[i][0]))

					newtup = (dest,edges1[j][1])
					if dest == node:
						if newtup not in auto.transition[str(node)]:
							auto.transition[str(node)].append(newtup)
					else:
						auto.transition[str(node)].append(newtup)
					
					if not seened & {dest}:
						nextnode.add(dest)						


			seened.add(node)
			print ('nextnode',nextnode)
			print ('auto.transition',auto.transition)






		'''
		templetters = {}
		for item in autom2.states:
			templetters[str(item)] = set([])
			for item2 in autom2.transition[str(item)]:
				templetters[str(item)].add(str(item2[1]))
		inittup = (0,0)
		nextnode = set([inittup])
		seened = set([inittup])
		while nextnode:
			tup = nextnode.pop()
			seened.add(tup)
			print tup
			node1 = str(tup[0])
			node2 = str(tup[1])
			trans = autom1.transition[str(node1)]
			for tup in trans:
				val = tup[1]
				if templetters[str(node2)] & {val}:
					name = (int(node1),int(node2))
					auto.states.add(str(name))
					ghaskey(auto.transition,str(name))
					for tup2 in autom2.transition[str(node2)]:
						if tup2[1] == val:
							dest = (int(tup[0]),int(tup2[0]))
							tup3 = (str(dest),str(val))
							auto.transition[str(name)].append(tup3)
							if not seened & {dest}:
								nextnode.add(dest)
						
						elif tup2[1][-1] in ext and tup[1][-1] in ext:
							dest = (int(tup[0]),int(tup2[0]))
							tup3 = (str(dest),str(val))
							auto.transition[str(name)].append(tup3)
							if not seened & {dest}:
								nextnode.add(dest)
						
		if len(auto.states) == 0:
			print 'join failed'
			sys.exit(0)
		'''
		'''
		#safe way
		for node1 in autom1.transition.keys():
			trans = autom1.transition[str(node1)]
			for tup in trans:
				val = tup[1]
				for node2 in autom2.transition.keys():
					if templetters[str(node2)] & {val}:
						name = (int(node1),int(node2))
						auto.states.add(str(name))
						ghaskey(auto.transition,str(name))
						for tup2 in autom2.transition[str(node2)]:
							if tup2[1] == val:
								dest = (int(tup[0]),int(tup2[0]))
								tup3 = (str(dest),str(val))
								auto.transition[str(name)].append(tup3)
		'''
		auto.printauto()
		printgraph(auto,1)

		inputstr = input('Enter your string: ')

		varstates = functionalitychk(auto,'-1')

		print ('varstates',varstates)

		graph = gengraphs(auto,inputstr)

		finalauto = final(auto,graph,varstates,2)

		outputing(graph, varstates, inputstr, auto, -1)

	elif int(x) == 4:
		inputprint = input('Print Graph: yes=0, no=any \n')
		if not inputprint:
			printgraph(autom,1)
	
		inputstr = input('Enter your string: ')

		varstates1 = functionalitychk(autom1,'-1')
		varstates2 = functionalitychk(autom2,'-1')

		print ('varstates1',varstates1)
		print ('varstates2',varstates2)

		graph1 = gengraphs(autom1,inputstr)
		graph2 = gengraphs(autom2,inputstr)

		finalauto1 = final(autom1,graph1,varstates1,3)
		finalauto2 = final(autom2,graph2,varstates2,4)
		'''
		auto = sc2.automata(0,0,0)
		auto.reset()
		auto.start = str(finalauto1.start)
		stup = (str(len(inputstr)),str((autom1.end,autom2.end)))
		auto.end = str(stup)
		auto.varstates = autom1.varstates | autom2.varstates
		todoss = set(['0'])
		todosss = set(['0'])

		for i in range(-1,len(inputstr)):
			while todoss and todosss:
				nod1 = todoss.pop()
				nod2 = todosss.pop()
				for item1 in graph1[i][nod1]:
					for item2 in graph2[i][nod2]:
						if item1[1] == item2[1]:
							dest = ()

		'''
			
		#outputing(graph, varstates, inputstr, autom)

elif int(x) == 5:
	autom = sc2.main()
	print ('automaton',autom.printauto())
	inputprint = input('Print Graph: yes=0, no=any \n')
	if not inputprint:
		printgraph(autom,1)
	
	inputstr = input('Enter your string: ')

	varstates = functionalitychk(autom,'-1')

	print ('varstates all',varstates)

	graph = gengraphs(autom,inputstr)

	finalauto = final(autom,graph,varstates,2)

	print ('varstates',autom.varstates)
	time.sleep(1)

	num1 = input('choose position, -1 = all\n')
	outputing(graph, varstates, inputstr, autom, num1)

elif int(x) == 6:
	autom = sc2.main()
	print ('automaton',autom.printauto())
	inputstr = input('Enter your string: ')
	print ('varstates',autom.varstates)
	var3 = input('choose var operation: , all == -1 \n')
	autom.varstates = set([var3])
	varstates = functionalitychk(autom,var3)

	print ('varstates all',varstates)
	autom.printauto()

	graph = gengraphs(autom,inputstr)

	finalauto = final(autom,graph,varstates,2)

	print ('varstates',autom.varstates)
	time.sleep(2)
	outputing(graph, varstates, inputstr, autom, -1)