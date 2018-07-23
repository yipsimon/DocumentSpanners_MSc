import script2 as sc2
import functools
import graphviz as gv
import threading, time, sys, copy

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

#Reading in a file and output as automaton object
def readauto(fname):
    #filename = raw_input('Please enter a file name: ')
    #fname = 'test'+'.txt'
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
    			if str(item[2][0]) not in auto.varstates:
    				auto.varstates.append(str(item[2][0]))
    		if int(item[0]) == 0:
    			auto.start = item[0]
    		if int(item[1]) > int(auto.end):
    			auto.end = item[1]
    f.close()
    auto.tostr()

    return auto

#Checking whether the inputted automaton is functional.
#Output is a dictionary call varconfig, might consider removing openlist and closelist and replacing them with varconfig data
#Or it might be better to create varconfig in a different function to make it easier to read
#Converting edges to epsi is done here as well, var value determine this, however this method currently works for only one varstate, need to consider another method for handling multiple states
def functionalitychk(auto, var):
	openlist = {}
	closelist = {}
	varconfig = {}
	temp = auto.varstates

	#Creating Empty Spaces for dictionaries
	for item in auto.states:
		openlist[str(item)] = set([])
		closelist[str(item)] = set([])
		varconfig[str(item)] = []
		#For case of multiple varaibles states, default value is w
		for config in auto.varstates:
			varconfig[str(item)].append('w')

	seenlist = {str(auto.start)}
	todolist = {str(auto.start)}
	#While loop for finding all varconfig for all nodes, replacement for edges containing 'x','-' is replaced by epsilon as well
	while todolist:
		origin = todolist.pop()
		for item in auto.transition[origin]:
			dest = str(item[0])
			letter = item[1][0]
			op = openlist[dest]
			oq = openlist[str(origin)]
			cp = closelist[dest]
			cq = closelist[str(origin)]
			if item[1][-1] == '+':
				if var == '-1' or letter == str(var):
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
						#Update varconfig, however the position of the var state is unknown therefore a annoying for loop is used.
						for k in range(len(temp)):
							if temp[k] == letter:
								varconfig[dest] = []
								varconfig[dest].extend(varconfig[origin])
								varconfig[dest][k] = 'o'
				
				elif letter != str(var):
					auto.transition[origin].remove(item)
					tuptemp = (dest,'[epsi]')
					auto.transition[origin].append(tuptemp)
					seenlist.add(dest)
					todolist.add(dest)
					openlist[dest] = openlist[origin] 
					closelist[dest] = closelist[origin]	
					varconfig[dest] = varconfig[origin]
			#Need to shrink this block of text
			elif item[1][-1] == '-':
				if var == '-1' or letter == str(var):
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

	return varconfig

def chkexist(graph,pos,node):
	if not node in graph[pos]:
		graph[pos][node] = set([])

def repeat(auto,graph,i,j,key,varstates):
	listedges = auto.transition[key]
	ext = ['+','-']
	for edge in listedges:
		if (edge[1][-1] in ext) or (edge[1] == '[epsi]'):
			#if (varstates[edge[0]] != varstates[str(j)]):
			chkexist(graph,i+1,edge[0])
			graph[i+1][edge[0]].add(j)
			repeat(auto,graph,i,j,edge[0],varstates)
			#if (varstates[edge[0]] == varstates[str(j)]):
				#repeat(auto,graph,i,j,edge[0],varstates)

def ifepsi(autom,inputstr,regraph,i,find,edge,key,varstates):
	listedges = autom.transition[edge[0]]
	for edg in listedges:
		if edg[1] == inputstr[i]:
			chkexist(regraph,i+1,edg[0])
			regraph[i+1][edg[0]].add(key)
			find = 1
		elif edg[1] == '[epsi]':
			if (varstates[edg[0]] == varstates[str(key)]):
				ifepsi(autom,inputstr,regraph,i,find,edg,key,varstates)

				

