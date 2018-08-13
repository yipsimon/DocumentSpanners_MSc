import script2rev as sc2
import scriptgrph as sg
import functools
import threading, time, sys, copy, re
import texttable as txttab 


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

def csymtonulllong(auto):
	ext = ['+','-']
	for key, edges in auto.transition.items():
		copy1 = copy.deepcopy(edges)
		for edge in edges:
			if edge[1][-1] in ext:
				copy1.remove(edge)
				newedge = (edge[0],'[epsi]')
				copy1.append(newedge)
		auto.transition[key] = copy1

def getvarconfig(auto,openlist,closelist):
	finallist = {}
	key = {}	
	template = list()
	
	for i in range(len(auto.varstates)):
		key[str(auto.varstates[i])] = i
		template.append('w')

	#Creating Empty Spaces for dictionaries
	for item in auto.states:
		finallist[str(item)] = list()
		finallist[str(item)].extend(template)

	for node in auto.states:
		print('node',node)
		opp = openlist[node]
		cpp = closelist[node]
		for config in auto.varstates:
			if opp & {config} and cpp & {config}:
				finallist[node][key[config]] = 'c'
			elif opp & {config} and not cpp & {config}:
				finallist[node][key[config]] = 'o'

	return finallist, key

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
	#varedges = []	#To store edges with varconfigurations
	
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
					#tuptemp = (origin,item)
					#varedges.append(tuptemp)

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
					#tuptemp = (origin,item)
					#varedges.append(tuptemp)
				
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
	for node in auto.states:
		opp = openlist[node]
		cpp = closelist[node]
		for config in auto.varstates:
			if opp & {config} and cpp & {config}:
				finallist[node][key[config]] = 'c'
			elif opp & {config} and not cpp & {config}:
				finallist[node][key[config]] = 'o'

	auto.varconfig = finallist
	auto.key = key
	#return finallist, key #, varedges
	#return openlist, closelist

def csymtonull(auto,varedges):
	for edge in varedges:
		auto.transition[edge[0]].remove(edge[1])
		newedge = (edge[1][0],'[epsi]')
		auto.transition[edge[0]].append(newedge)


	

def foundepsilon(auto,finalgraph,currentnode,edgenode,text,letterpos,extratodo):
	for edge in auto.transition[edgenode]:
		#if edge[1] == text[letterpos] or edge[1] == '[sum]':
		if edge[1] != '[epsi]':
			matching = re.match(edge[1],text[letterpos])
			if matching:
				print('foundmatch2')
				if letterpos == len(text)-1:
					if edge[0] == str(auto.end):
						finalgraph[letterpos][currentnode].add(edge[0])		
				else:
					finalgraph[letterpos][currentnode].add(edge[0])
				extratodo.add(edge[0])
		elif edge[1] == '[epsi]' and auto.varconfig[edgenode] == auto.varconfig[edge[0]]:
			foundepsilon(auto,finalgraph,currentnode,edge[0],text,letterpos,extratodo)

def generateAg(auto,text):
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
			
			#if tup[1] == text[0]:
			if tup[1] != '[epsi]':
				matching = re.match(tup[1],text[0])
				if matching:
					nxsetnodes.add(item)
					finalgraph[-1]['0'].add(item)
			if tup[1] == '[epsi]' and ({str(tup[1])} not in seenlist):
				tochecklist.add(str(tup[0]))
	
	print('nxsetnodes \n',nxsetnodes)

	
	for i in range(len(text)):
		nexttodo = set([])
		while nxsetnodes:
			extratodo = set([])
			currentnode = nxsetnodes.pop()
			print('currentnode',currentnode)
			print('currentnode, tran',auto.transition[currentnode])

			for edge in auto.transition[currentnode]:
				print('edge',edge)

				#if edge[1] == text[i] or edge[1] == '[sum]':
				if edge[1] != '[epsi]':
					print(edge[1])
					#time.sleep(2)
					matching = re.match(edge[1],text[i])
					print('foundmatch')
					if matching:
						if i == len(text)-1:
							if edge[0] == str(auto.end):
								ifnotlv3(finalgraph, i, currentnode)
								finalgraph[i][currentnode].add(edge[0])	
						else:
							ifnotlv3(finalgraph, i, currentnode)
							finalgraph[i][currentnode].add(edge[0])

					extratodo.add(edge[0])
				elif edge[1] == '[epsi]' and auto.varconfig[currentnode] == auto.varconfig[edge[0]]:
					ifnotlv3(finalgraph, i, currentnode)
					foundepsilon(auto,finalgraph,currentnode,edge[0],text,i,extratodo)
			print(finalgraph)
			print('extratodo',extratodo)
			#seenlist = set([])
			#states = finallist[currentnode]
			while extratodo:
				extranode = extratodo.pop()
				print('extranode',extranode)
				#seenlist.add(extranode)
				#print('extranode trans',auto.transition[extranode])
				for edge in auto.transition[extranode]:
					print('edge',edge)
					if edge[1] == '[epsi]' and auto.varconfig[extranode] != auto.varconfig[edge[0]]:
						print('match3')
						if i == len(text)-1:
							if edge[0] == str(auto.end):
								ifnotlv3(finalgraph, i, currentnode)			
								finalgraph[i][currentnode].add(edge[0])		
						else:
							ifnotlv3(finalgraph, i, currentnode)			
							finalgraph[i][currentnode].add(edge[0])
						#if edge[0] not in seenlist:
						extratodo.add(edge[0])
						#states = finallist[edge[0]]
					elif edge[1] == '[epsi]' and auto.varconfig[extranode] == auto.varconfig[edge[0]]:
						print('match4')
						if edge[0] == str(auto.end):
							finalgraph[i][currentnode].add(edge[0])
						else:
							#if edge[0] not in seenlist:
							extratodo.add(edge[0])
				print('extratodo0',extratodo)
			if currentnode in finalgraph[i]:
				nexttodo = nexttodo | finalgraph[i][currentnode]
			print(finalgraph)
			print('extratodo',extratodo)
			

		print(finalgraph)
		
		print('nxsetnodes',nxsetnodes)
		print('nexttodo',nexttodo)
		nxsetnodes = nxsetnodes | nexttodo
		print('nxsetnodes \n\n\n\n',nxsetnodes)


		
		#print('finalgraph \n', finalgraph)
		#time.sleep(4)
	
	tokeepnodes = set([str(auto.end)])
	print('tokeepnodes',tokeepnodes)
	for i in range(len(text)-1,-2,-1):
		print('i',i)
		updatetokeep = set([])
		list0 = list(finalgraph[i].keys())
		print ('list0',list0)
		for key in list0:
			print('key',key)
			list1 = list(finalgraph[i][key])
			print ('list1',list1)
			for item in list1:
				print('item',item)
				if {str(item)} & tokeepnodes:
					updatetokeep.add(key)
				else:
					finalgraph[i][key].remove(item)

			
			if len(finalgraph[i][key]) == 0:
				del finalgraph[i][key]
		print('finalgraph \n', finalgraph)
		print ('updatetokeep',updatetokeep)
		tokeepnodes = set([])
		tokeepnodes = tokeepnodes | updatetokeep
		print ('tokeepnodes',tokeepnodes)
		

	#print('\nfinalgraph \n', finalgraph)
	
	

	return finalgraph


