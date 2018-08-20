import script2rev as sc2
import scriptgrph as sg
import functools
import threading, time, sys, copy, re
import texttable as txttab 

def ifnotlv1(table, key):
	if not key in table:
		table[key] = []

def ifnotlv3(table,key1,key2):
	if not key2 in table[key1]:
		table[key1][key2] = set([])

"""
Read a txt file and output as automata object
txt file must have the format: startnode,endnode,value; startnode, ...
to represent edges of the automaton. nodes has to be in int format.
+ represent open variable, - is close variable.
Input: txt file, Output: Automata Object (in str form)
"""
def readauto(fname):
	auto = sc2.automata(0,0,0)
	auto.reset()
	f = open(fname, 'r')
	for line in f:
		temp = line.split(';')
		del temp[-1]
		for item in temp:
			item = item.split(',')
			ifnotlv1(auto.transition, item[0])
			ifnotlv1(auto.transition, item[1])
			tup = (item[1],item[2])
			auto.transition[item[0]].append(tup)
			auto.states.append(item[0])
			auto.states.append(item[1])
			if str(item[2][-1]) == '+':
				if str(item[2][0]) not in auto.varstates:
					auto.varstates.append(str(item[2][0]))
			if int(item[0]) == 0:
				auto.start = item[0]
			if int(item[1]) > int(auto.end):
				auto.end = item[1]
				auto.last = item[1]
	f.close()
	auto.tostr()
	return auto

"""
This function convert all variable states values to [epsi].
Perform only after funchk(). 
Input: Automata Object, Output: The Same Automata Object
"""
def csymtonulllong(auto): #Changed, testing
	ext = ['+','-']
	for key, edges in auto.transition.items():
		#Make a copy of the edges available from the node(key). Transition Format: {node: [(endnode,value),(),...], ...}
		copy1 = [] 
		for edge in edges: #O(n), edge = (endnode, value)
			#If the last letter of the value is either + or -, the function will assume that it is a state contain variable state.
			if edge[1][-1] in ext and len(edge[1]) > 1:
				newedge = (edge[0],'[epsi]')
				copy1.append(newedge) #O(1)
			else:
				copy1.append(edge) #O(1)
			#It is possible to use the varstate information obtained from funchk() instead.
		auto.transition[key] = copy1