def gengraphs(autom,inputstr,varstates):
	graphing = {}
	regraph = {}
	#reversegraph store edges in the {positionoftext :{ 'destination' : [/origins] } } format
	#reversegraph is used to prune the graph from the final node to obtain all valid edges for the finalgraph
	#Setting up empty variables
	for i in range(len(inputstr)):
		regraph[i] = {}
		graphing[i] = {}
	regraph[len(inputstr)] = {}	#length from 0 to 2 if text has leng 3 but 0 account for initial node 'q0'
	graphing[-1] = {} #-1 is used to represent the initial node 'q0', then (0,/something), (1,/something) etc

	#all possible paths
	ext = ['+','-']
	node = set([])
	for i in range(-1,len(inputstr)):
		find = 0
		if i == -1:
			chkexist(regraph,i+1,str(autom.start))
			#regraph[i+1][str(autom.start)].add('0')
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
		else:
			for key in regraph[i].keys():
				edges = autom.transition[key]
				for edge in edges:
					if edge[1] == '[epsi]':
						if (varstates[edge[0]] == varstates[str(key)]):
							ifepsi(autom,inputstr,regraph,i,find,edge,key,varstates)

					elif edge[1] == inputstr[i]:
						chkexist(regraph,i+1,edge[0])
						regraph[i+1][edge[0]].add(key)
						find = 1

			if find == 1:
				for key in regraph[i].keys():
					repeat(autom,regraph,i,key,key,varstates)

	states = regraph[len(inputstr)][str(autom.end)]
	for item in states:
		chkexist(graphing,len(inputstr)-1,str(item))
		graphing[len(inputstr)-1][str(item)].add(str(autom.end))

	for i in range(len(inputstr)-1,-1,-1):
		temp = set([])
		for node in states:
			edges = regraph[i][node]
			for edge in edges:
				chkexist(graphing,i-1,str(edge))
				graphing[i-1][str(edge)].add(str(node))
				temp.add(str(edge))
		states = temp

	return graphing



def ghaskey(graph,node):
	if not node in graph:
		graph[node] = []

def final(end,graphing,varstates,num):
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
	enode = "('"+str(len(inputstr))+"', '"+str(end)+"')"
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

def minString(num,s,avali,edging,graphing,varstates,inputstr,start,num2):
	tempedge = {}
	letter = []
	last = []
	if num2 == -1:
		leng = len(varstates[str(start)])
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

def nextString(word,s,avali,edging,graphing,varstates,inputstr,start,num2):
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
			nk = minString(i+1,s,avali,edging,graphing,varstates,inputstr,start,num2)
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


def outputing(graphing, varstates, inputstr, start, num2):
	s = {}
	avali = {}
	edging = {}

	for i in range(-1,len(inputstr)):
		s[i] = set([])
		edging[i] = {}
		avali[i] = []

	s[-1].add(0)
	k = minString(-1,s,avali,edging,graphing,varstates,inputstr,start,num2)
	print (k)
	print ('edging',edging)

	listofout = []
	while k != []:
		print ('k',k)
		listofout.append(str(k))
		k = nextString(k,s,avali,edging,graphing,varstates,inputstr,start,num2)
	print ('\n results')
	for i in range(len(listofout)):
		print (listofout[i])


def defaultfunction1(regex,typem):
	if typem == 2:
		autom = readauto(regex)
	else:
		autom = sc2.main(regex)

	print ('automaton',autom.printauto())
	inputprint = input('Print Graph: yes=0, no=any \n')
	if int(inputprint) == 0:
		printgraph(autom,1)
	
	inputstr = input('Enter your string: ')

	varstates = functionalitychk(autom,'-1')

	print ('varstates',varstates)

	graph = gengraphs(autom,inputstr,varstates)

	finalauto = final(autom.end,graph,varstates,2)

	outputing(graph, varstates, inputstr, autom.start, -1)

def projectionver1(regex):
	autom = sc2.main(regex)
	print ('automaton',autom.printauto())
	inputprint = input('Print Graph: yes=0, no=any \n')
	if int(inputprint) == 0:
		printgraph(autom,1)
	
	inputstr = input('Enter your string: ')

	varstates = functionalitychk(autom,'-1')

	print ('varstates all',varstates)

	graph = gengraphs(autom,inputstr,varstates)

	finalauto = final(autom.end,graph,varstates,2)

	print ('varstates',autom.varstates)
	time.sleep(1)

	num1 = input('choose var operation: , all == -1 \n')
	temp4 = list(autom.varstates)
	for i in range(len(temp4)):
		if str(num1) == str(temp4[i]):
			num1 = i
			break

	outputing(graph, varstates, inputstr, autom.start, num1)

