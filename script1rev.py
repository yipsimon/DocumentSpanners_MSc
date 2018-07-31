import script2rev as sc2
import scriptgrph as sg
import functools
import threading, time, sys, copy


def ifnotlv1(table, key):
	if not key in table:
		table[key] = []

def ifnotlv2(table,key1,key2):
	if not key2 in table[key1]:
		table[key1] = key2

def ifnotlv3(table,key1,key2):
	if not key2 in table[key1]:
		table[key1][key2] = set([])

def ifnotlv4(table,key):
	if not key in table:
		table[key] = set([])

#Reading in a file and output as automaton object
def readauto(fname):
    f = open(fname, 'r')
    auto = sc2.automata(0,0,0)
    auto.reset()
    for line in f:
    	temp = line.split(';')
    	del temp[-1]
    	for item in temp:
    		item = item.split(',')
    		ifnotlv1(auto.transition, item[0])
    		ifnotlv1(auto.transition, item[1])
    		tup = (item[1],item[2])
    		auto.transition[item[0]].append(tup)
    		auto.states.add({item[0],item[1]})

    		if str(item[2][-1]) == '+':
    			if str(item[2][0]) not in auto.varstates:
    				auto.varstates.append(str(item[2][0]))
    		if int(item[0]) == 0:
    			auto.start = item[0]
    		if int(item[1]) > int(auto.end):
    			auto.end = item[1]
    f.close()
    #auto.tostr()
    return auto

#Functionality checks
def funchk(auto):
	openlist = {}
	closelist = {}
	finallist = {}	#Final output, {'node': [/varconfigurations]}
	key = {}		#Position of the specific varconfig, i.e. [x,y] => {'x': 0, 'y': 1}
	template = list()
	
	for i in range(len(auto.varstates)):
		key[str(auto.varstates[i])] = i
		template.append('w')

	#Creating Empty Spaces for dictionaries
	for item in auto.states:
		openlist[str(item)] = set([])
		closelist[str(item)] = set([])
		finallist[str(item)] = list()
		finallist[str(item)].extend(template)

	seenlist = {str(auto.start)}
	todolist = {str(auto.start)}
	varedges = []	#To store edges with varconfigurations
	
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
					tuptemp = (origin,item)
					varedges.append(tuptemp)

			elif item[1][-1] == '-':
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
					tuptemp = (origin,item)
					varedges.append(tuptemp)
				
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

	#Generate 'w','o','c' for each node based on openlist, closelist
	print('openlist',openlist)
	print('closelist',closelist)
	print('autostates',auto.states)
	for node in auto.states:
		print('node',node)
		opp = openlist[node]
		cpp = closelist[node]
		for config in auto.varstates:
			if opp & {config} and cpp & {config}:
				finallist[node][key[config]] = 'c'
			elif opp & {config} and not cpp & {config}:
				finallist[node][key[config]] = 'o'


	return finallist, key, varedges

def csymtonull(auto,varedges):
	for edge in varedges:
		auto.transition[edge[0]].remove(edge[1])
		newedge = (edge[1][0],'[epsi]')
		auto.transition[edge[0]].append(newedge)

def projectionv1(auto,projections):
	ext = ['+','-']
	for key, edges in auto.transitions.items():
		for edge in edges:
			if edge[1][-1] in ext:
				if edge[1][0] not in projection:
					auto.transition[key].remove(edge)
					newedge = (edge[0],'[epsi]')
					auto.transition[edge[0]].append(newedge)

def foundepsilon(auto,finalgraph,currentnode,edgenode,text,letterpos,nexttodo,extratodo,finallist):
	for edge in auto.transition[edgenode]:
		if edge[1] == text[letterpos] or edge[1] == '[sum]':
			if letterpos == len(text)-1:
				if edge[0] == auto.end:
					finalgraph[letterpos][currentnode].add(edge[0])		
			else:
				nexttodo.add(edge[0])
				finalgraph[letterpos][currentnode].add(edge[0])
			extratodo.add(edge[0])
		elif edge[1] == '[epsi]' and finallist[edgenode] == finallist[edge[0]]:
			foundepsilon(auto,finalgraph,currentnode,edge[0],text,letterpos,nexttodo,extratodo,finallist)