"""
Functionality Test for automata object, to check whether the automata is functional, with no overlapping
variable configuration for each node. Input: Automata object, Output:Automata Object (with key and varstates filled in)
"""
def funchk(auto):
	openlist = {}	#Dictionary of all nodes with a set of variable states that has been opened
	closelist = {}	#Dictionary of all nodes with a set of variable states that has been closed
	finallist = {}	#Variable configuration values in automata object for all node in autoamta, format {'node': [/varconfigurations]}
	key = {}		#Position of the specific variable config, i.e. [x,y] => {'x': 0, 'y': 1}
	template = list()	#Default template for variable configuration, i.e. [w,w], the key above is used to indicate variable configuration for which variable state
	#Note to self, the format {'node': {'varstate': varconfig, 'varstate': varconfig, ... }}, is also possible, consider for future implementation
	
	#Set positions for variable states, create the default templeta using the number of varstates.
	for i in range(len(auto.varstates)):
		key[str(auto.varstates[i])] = i
		template.append('w')

	#Creating Empty Spaces for dictionaries
	for item in auto.states:
		openlist[str(item)] = set([])
		closelist[str(item)] = set([])
		finallist[str(item)] = list()
		finallist[str(item)].extend(template)
		#Extend template, not = template, = change all items if value changed

	seenlist = {str(auto.start)}	#Store seen nodes
	todolist = {str(auto.start)}	#Store nodes for processing
	
	while todolist:	
		origin = todolist.pop() #Return an element from the right side
		for item in auto.transition[origin]:
			dest = str(item[0])
			letter = item[1][0]
			op = openlist[dest]
			oq = openlist[str(origin)]
			cp = closelist[dest]
			cq = closelist[str(origin)]

			#Find + from value of the edge, indicating a change of variable configuration
			if item[1][-1] == '+' and len(item[1]) > 1:
				#If the variable state if already opened
				if oq & {letter}:	
					print ('Error from open: Variable state',letter,'have multiple open, not functional')
					sys.exit(1)	#The automata is not functional. stop program
				#If destination node is in seenlist
				if seenlist & {dest}:	#The destination node of the edge has already been processed, so there are existing values in openlist and closelist for that node
					#If the openlist value of the destination node is not the same as the start node of the openlist added with the variable state that will be opened
					#or if the closelists value does not match, (since both nodes has been processed, there should be no change since it is open transition between the nodes)
					if op != (oq | {letter}) or cp != cq:	
						print ('Error from opne: Obtained multiple variable configuration for one node')
						sys.exit(1)
				else:
					#Destination node processed, destination node is opened with corresponding variable state
					seenlist.add(dest)
					todolist.add(dest)
					openlist[dest] = (openlist[origin] | {letter})
					closelist[dest] = closelist[origin]

			#Find - from value of the edge, indicating a change of variable configuration
			elif item[1][-1] == '-' and len(item[1]) > 1:
				#Check if variable state is opened from the start node or whether the variable state has been closed before.
				if {letter} - oq or cq & {letter}:
					print ('Error from close: Either the variable state has not opened or its has already closed')
					sys.exit(1)
				if seenlist & {dest}:
					#If openlist value of start and destination node are different, or variable states is not closed at destination node
					if op != oq  or cp != (cq | {letter}):
						print ('not function different states for one node')
						sys.exit(1)
				else:
					#Destination node processed, node is closed with corresponding variable state
					seenlist.add(dest)
					todolist.add(dest)
					openlist[dest] = openlist[origin] 
					closelist[dest] = (closelist[origin] | {letter})
			
			#Nothing is opened or closed.
			else:
				if seenlist & {dest}:
					if op != oq  or cp != cq:
						print ('Error normal: Multiple variable states for one node')
						sys.exit(1)
				else:
					seenlist.add(dest)
					todolist.add(dest)
					openlist[dest] = openlist[origin] 
					closelist[dest] = closelist[origin]	

	#Using the openlist and closelist, for each node, we can determine whether the variable state is waiting, open or closed 
	for node in auto.states:
		opp = openlist[node]
		cpp = closelist[node]
		for config in auto.varstates:
			if opp & {config} and cpp & {config}:	#If variable state is in both openlist and closelist
				finallist[node][key[config]] = 'c'
			elif opp & {config} and not cpp & {config}:	#If the variable state is in openlist but not closelist
				finallist[node][key[config]] = 'o'
			#All node have the default template of [w,w,..], not need to change to waiting.

	auto.varconfig = finallist	
	auto.key = key

"""
This function activate when it read a [epsi] with not variable configuration changes between the start and end node of the edge.
A subfunction of generateAg(). To find an edge with value (letter or regex expression) that accept existing text[letterpos] (a letter),
Input: Automata, finalgraph //A dictionary, currentnode(to add to finalgraph), edgenode (node to iterate through), test, letterposition, extratodo
extratodo is a set to be used in generateAg() later.
Output: Nothing, it will add to valid nodes finalgraph and to extratodo.
"""
def foundepsilon(auto,finalgraph,currentnode,edgenode,text,letterpos,extratodo): #Changed, Testing
	for edge in auto.transition[edgenode]:
		#if edge[1] == text[letterpos] or edge[1] == '[sum]':
		if edge[1] != '[epsi]':
			matching = re.match(edge[1],text[letterpos])
			if matching:
				#If not last letter, add to finalgraph normally
				if letterpos == len(text)-1:
					#If last letter, only add nodes that are terminals in the automata to finalgraph
					if edge[0] == str(auto.end):
						finalgraph[letterpos][currentnode].add(edge[0])		
				else:
					finalgraph[letterpos][currentnode].add(edge[0])
				#If matchs, add node to extratodo for further processing in generateAg()
				extratodo.add(edge[0])
		#If no changes to variable configuration between start and end node, loop the function updated with new end node.
		elif edge[1] == '[epsi]' and auto.varconfig[edgenode] == auto.varconfig[edge[0]]:
			foundepsilon(auto,finalgraph,currentnode,edge[0],text,letterpos,extratodo)
		#If changes to variable configuration, ignore.