def projectionver2(regex):
	autom = sc2.main(regex)
	print ('automaton',autom.printauto())
	inputstr = input('Enter your string: ')
	print ('varstates',autom.varstates)

	var3 = input('choose var operation: , all == -1 \n')
	autom.varstates = set([var3])
	
	varstates = functionalitychk(autom,var3)

	print ('varstates all',varstates)
	autom.printauto()

	graph = gengraphs(autom,inputstr,varstates)

	finalauto = final(autom.end,graph,varstates,2)

	print ('varstates',autom.varstates)
	time.sleep(2)
	outputing(graph, varstates, inputstr, autom.start, -1)

def joinver1(regex1,regex2):
	autom1 = sc2.main(regex1)
	autom2 = sc2.main(regex2)
	arstates1 = functionalitychk(autom1,'-1')
	varstates2 = functionalitychk(autom2,'-1')
	auto = sc2.automata(0,0,0)
	auto.reset()
	stup = (autom1.start,autom2.start)
	auto.start = str(stup)
	stup = (autom1.end,autom2.end)
	auto.end = str(stup)
	auto.varstates = []
	auto.varstates.extend(autom1.varstates)
	for item in autom2.varstates:
		if item not in auto.varstates:
			auto.varstates.append(item)
	inittup = (0,0)
		
	todo1 = set([(int(0),int(0))])
	seen1 = set([])
	done = set([])
	varstates = {}
	ext = ['+','-']
		
	while todo1:
		start = todo1.pop()
		edges1 = autom1.transition[str(start[0])]
		edges2 = autom2.transition[str(start[1])]
		tempdest = []
		for edge in edges2:
			dest = (int(start[0]),int(edge[0]))
			fail = 0
			if dest in tempdest:
				fail = 2
			else:
				tempdest.append(dest)
				
			if not seen1 & {dest}:
				seen1.add(dest)
				getvar1 = varstates1[str(dest[0])]
				getvar2 = varstates2[str(dest[1])]
				order1 = list(autom1.varstates)
				order2 = list(autom2.varstates)
				varstates[str(dest)] = []
				for state in auto.varstates:
					find = 0					
					for i in range(len(order1)):
						if str(state) == str(order1[i]):
							for j in range(len(order2)):
								if str(state) == str(order2[j]):
									find = 1
									if getvar1[i] != getvar2[j]:
										fail = 1
									else:
										varstates[str(dest)].append(getvar1[j])

								elif find == 1 or fail == 1:
									break
								elif j == len(order2)-1 and find == 0:
									varstates[str(dest)].append(getvar1[i])
									find = 1
									
										
						elif find == 1 or fail == 1:
							break

						elif i == len(order1)-1 and find == 0:
							for k in range(len(order2)):
								if str(state) == str(order2[k]):
									varstates[str(dest)].append(getvar2[k])
									find = 1
									break
			if fail == 0:
				if edge[1][-1] in ext:
					temptup = (str(dest),'[epsi]')
				else:
					temptup = (str(dest),edge[1])
					
				if not str(start) in auto.transition:
					auto.transition[str(start)] = []
					#auto.transition[str(start)] = []

				auto.transition[str(start)].append(temptup)
				if str(start) != str(dest) and (not done&{dest}):
					todo1.add(dest)

			elif fail == 1:
				del varstates[str(dest)]

		for edge in edges1:
			dest = (int(edge[0]),int(start[1]))
			fail = 0
			if dest in tempdest:
				fail = 2
			else:
				tempdest.append(dest)

			if not seen1 & {dest}:
				seen1.add(dest)
				getvar1 = varstates1[str(dest[0])]
				getvar2 = varstates2[str(dest[1])]
				order1 = autom1.varstates
				order2 = autom2.varstates
				varstates[str(dest)] = []
				for state in auto.varstates:
					find = 0					
					for i in range(len(order1)):
						if str(state) == str(order1[i]):
							for j in range(len(order2)):
								if str(state) == str(order2[j]):
									find = 1
									if getvar1[i] != getvar2[j]:
										fail = 1
									else:
										varstates[str(dest)].append(getvar1[j])


								elif find == 1 or fail == 1:
									break
								elif j == len(order2)-1 and find == 0:
									varstates[str(dest)].append(getvar1[i])
									find = 1

						elif find == 1 or fail == 1:
							break
						elif i == len(order1)-1 and find == 0:
							for k in range(len(order2)):
								if str(state) == str(order2[k]):
									varstates[str(dest)].append(getvar2[k])
									find = 1
									break
			if fail == 0:	
				if edge[1][-1] in ext:
					temptup = (str(dest),'[epsi]')
				else:
					temptup = (str(dest),edge[1])
				
				if not str(start) in auto.transition:
					auto.transition[str(start)] = []
					#auto.transition[str(start)] = []
					auto.transition[str(start)].append(temptup)
				if start != dest and (not done&{dest}):
					todo1.add(dest)
			elif fail == 1:
				del varstates[str(dest)]
		done.add(start)


		auto.printauto()
		printgraph(auto,1)


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
	if int(inputprint) == 0:
		printgraph(autom,1)
	
	inputstr = input('Enter your string: ')

	varstates = functionalitychk(autom,'-1')

	print ('varstates',varstates)

	graph = gengraphs(autom,inputstr,varstates)

	finalauto = final(autom.end,graph,varstates,2)

	outputing(graph, varstates, inputstr, autom.start, -1)