def generateAg(auto,text,finallist):
	finalgraph = {}
	for i in range(len(text)):
		finalgraph[i] = {}
	finalgraph[-1] = {'0': set([])}

	#To obtain all possible paths, we iterate the edges stored in auto.
	#First, we need to determine initial valid node to start
	tochecklist = set([str(auto.start)])
	nxsetnodes = set([])
	seenlist = set([str(auto.start)])
	while tochecklist:
		item = tochecklist.pop()
		seenlist.add(item)
		for tup in auto.transition[item]:
			if tup[1] == text[0]:
				nxsetnodes.add(key)
				finalgraph[-1]['0'].add(key)
			if tup[1] == '[epsi]' and ({str(tup[1])} not in seenlist):
				tochecklist.add(str(tup[0]))

	for key, edges in auto.transition.items():
		extra = set([])
		for edge in edges:
			if edge[1] == text[0] or edge[1] == '[sum]':
				
			elif edge[1] == '[epsi]' and finallist[key] != finallist[edge[0]]:
				extra.add(edge[0])
		print ('extra',extra)
		while extra:
			exnode = extra.pop()
			for edge in auto.transition[exnode]:
				if edge[1] == text[0] or edge[1] == '[sum]':
					todonodes.add(key)
					finalgraph[-1]['0'].add(key)
				elif edge[1] == '[epsi]' and finallist[exnode] != finallist[edge[0]]:
					extra.add(edge[0])
	print('finalgraph',finalgraph)
	print('todonodes \n',todonodes)

	#time.sleep(4)
	for i in range(len(text)):
		nexttodo = set([])
		while todonodes:
			extratodo = set([])
			currentnode = todonodes.pop()

			for edge in auto.transition[currentnode]:
				if edge[1] == text[i] or edge[1] == '[sum]':
					ifnotlv3(finalgraph, i, currentnode)
					if i == len(text)-1:
						if edge[0] == auto.end:
							finalgraph[i][currentnode].add(edge[0])	
					else:
						nexttodo.add(edge[0])
						finalgraph[i][currentnode].add(edge[0])
					extratodo.add(edge[0])
				elif edge[1] == '[epsi]' and finallist[currentnode] == finallist[edge[0]]:
					ifnotlv3(finalgraph, i, currentnode)
					foundepsilon(auto,finalgraph,currentnode,edge[0],text,i,nexttodo,extratodo,finallist)

			while extratodo:
				extranode = extratodo.pop()
				for edge in auto.transition[extranode]:
					if edge[1] == '[epsi]' and finallist[extranode] != finallist[edge[0]]:
						ifnotlv3(finalgraph, i, currentnode)
						if i == len(text)-1:
							if edge[0] == auto.end:
								finalgraph[i][currentnode].add(edge[0])		
						else:
							nexttodo.add(edge[0])
							finalgraph[i][currentnode].add(edge[0])
						extratodo.add(edge[0])
					elif edge[1] == '[epsi]' and finallist[currentnode] == finallist[edge[0]]:
						extratodo.add(edge[0])
		
		print('todonodes',todonodes)
		print('nexttodo',nexttodo)
		todonodes = todonodes | nexttodo
		print('todonodes',todonodes)


		print('finalgraph \n', finalgraph)
		#time.sleep(4)
	
	tokeepnodes = set([str(auto.end)])
	print('tokeepnodes',tokeepnodes)
	for i in range(len(text)-1,-2,-1):
		print('i',i)
		updatetokeep = set([])
		list0 = list(finalgraph[i].keys())
		for key in list0:
			list1 = list(finalgraph[i][key])
			for edges in list1:
				print('edges',edges)
				for item in edges:
					if {item} & tokeepnodes:
						updatetokeep.add(key)
					else:
						finalgraph[i][key].remove(item)
			
			if len(finalgraph[i][key]) == 0:
				del finalgraph[i][key]

		tokeepnodes = set([])
		tokeepnodes = tokeepnodes | updatetokeep

	print('finalgraph \n', finalgraph)
	time.sleep(10)

	return finalgraph