"""
This function generate a Ag graph which contain all possible paths for the given text.
Input: Automata object and string, Output: Ag graph in dictionary format: {positionoftext:{Available startnodes:[set of endnodes], }, }
"""
def generateAg(auto,text):
	finalgraph = {}
	#Set up empty variables
	for i in range(len(text)):
		finalgraph[i] = {}
	#-1 reference to q0 of the graph. '0' is just a placeholder, not node '0'
	finalgraph[-1] = {'0': set([])}
	
	tochecklist = set([str(auto.start)]) #Set of nodes to check
	nxsetnodes = set([])				#Set of to be iterated in the next position, (stored confirmed existing node in the graph for the current position)
	seenlist = set([str(auto.start)])	#Set to store processed node for the current letter
	#First, we need to determine initial valid nodes to start
	while tochecklist:
		item = tochecklist.pop()	#Started with auto.start as starting node of the automata
		seenlist.add(item)
		#print('s',seenlist)
		#Iterate avaiable edges for node
		#print(auto.transition[item])
		for tup in auto.transition[item]:
			#if tup[1] == text[0]:
			#Check if there is an edge that matching the first letter of the text
			if tup[1] != '[epsi]':
				#print(tup[1])
				matching = re.match(tup[1],text[0])
				if matching:
					#print('matched, item',item)
					nxsetnodes.add(item)
					finalgraph[-1]['0'].add(item)
			if tup[1] == '[epsi]' and ({str(tup[0])} not in seenlist):
				#Add end node of edges that are [epsi] to search differnt nodes that are connected
				tochecklist.add(str(tup[0]))
	#print(finalgraph[-1])
	#sys.exit(1)
	#Iterate through the text,
	ext2 = ['\n','\r','\t']
	for i in range(len(text)):
		nexttodo = set([])
		if not text[i] in ext2:
			#Iterate available nodes from previous letters (positions) in the graph
			while nxsetnodes:
				extratodo = set([])		#This set store end nodes that matchs the letter from the text
				#Note, the algorithm first find the path that contain the matching letter searching through edges of the popped node,
				#i.e 0 -> 1 with value 'a' or 0 -> 1 -> 2 with value [epsi] and 'a' respectively given that 0 -> 1 has no variable configuration changes
				#After finding the a, the algorithm will continue to search for path with [epsi] value which has varconfig changes, finding all possible ending node for that letter.
				currentnode = nxsetnodes.pop()
				#Iterate all edges from currentnode
				#if text[i] == '\n':
					#print('sstopp')
					#sys.exit(1)

				#if i == 13:
					#print(text[i])
					#time.sleep(1)

				for edge in auto.transition[currentnode]:
					#print(edge)
					#time.sleep(1)
					#if edge[1] == text[i] or edge[1] == '[sum]':
					#Check if there is an edge that matching the letter of the text
					#if i == 13:
						#print('e',edge[1])
					if edge[1] != '[epsi]':
						#print(edge[1])
						matching = re.match(edge[1],text[i])
						if matching:
							#If last letter, only add edges to point toward terminal
							if i == len(text)-1:
								if edge[0] == str(auto.end):
									ifnotlv3(finalgraph, i, currentnode)
									finalgraph[i][currentnode].add(edge[0])	
							else:
								ifnotlv3(finalgraph, i, currentnode)
								finalgraph[i][currentnode].add(edge[0])
							#Add the end node to set
							extratodo.add(edge[0])

					#[epsi] value, with no changes to varconfig, is just an empty edge, search from the end node of this empty edge for the letter
					elif edge[1] == '[epsi]' and auto.varconfig[currentnode] == auto.varconfig[edge[0]]:
						ifnotlv3(finalgraph, i, currentnode)
						foundepsilon(auto,finalgraph,currentnode,edge[0],text,i,extratodo)
				
				#Extratodo contain all end nodes for the currentnode
				while extratodo:
					extranode = extratodo.pop()
					#Iterate the edges of the node, find edges with varconfig changes and add its end node to finalgraph as a new path
					#,from currentnode to new end node
					for edge in auto.transition[extranode]:
						if edge[1] == '[epsi]' and auto.varconfig[extranode] != auto.varconfig[edge[0]]:
							if i == len(text)-1:
								if edge[0] == str(auto.end):
									ifnotlv3(finalgraph, i, currentnode)			
									finalgraph[i][currentnode].add(edge[0])		
							else:
								ifnotlv3(finalgraph, i, currentnode)			
								finalgraph[i][currentnode].add(edge[0])
							#if edge[0] not in seenlist:
							#Add end node of edge to set for searching, this will add paths with multiple varconfig changes
							extratodo.add(edge[0])
							#states = finallist[edge[0]]
						#Empty edges
						elif edge[1] == '[epsi]' and auto.varconfig[extranode] == auto.varconfig[edge[0]]:
							if edge[0] == str(auto.end):
								#Add path which end at the terminal node
								finalgraph[i][currentnode].add(edge[0])
							else:
								#if edge[0] not in seenlist:
								#Empty edges, add end node to search for more
								extratodo.add(edge[0])
				
				#Add node to nexttodo only if it exists in the graph, to prepare for the next letter
				if currentnode in finalgraph[i]:
					nexttodo = nexttodo | finalgraph[i][currentnode]
			#if i == 13:
				#print(finalgraph[i])
				#sys.exit(1)
			#Get a new set of available node for the next letter
			nxsetnodes = nxsetnodes | nexttodo
		#for pos in range(len(text)):
			#print('final i',pos,finalgraph[pos])
	#sys.exit(1)
	#Pruneing starts here, we want to keep all possible paths that are connected to the terminal node.
	tokeepnodes = set([str(auto.end)]) #keep the terminal node
	for i in range(len(text)-1,-2,-1):
		updatetokeep = set([]) #set of nodes that link from the tokeepnodes
		list0 = list(finalgraph[i].keys())	
		#Iterate through the key (startnode) from i
		for key in list0:
			list1 = list(finalgraph[i][key])
			#Iterate all edges fron key (startnode)
			for item in list1:
				#Only keep nodes that are in tokeepnodes
				if {str(item)} & tokeepnodes:
					updatetokeep.add(key)
				else:
					finalgraph[i][key].remove(item)
			#Delete key (startnode) if there is not edges left
			if len(finalgraph[i][key]) == 0:
				del finalgraph[i][key]
		#Update tokeepnode with updatatokeep
		tokeepnodes = set([])
		tokeepnodes = tokeepnodes | updatetokeep

	return finalgraph