elif int(x) > 2 and int(x) <= 4:
	autom1 = sc2.automata(0,0,0)
	autom2 = sc2.automata(0,0,0)
	autom1.reset()
	autom2.reset()
	autom1.states = autom1.states | {'0','1','2'}
	autom2.states = autom2.states | {'0','1','2'}
	autom1.varstates = ['x']
	autom2.varstates = ['y']
	autom1.transition['0'] = [('0','a'),('1','x+')]
	autom1.transition['1'] = [('1','a'),('2','x-')]
	autom1.transition['2'] = [('2','a')]
	autom2.transition['0'] = [('0','a'),('1','y+')]
	autom2.transition['1'] = [('1','a'),('2','y-')]
	autom2.transition['2'] = [('2','a')]
	autom1.start = 0
	autom1.end = 2
	autom2.start = 0
	autom2.end = 2
	
	#ext = ['+','-']
	if int(x) == 3:
		varstates1 = functionalitychk(autom1,'-1')
		varstates2 = functionalitychk(autom2,'-1')
		auto = sc2.automata(0,0,0)
		auto.reset()
		stup = (autom1.start,autom2.start)
		auto.start = str(stup)
		stup = (autom1.end,autom2.end)
		auto.end = str(stup)
		auto.varstates = []
		auto.varstates.extend(autom1.varstates)
		for item in autom2.varstates:
			if item not in auto.varstates:
				auto.varstates.append(item)
		inittup = (0,0)
		
		print('auto.varstates',auto.varstates)
		todo1 = set([(int(0),int(0))])
		seen1 = set([])
		done = set([])
		varstates = {}
		ext = ['+','-']

		while todo1:
			print ('todo',todo1)
			start = todo1.pop()
			edges1 = autom1.transition[str(start[0])]
			edges2 = autom2.transition[str(start[1])]
			tempdest = []
			for edge in edges2:
				dest = (int(start[0]),int(edge[0]))
				fail = 0
				print('dest',dest)
				print('tempdest',tempdest)
				print('var',varstates)
				if dest in tempdest:
					fail = 2
				else:
					tempdest.append(dest)
				

				if not seen1 & {dest}:
					seen1.add(dest)
					getvar1 = varstates1[str(dest[0])]
					getvar2 = varstates2[str(dest[1])]
					print('getvar1',getvar1)
					print('getvar2',getvar2)
					order1 = list(autom1.varstates)
					order2 = list(autom2.varstates)
					print('order1',order1)
					print('order2',order2)
					varstates[str(dest)] = []
					for state in auto.varstates:
						find = 0					
						print('state',state)
						for i in range(len(order1)):
							print('i',i)
							print('order1[i]',order1[i])
							print('getvar1[i]',getvar1[i])
							if str(state) == str(order1[i]):
								print('same order1[i]')
								for j in range(len(order2)):
									print('j',j)
									print('order2[j]',order2[j])
									print('getvar2[j]',getvar2[j])
									if str(state) == str(order2[j]):
										print('same order2[j]')
										find = 1
										if getvar1[i] != getvar2[j]:
											fail = 1
										else:
											varstates[str(dest)].append(getvar1[j])
											print('varstates[str(dest)]',varstates[str(dest)])


									elif find == 1 or fail == 1:
										break
									elif j == len(order2)-1 and find == 0:
										varstates[str(dest)].append(getvar1[i])
										find = 1
										print('varstates[str(dest)]',varstates[str(dest)])
										
							elif find == 1 or fail == 1:
								break

							elif i == len(order1)-1 and find == 0:
								for k in range(len(order2)):
									print('k',k)
									print('order2[k]',order2[k])
									print('getvar2[k]',getvar2[k])
									if str(state) == str(order2[k]):
										varstates[str(dest)].append(getvar2[k])
										print('varstates[str(dest)]',varstates[str(dest)])
										find = 1
										break
				if fail == 0:
					
					if edge[1][-1] in ext:
						temptup = (str(dest),'[epsi]')
					else:
						temptup = (str(dest),edge[1])
					
					if not str(start) in auto.transition:
						auto.transition[str(start)] = []
						#auto.transition[str(start)] = []

					auto.transition[str(start)].append(temptup)
					if str(start) != str(dest) and (not done&{dest}):
						todo1.add(dest)

				elif fail == 1:
					del varstates[str(dest)]

			for edge in edges1:
				dest = (int(edge[0]),int(start[1]))
				fail = 0
				print('dest',dest)
				print('tempdest',tempdest)
				print('var',varstates)
				if dest in tempdest:
					fail = 2
				else:
					tempdest.append(dest)

				if not seen1 & {dest}:
					seen1.add(dest)
					getvar1 = varstates1[str(dest[0])]
					getvar2 = varstates2[str(dest[1])]
					print('getvar1',getvar1)
					print('getvar2',getvar2)
					order1 = autom1.varstates
					order2 = autom2.varstates
					print('order1',order1)
					print('order2',order2)
					varstates[str(dest)] = []
					for state in auto.varstates:
						find = 0					
						print('state',state)
						for i in range(len(order1)):
							print('i',i)
							print('order1[i]',order1[i])
							print('getvar1[i]',getvar1[i])
							if str(state) == str(order1[i]):
								print('same order1[i]')
								for j in range(len(order2)):
									print('j',j)
									print('order2[j]',order2[j])
									print('getvar2[j]',getvar2[j])
									if str(state) == str(order2[j]):
										print('same order2[j]')
										find = 1
										if getvar1[i] != getvar2[j]:
											fail = 1
										else:
											varstates[str(dest)].append(getvar1[j])
											print('varstates[str(dest)]',varstates[str(dest)])


									elif find == 1 or fail == 1:
										break
									elif j == len(order2)-1 and find == 0:
										varstates[str(dest)].append(getvar1[i])
										find = 1
										print('varstates[str(dest)]',varstates[str(dest)])
										


							elif find == 1 or fail == 1:
								break

							elif i == len(order1)-1 and find == 0:
								for k in range(len(order2)):
									print('k',k)
									print('order2[k]',order2[k])
									print('getvar2[k]',getvar2[k])
									if str(state) == str(order2[k]):
										varstates[str(dest)].append(getvar2[k])
										print('varstates[str(dest)]',varstates[str(dest)])
										find = 1
										break
				if fail == 0:
					
					if edge[1][-1] in ext:
						temptup = (str(dest),'[epsi]')
					else:
						temptup = (str(dest),edge[1])
					
					if not str(start) in auto.transition:
						auto.transition[str(start)] = []
						#auto.transition[str(start)] = []

					auto.transition[str(start)].append(temptup)
					if start != dest and (not done&{dest}):
						todo1.add(dest)

				elif fail == 1:
					del varstates[str(dest)]

			done.add(start)



		auto.printauto()
		printgraph(auto,1)




				

		'''
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
		print(auto.transition)

		inputstr = input('Enter your string: ')

	
		print ('varstates',varstates)

		graph = gengraphs(auto,inputstr,varstates)
		print(graph)
		#time.sleep(5)

		finalauto = final(auto.end,graph,varstates,2)

		outputing(graph, varstates, inputstr, auto.start, -1)

	elif int(x) == 4:
		inputprint = input('Print Graph: yes=0, no=any \n')
		if int(inputprint) == 0:
			printgraph(autom,1)
	
		inputstr = input('Enter your string: ')

		varstates1 = functionalitychk(autom1,'-1')
		varstates2 = functionalitychk(autom2,'-1')

		print ('varstates1',varstates1)
		print ('varstates2',varstates2)

		graph1 = gengraphs(autom1,inputstr,varstates1)
		graph2 = gengraphs(autom2,inputstr,varstates2)

		#finalauto1 = final(autom1.end,graph1,varstates1,3)
		#finalauto2 = final(autom2.end,graph2,varstates2,4)

		print('g1',graph1)
		print('g2',graph2)
		disjoint = 1
		pos = []
		pos.extend(autom1.varstates)
		for v in autom2.varstates:
			if v in autom1.varstates:
				disjoint = 0
			else:
				pos.append(v)
		start = (autom1.start,autom2.start)
		end = (autom1.end,autom2.end)
		nvarstates = {}
		posstate = {}
		for state in pos:
			for i in range(len(autom1.varstates)):
				if state == autom1.varstates[i]:
					pos1 = i
				elif i == len(autom1.varstates)-1:
					pos1 = -1
			for j in range(len(autom2.varstates)):
				if state == autom2.varstates[j]:
					pos2 = j
				elif j == len(autom2.varstates)-1:
					pos2 = -1 
			posstate[state] = (pos1,pos2)


		cgraph = {}
		doing = {(0,0)}
		for i in range(-1,len(inputstr)):
			cgraph[i] = {}
			print('doing',doing)
			temp = set([])
			while doing:
				get = doing.pop()
				if i == -1:
					cgraph[i]['0'] = set([])
					toadd = cgraph[i]['0']
				else:
					cgraph[i][str(get)] = set([])
					toadd = cgraph[i][str(get)]

				print ('c',cgraph)
				
				for item1 in graph1[i][str(get[0])]:
					for item2 in graph2[i][str(get[1])]:

						add = 0
						'''
						if disjoint == 1:
							add = 1
						else:
						'''
						tup4 = (int(item1),int(item2))
						print ('tup',tup4)
						varss = []
						for var in pos:
							posi = posstate[var]
							print('posi',posi)
							if posi[0] != -1 and posi[1] != -1:
								if varstates1[item1][posi[0]] != varstates2[item2][posi[1]]:
									add = 0
									break
							else:
								add = 1




						'''
						for key, pos2 in posstate.items():
							print ('key',key)
							print ('pos',pos2)
							if pos2[0] != -1 and pos2[1] != -1:
								if varstates1[pos2[0]] == varstates2[pos2[1]]:
									add = 1
								else:
									add = 0
							if pos2[0] == -1 or pos2[1] == -1:
								add = 1
						'''
						if add == 1:
							toadd.add(str(tup4))
							temp.add(tup4)
							if not tup4 in nvarstates:
								varss = []
								for var in pos:
									posi = posstate[var]
									if posi[0] != -1:
										varss.append(varstates1[item1][posi[0]])
									elif posi[1] != -1:
									 	varss.append(varstates2[item2][posi[1]])

								nvarstates[str(tup4)] = []
								nvarstates[str(tup4)].extend(varss)
			
			doing = temp

		print('cg',cgraph)
		print('var',nvarstates)

		finalauto = final(str(end),cgraph,nvarstates,2)

		outputing(cgraph, nvarstates, inputstr, str(end), -1)





		












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
	if int(inputprint) == 0:
		printgraph(autom,1)
	
	inputstr = input('Enter your string: ')

	varstates = functionalitychk(autom,'-1')

	print ('varstates all',varstates)

	graph = gengraphs(autom,inputstr,varstates)

	finalauto = final(autom.end,graph,varstates,2)

	print ('varstates',autom.varstates)
	time.sleep(1)

	num1 = input('choose var operation: , all == -1 \n')
	temp4 = list(autom.varstates)
	for i in range(len(temp4)):
		if str(num1) == str(temp4[i]):
			num1 = i
			break

	outputing(graph, varstates, inputstr, autom.start, num1)

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

	graph = gengraphs(autom,inputstr,varstates)

	finalauto = final(autom.end,graph,varstates,2)

	print ('varstates',autom.varstates)
	time.sleep(2)
	outputing(graph, varstates, inputstr, autom.start, -1)