def finalauto(auto,graph):
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
				value = auto.varconfig[edge]
				end = (positions+1, edge)
				tup = (end,value)
				finalgraph[str(start)].append(tup)

			if positions > final:
				final = positions

	endnode = (final+1,str(auto.end))

	return finalgraph, endnode


def printresults(listofoutputs):
	print ('\n results')
	for i in range(len(listofoutputs)):
		print (listofoutputs[i])


def printresultsv2(listofoutputs,auto):
	print ('\n results')
	key1 = {}
	key2 = {}
	key3 = {}
	tempkey = {}
	for item in auto.varstates:
		tempkey[str(item)] = []

	for i in range(len(listofoutputs)):
		key1[i] = listofoutputs[i]
		key3[i] = {}

	print(key1)
	print(key3)
	print(tempkey)

	for i in range(len(listofoutputs)):
		jend = 0
		for j in range(len(listofoutputs[i])):
			print('j',j)
			if jend == 1:
				break
			print(listofoutputs[i][j])
			if j == 0 or listofoutputs[i][j] != listofoutputs[i][j-1]:
				print('cond 1')
				for k in range(len(listofoutputs[i][j])):
					print('k',k)
					if listofoutputs[i][j][k] == 'o':
						if j == 0:
							tempkey[auto.varstates[k]].append(j+1)
							print('results1')
						else:
							if listofoutputs[i][j-1][k] != listofoutputs[i][j][k]:
								tempkey[auto.varstates[k]].append(j+1)
								print('results2')
					elif listofoutputs[i][j][k] == 'c':
						if j == 0:
							tempkey[auto.varstates[k]].append(j+1)
							tempkey[auto.varstates[k]].append(j+1)
							print('results3')
						else:
							if listofoutputs[i][j-1][k] != listofoutputs[i][j][k]:
								tempkey[auto.varstates[k]].append(j+1)
								if len(tempkey[auto.varstates[k]]) == 1:
									tempkey[auto.varstates[k]].append(j+1)
								print('results4')

		for key, item in tempkey.items():
			tempkey[key] = tuple(item)
		print(tempkey)
		key3[i] = copy.deepcopy(tempkey)
		print(key3)
		for item in auto.varstates:
			tempkey[str(item)] = []
		print(tempkey)
	
	#print('k1',key1)
	#print('k3',key3)


	tab = txttab.Texttable()
	headings = ['ConfigVariable']
	for v in range(len(auto.varstates)):
		headings.append(auto.varstates[v])

	tab.header(headings)
	for i in range(len(listofoutputs)):
		#print (' config variables: ', key1[i])
		temp = [key1[i]]
		for v in range(len(auto.varstates)):
			temp.append(key3[i][auto.varstates[v]])
		tab.add_row(temp)
	
	s = tab.draw()
	print(s)

	'''
	#print(''.format('config variable',))
	for i in range(len(listofoutputs)):
		print (' config variables: ', key1[i])
		print (key3[i])
	'''

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
		listofoutputs.append(k)
		k = nextString(k,stacks,finalgraph,totallength,finallist,availableletters,letterofedges,template)
		print('\n\n\n')
		print('finalgraph',finalgraph)
		print('stacks',stacks)
		print('availableletters',availableletters)
		print('letterofedges',letterofedges)
		print('k',k)
	
	
	return listofoutputs