"""
Create only the transition edges dictionary of the automata strictly for displaying the Ag graph in a proper format.
Input: Automata object, Graph (format: {name1: {name1.1: setvalues, name1.2: setvalues,...},...})
Output, Graph (format: {startnode: [(endnode1,edgevalue),(endnode2,edgevalue),...],...}), end node
"""
def finalauto(auto,graph):
	finalgraph = {}
	final = -1
	for positions, nodes in graph.items():
		for begining, ending in nodes.items():
			if positions == -1:
				start = 'q0'
			else:
				start = (positions, begining)

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

"""
Function to print results only in waiting, open and close format (w,o,c format)
"""
def printresults(listofoutputs):
	print ('\n results')
	for i in range(len(listofoutputs)):
		print (listofoutputs[i])

"""
Function to print results in a table format
"""
def printresultsv2(listofoutputs,auto,string,showstring=0,showconfig=0):
	print ('\n results')
	key1 = {}	#key correspond from int to w,o,c format
	key2 = {}	#key correspond from int to string format
	key3 = {}	#key correspond from int to varstate positions format x:[1,2], y:[2,4] etc
	
	tempkey = {}	#Temporary store varpos value 
	for item in auto.varstates:
		tempkey[str(item)] = []
		
	#Initialise and link keys
	for i in range(len(listofoutputs)):
		key1[i] = listofoutputs[i]
		key3[i] = {}
		key2[i] = {}

	#Iterate outputs
	for i in range(len(listofoutputs)):
		tempkey2 = []	#Termporary store string format
		#Iterate within output of w.o.c format
		for j in range(len(listofoutputs[i])):
			#Check for changes
			if j == 0 or listofoutputs[i][j] != listofoutputs[i][j-1]:
				#Iterate within w,o,c format i.e [w,w],[w,o],..., 
				for k in range(len(listofoutputs[i][j])):
					if listofoutputs[i][j][k] == 'o':
						if j == 0:
							tempkey[auto.varstates[k]].append(j+1) #+1 since we start from 0 and want 1 for pos
							tempkey2.append(auto.varstates[k]+'+')
						else:
							#Compare individual variable states
							if listofoutputs[i][j-1][k] != listofoutputs[i][j][k]:
								tempkey[auto.varstates[k]].append(j+1)
								tempkey2.append(auto.varstates[k]+'+')
					
					elif listofoutputs[i][j][k] == 'c':
						if j == 0:
							#Closed immediately
							tempkey[auto.varstates[k]].append(j+1)
							tempkey[auto.varstates[k]].append(j+1)
							tempkey2.append(auto.varstates[k]+'-')
						else:
							if listofoutputs[i][j-1][k] != listofoutputs[i][j][k]:
								tempkey[auto.varstates[k]].append(j+1)
								tempkey2.append(auto.varstates[k]+'-')
								#Closed immediately if length == 1 otherwise it would have been == 2
								if len(tempkey[auto.varstates[k]]) == 1:
									tempkey[auto.varstates[k]].append(j+1)
									tempkey2.append(auto.varstates[k]+'-')
			#Add placeholder letter for string
			if j != len(listofoutputs[i])-1:
				tempkey2.append('a')
		#Convert varpos format to tuple
		for key, item in tempkey.items():
			tempkey[key] = tuple(item)
		#Add to resp keys
		key3[i] = copy.deepcopy(tempkey)
		key2[i] = copy.deepcopy(tempkey2)
		#Initialise
		for item in auto.varstates:
			tempkey[str(item)] = []
	
	tab = txttab.Texttable(100)
	headings = ['No.']
	if showstring == 1:
		headings.append('String')
	if showconfig == 1:
		headings.append('w,o,c format')
	for v in range(len(auto.varstates)):
		headings.append(auto.varstates[v])
	for v in range(len(auto.varstates)):
		headings.append(auto.varstates[v]+'str')

	tab.header(headings)
	for i in range(len(listofoutputs)):
		temp = [i]
		if showstring == 1:
			temp.append(key2[i])
		if showconfig == 1:
			temp.append(key1[i])
		#temp = [i,key2[i],key1[i]]
		for v in range(len(auto.varstates)):
			temp.append(key3[i][auto.varstates[v]])
		for v in range(len(auto.varstates)):
			start = int(key3[i][auto.varstates[v]][0])-1
			end = int(key3[i][auto.varstates[v]][1])-1
			#print('s',start,'e',end)
			temp2 = string[start:end]
			temp.append([temp2])
		tab.add_row(temp)
	
	s = tab.draw()
	print(s)