def finalauto(graph,finallist,last):
	print('graph',graph)
	finalgraph = {}
	final = -1
	for positions, nodes in graph.items():
		for begining, ending in nodes.items():
			print('positions',positions)
			print('nodes',nodes)
			if positions == -1:
				start = 'q0'
			else:
				start = (positions, begining)

			print('start',start)

			ifnotlv1(finalgraph,str(start))
			for edge in ending:
				value = finallist[edge]
				end = (positions+1, edge)
				tup = (end,value)
				finalgraph[str(start)].append(tup)

			if positions > final:
				final = positions

		print('autotrani',positions,finalgraph)
		#time.sleep(5)	

	endnode = (final+1,str(last))
	autograph = sc2.automata(0,0,0)
	autograph.reset()
	autograph.start = 'q0'
	autograph.end = str(endnode)
	autograph.transition = finalgraph
	print('autotran',autograph.transition)
	#time.sleep(10)

	return autograph




def printresults(listofoutputs):
	print ('\n results')
	for i in range(len(listofoutputs)):
		print (listofoutputs[i])

def projectionv2(finallist,key,listofprojections):
	tokeep = []
	for item in listofprojections:
		tokeep.append(key[item])

	for key, item in finallist:
		temp = []
		for pos in tokeep:
			temp.append( item[pos] )
		finallist[key] = temp




def minString(integer,stacks,finalgraph,totallength,finallist,availableletters,letterofedges,template):
	finalstring = []
	for i in range(integer, totallength-1):
		for availablenode in stacks[i]:
			if str(availablenode) in finalgraph[i]:
				for item in finalgraph[i][availablenode]:
					if not finallist[item] in availableletters[i+1]:
						availableletters[i+1].append( finallist[item] )
					if str(finallist[item]) not in letterofedges[i+1]:
						letterofedges[i+1][str(finallist[item])] = set([])	
					letterofedges[i+1][str(finallist[item])].add(item)
		
		for j in range(len(availableletters[i+1][0])-1,-1,-1):
			availableletters[i+1].sort(key=lambda tup: tup[j], reverse=1)

		finalstring.append(availableletters[i+1][0])
		
		stacks[i+1] = stacks[i+1] | letterofedges[i+1][str(availableletters[i+1][0])]	
		
		#del availableletters[i][0]	

	if template == ['0']:
		copying = copy.deepcopy(availableletters[integer+1][0])

		for k in range(len(copying)):
			copying[k] = 'c'

		finalstring.append(copying)	

		return copying, finalstring
	else:
		finalstring.append(template)	

		return finalstring

def nextString(currentstring,stacks,finalgraph,totallength,finallist,availableletters,letterofedges,template):
	print('\n\n\n\n')
	print('currentstring',currentstring)
	for i in range(totallength-1,-1,-1):
		print('i',i)	
		print('currentstringi',currentstring[i])
		print('availableletters',availableletters)
		if len(availableletters[i]) != 1:
			availableletters[i].remove( currentstring[i] )
			print('availableletters2',availableletters)
			finalstring = currentstring[0:i]
			print('finalstringbe',finalstring)
			finalstring.append(availableletters[i][0])
			print('finalstringaf',finalstring)
			print('letterofedges',letterofedges[i])
			stacks[i] = letterofedges[i][str(availableletters[i][0])]
			print('stacks',stacks)
	
			lastpart = minString(i,stacks,finalgraph,totallength,finallist,availableletters,letterofedges,template)
			finalstring.extend(lastpart)
			print('finalstringend',finalstring)
			return finalstring

		else:
			stacks[i] = set([])
			letterofedges[i] = {}
			availableletters[i] = []
			print('availableletters',availableletters[i])
	return []

def calcresults(finalgraph,totallength,finallist):
	stacks = {}
	availableletters = {}
	letterofedges = {}
	stacks[-1] = {'0'}

	for i in range(0,totallength+1):
		stacks[i] = set([])
		availableletters[i] = []
		letterofedges[i] = {}		

	template, k = minString(-1,stacks,finalgraph,totallength,finallist,availableletters,letterofedges,['0'])
	print('template',template,'k',k)
	#time.sleep(4)
	listofoutputs = []
	print('\n\n\n')
	print('finalgraph',finalgraph)
	print('stacks',stacks)
	print('availableletters',availableletters)
	print('letterofedges',letterofedges)

	while k != []:
		listofoutputs.append(str(k))
		k = nextString(k,stacks,finalgraph,totallength,finallist,availableletters,letterofedges,template)
		print('\n\n\n')
		print('finalgraph',finalgraph)
		print('stacks',stacks)
		print('availableletters',availableletters)
		print('letterofedges',letterofedges)
		print('k',k)
	
	
	return listofoutputs