"""
Subfunction for enumeration. minString takes a integer and find the minimum variable configuration available from all possible edges
Minimum ascending waiting, open then close
All other inputs beside integer are used for its data, Output: list of list contain variable configurations
"""
def minString(integer,stacks,finalgraph,totallength,finallist,availableletters,letterofedges,template):
	finalstring = []
	for i in range(integer, totallength-1):
		#Iterate available nodes from position i, obtain from stacks
		for availablenode in stacks[i]:
			if str(availablenode) in finalgraph[i]:
				#Iterate edges from available node
				for item in finalgraph[i][availablenode]:
					#If the variable configuration of the node is not in the list of availableletters
					#Reminder: availableletters is like stacks but with a list of possible varconfig patterns
					if not finallist[item] in availableletters[i+1]:
						availableletters[i+1].append( finallist[item] )
					#Reminder, letterofedges trace the varconfig to endnode, to get all possible end node for varconfig
					#Used to get set of nodes for stacks when an varconfig is chosen
					if str(finallist[item]) not in letterofedges[i+1]:
						letterofedges[i+1][str(finallist[item])] = set([])	
					letterofedges[i+1][str(finallist[item])].add(item)
		
		#Sort varconfig and pick the first one as minimum
		for j in range(len(availableletters[i+1][0])-1,-1,-1):
			availableletters[i+1].sort(key=lambda tup: tup[j], reverse=1)

		finalstring.append(availableletters[i+1][0])
		
		#Get list of end node from letterofedges and store it for the next stack
		stacks[i+1] = stacks[i+1] | letterofedges[i+1][str(availableletters[i+1][0])]	
		
		#del availableletters[i][0]	

	#Last value is always going to be closed
	if template == ['0']:
		#Initalise the template for last value
		copying = copy.deepcopy(availableletters[integer+1][0])

		for k in range(len(copying)):
			copying[k] = 'c'

		finalstring.append(copying)	

		return copying, finalstring

	else:
		finalstring.append(template)	

		return finalstring

"""
Subfunction for enumeration. nextString take the outputstring and search alterative paths by iteration from right to left.
Outputstring is in the list of list format.
Only true input is currentstring, all others are used for its data.
Output a new list of list different from currentstring or empty list.
"""
def nextString(currentstring,stacks,finalgraph,totallength,finallist,availableletters,letterofedges,template):
	for i in range(totallength-1,-1,-1):
		#If there are at least 2 availableletter
		if len(availableletters[i]) != 1:
			#Remove the list in currentstring[i] from availableletters
			availableletters[i].remove( currentstring[i] )
			#Replace the list with one from availableletters
			finalstring = currentstring[0:i]
			finalstring.append(availableletters[i][0])
			#Get new stack (new end nodes from the chosen list of availableletters)
			stacks[i] = letterofedges[i][str(availableletters[i][0])]
			#Find the rest of the varconfig (lists) using minString
			lastpart = minString(i,stacks,finalgraph,totallength,finallist,availableletters,letterofedges,template)
			finalstring.extend(lastpart)
			#Obtained a new output
			return finalstring

		else:
			#Current position does not have anymore alterative paths to terminal
			stacks[i] = set([])
			letterofedges[i] = {}
			availableletters[i] = []

	return []

"""
This is the enumeration function for obtain a list of outputs from the Ag graph.
Input: finalgraph, totallength of text, variable configuration of all nodes.
Output: list of list containing the variable configuration for each position of the text.
"""
def calcresults(finalgraph,totallength,finallist):
	stacks = {}
	availableletters = {}
	letterofedges = {}
	stacks[-1] = {'0'}

	#Initializtion
	for i in range(0,totallength+1):
		stacks[i] = set([])
		availableletters[i] = []
		letterofedges[i] = {}		

	template, k = minString(-1,stacks,finalgraph,totallength,finallist,availableletters,letterofedges,['0'])
	listofoutputs = []
	while k != []:
		listofoutputs.append(k)
		k = nextString(k,stacks,finalgraph,totallength,finallist,availableletters,letterofedges,template)
	
	return listofoutputs
