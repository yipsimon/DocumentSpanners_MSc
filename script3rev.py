import script2rev as sc2
import scriptgrph as sg
import script1rev as sc1
import threading, time, sys, copy, objgraph, random, inspect, re

"""
This function is projection from the algebraic operation of spanners. 
The function takes an automata object and transform the automata that only contain the desire variable statees.
Input: Automata object, list of variable states for projections and an indicator determine 
	whether the automata object had gone through the csymtonullong() function.
Output: A new automata object only contains the desired projections
"""
def projection(automata,listofprojections,before=0):
	#Initialise a new automata object
	auto = sc2.automata(0,0,0)
	auto.reset()
	auto = copy.deepcopy(automata)
	#If performed before csymtonulllong() function see sc1,
	#Then, there exists edges containing the open variable states and closing variable states
	if before == 1:
		ext = ['+','-']
		for key, edges in auto.transition.items():
			for edge in edges:
				if edge[1][-1] in ext:
					#Remove and Replace unneeded variable states values in the automata
					if not edge[1][0] in listofprojections:
						auto.transition[key].remove(edge)
						newedge = (edge[0],'[epsi]')
						auto.transition[key].append(newedge)

	auto.varstates = listofprojections
	newkey = {}		#New key for new varstates
	templist = []	#List of positions from old key for new varstates
					#Used to get varconfigs from old automata data in correct position and replace
	for i in range(len(listofprojections)):
		newkey[str(listofprojections[i])] = i
	
	for state in list(auto.key):
		if state in listofprojections:
			templist.append( auto.key[state] )
	#Replace current varconfig from nodes with only new varstates
	for key, var in auto.varconfig.items():
		tempvar = []	#Store new varconfig for node(key)
		#Get desire varconfig of new varstates using positions in templist
		for pos in templist:
			tempvar.append(var[pos])
		auto.varconfig[key] = copy.deepcopy(tempvar)

	auto.key = newkey

	return auto

def isnotlv5(table,key):
	if not key in table:
		table[key] = []

"""
This is a subfunction in the Join function to initialise the automata object as the result of the join operation.
Input: Automata Object 1, Automata Object 2
Output: The initialised join Automata Object (without varconfig, transition, states), Tempkey which stores the position of the variable states in the variable configuration for each node.
"""
def joincreate(auto1,auto2):
	#Initialise the Join automata object
	auto = sc2.automata(0,0,0)
	auto.reset()
	#The start node of the join will be the two starting nodes of the automata, stored in a tuple.
	auto.start = (str(auto1.start),str(auto2.start))
	#Similarly for terminal node
	auto.end = (str(auto1.end),str(auto2.end))
	#Combine both automata variable states together, without overlap
	auto.varstates.extend(auto1.varstates)
	for x in auto2.varstates:
		if x not in auto.varstates:
			auto.varstates.append(x)
	
	#Store the position of existing variable states of both automata
	keytemp = {} #Format: { 'x': (0,1), 'y': (1,0)} if Auto1.key = {'x':0,'y':1}, Auto2.key = {'y':0,'x':1}
	#This is used to get the variable configuration for specified state from both automata quickly.
	for variable in auto.varstates:
		#If a variable state does not exist in one of the automata, we represent this using -1.
		if variable not in auto1.key:
			num1 = -1
		else:
			num1 = auto1.key[variable]

		if variable not in auto2.key:
			num2 = -1
		else:
			num2 = auto2.key[variable]

		keytemp[variable] = (num1,num2)

	return auto, keytemp

"""
A subfunction in the Join function. 
This function checks for [epsi] values for all edges in the automata and pass it through to another subfunction.
This function add new empty edges to the automata object when more than one empty edges are connected between the nodes.
If empty edges are connected one after the other, then we need to consider that varconfig changes can change without strictly going through the same order.
For example, if 1->2->3 are empty edges and '2' has varconfig [o,w], '3' has [o,o], 'x','y' resp.
Both states will be open in '3' but to reach '3', '2' has to be open 'x' first. 
However, since '1','2','3' are connected by empty edges, 
the order of opening for the state should not matter at all since 1->2->3 connected by empty edges is the same as having 1->3 directly a empty edge. 
The main point is that node '1', can reach '3' either way. 
However, without the direct edge from 1->3, the automata will specified to opening 'x' first.
Adding a new empty edge from '1' to '3' will consider both state opened at the same time. 
"""
def addepsilon(auto):
	for startnode, tuples in auto.transition.items():
		for tup in tuples:
			#If find an [epsi] value, we pass the start node and the end node of the edge to the subfunction.
			if tup[1] == '[epsi]':
				checkfunction(auto,startnode,tup[0])
"""
A subfunction of the addepsilon function, part of the Join function.
This function checks for [epsi] values on edges (that does not end in start node) from the 'search' node, 
and add new [epsi] edges to the start node, skipping the 'search' node all together.
i.e. 0 -> 1 -> 2, new edge 0 -> 2, without passing 1.
"""
def checkfunction(auto,start,search):
	for tup in auto.transition[search]:
		#Find [epsi] that does not have destination in start node
		if tup[1] == '[epsi]' and tup[0] != start:
			#Only add the epsi edge if it does not exist in the start node.
			if (tup[0],'[epsi]') not in auto.transition[str(start)]:
				auto.transition[str(start)].append( (tup[0],'[epsi]') )
			#Continue searching for possible paths
			checkfunction(auto,start,tup[0])

"""
A subfunction from the Join function. 
This funciton checks whether the propose combined destination of the nodes are valid for the join automata.
Input: Start and Destination node, all other are just for information purposes
Output: Added new edges to the start node and updated the varconfig for destination node, updated the todo set.
"""
def checklegal(auto,keytemp,auto1,auto2,seen,dest,currentnode,endvalue,todo,done):
	fail = 0
	#Destination node : (endpoint1, endpoint2), corresp to auto1 and auto2
	#Check varconfig of destinations in auto1 and auto2.
	for variable in auto.varstates:
		#When a variable state exist in one automata but not in the other, the destination nodes are valid, as there are no conflicts.
		if keytemp[variable][0] == -1 or keytemp[variable][1] == -1:
			fail = 0
		#if the varconfig of the same variable state is different, the destination is not valid
		elif auto1.varconfig[str(dest[0])][keytemp[variable][0]] != auto2.varconfig[str(dest[1])][keytemp[variable][1]]:
			fail = 1
			break

	#When the dest node pass the varconfig check and it is not processed for the currentnode (not in seen set)
	if fail == 0 and (not seen & {dest}):
		seen.add(dest)
		#Initalise
		auto.varconfig[str(dest)] = copy.deepcopy(auto.varconfig[str(auto.start)])
		isnotlv5(auto.transition,str(currentnode))
		#Add the varconfig for each variable state for the destination node
		for variable in auto.varstates:
			tup = keytemp[variable]	#Get positions of varstate for auto1.varconfig and auto2.varconfig
			if tup[0] != -1 and tup[1] == -1:	#Varstate does not exist in auto2, use auto1 varconfig
				auto.varconfig[str(dest)][auto.key[variable]] = auto1.varconfig[str(dest[0])][tup[0]]
				#Auto.varconfig for join of dest node = list, auto.key[variable] get position of the varstate in the list
				#Store the varconfig of the varstate using auto1 and the position of varstate of auto1 in keytemp
			elif tup[1] != -1 and tup[0] == -1:	#Varstate does not exist in auto1, use auto2 varconfig
				auto.varconfig[str(dest)][auto.key[variable]] = auto2.varconfig[str(dest[1])][tup[1]]
			else:
				auto.varconfig[str(dest)][auto.key[variable]] = auto1.varconfig[str(dest[0])][tup[0]]
		
		#Add new edge
		end = (str(dest), endvalue)
		auto.transition[str(currentnode)].append(end)
		isnotlv5(auto.transition,str(dest))
		#If the dest node has not been processed before, add node to todo set.
		if not done & {dest}:
			todo.add(dest)
			
"""
This is the join operation of the core spanner. 
Input: Automata object 1, Automata object 2
Output: Join Automata Object
"""
def joinver1(auto1,auto2):
	#Add extra empty edges to both automata, allow multiple opening and closing states in one transition where its valid.
	addepsilon(auto1)
	addepsilon(auto2)
	
	#Initialise the join automata object with basic information
	auto, keytemp = joincreate(auto1,auto2)
	
	#Template for the default varconfig for the varstates, and key for allocating position of varconfig (list) for each varstate.
	#{x:0, y:1, z:2}, varconfig for '4' = [w,o,c], show x = waiting, y = opened, z = closed.
	template = list()
	for i in range(len(auto.varstates)):
		auto.key[str(auto.varstates[i])] = i
		template.append('w')
	
	isnotlv5(auto.transition,str(auto.end))
	todo = set([auto.start])	#Set of nodes to be processed
	done = set([])	#Set of nodes to had been processed, to prevent reprocessing
	auto.varconfig[str(auto.start)] = template	
	#Processing all nodes in todo, to find new destination and add edges to nodes
	while todo:
		currentnode = todo.pop()
		auto.states.append(str(currentnode))
		done.add(currentnode)	
		seen = set([])	#Reset seen, this set is used to prevent repeat edges to dest that has been seen with currentnode
		"""
		Format of Current node: (node1, node2), from auto1, auto2 resp
		Format of destination node: ( pathsfromnode1, pathsfromnode2 )
		Destination node generated in three format, (hold,change), (change,hold), (change,change). Change = existing dest reached from node
		When one node is holded, only empty edges are valid as new dest from node
		"""
		for edge1 in auto1.transition[currentnode[0]]:	
			for edge2 in auto2.transition[currentnode[1]]:
				#Get all destination node where both node has changed, if value of edges matches, it could be a valid destination
				if edge1[1] == edge2[1]:
					dest = (edge1[0],edge2[0])
					#Value are essentially regex expression, we need to make sure that matching individual symbols are properly expressed as regex
					val = edge1[1]
					if len(edge1[1]) == 1:	
						if re.match('\W',edge1[1]):		#Check if edge value is a symbol, non-unicode char
							 val = "\\"+str(edge1[1])	#Add double \ to regex expression to match symbol

					checklegal(auto,keytemp,auto1,auto2,seen,dest,currentnode,val,todo,done)
				else:
					#When the values are not equals and not empty, then they are both advanced regex expression, not just a specific letter or number
					if edge1[1] != '[epsi]' and edge2[1] != '[epsi]':
						dest = (edge1[0],edge2[0])
						val1 = str(edge1[1])
						val2 = str(edge2[1])
						if len(edge1[1]) == 1:
							if re.match('\W',edge1[1]):
								val1 = "\\"+str(edge1[1])
							
						if len(edge2[1]) == 1:
							if re.match('\W',edge2[1]):
								val2 = "\\"+str(edge2[1])

						#The (?= )(?= ) is used to join two regex expressions
						#We check whether one exists on either edges and only wrapping (?= ) to edges without them
						if edge1[1][0:3] == "(?=" and edge2[1][0:3] != "(?=":
							value = edge1[1]+'(?='+val2+')'
						elif edge1[1][0:3] != "(?=" and edge2[1][0:3] == "(?=":
							value = '(?='+val1+')'+edge2[1]
						elif edge1[1][0:3] == "(?=" and edge2[1][0:3] == "(?=":
							value = edge1[1]+edge2[1]
						else:
							value = '(?='+val1+')(?='+val2+')'
						
						checklegal(auto,keytemp,auto1,auto2,seen,dest,currentnode,value,todo,done)
			#All destination node where only changing node1 and keeping node2 the same
			if edge1[1] == '[epsi]':	
				dest = (edge1[0],currentnode[1])
				checklegal(auto,keytemp,auto1,auto2,seen,dest,currentnode,edge1[1],todo,done)

		for edge3 in auto2.transition[currentnode[1]]:
			#All destination node where only changing node2 and keeping node1 the same
			if edge3[1] == '[epsi]':
				dest = (currentnode[0],edge3[0])
				checklegal(auto,keytemp,auto1,auto2,seen,dest,currentnode,edge3[1],todo,done)

	return auto

"""
A subfunction in the combinationauto. This function create an automata object from the item value.
The item value is a tuple obtained from the stringequality function when it satisfied with the conditions.
tuple format = (length of matched string, start position of varstate1 from string, start position of varstate2 from string)
"""
def createauto(item,string,varstates,inode):
	auto = sc2.automata(0,0,0)
	auto.reset()
	auto.varstates.extend(varstates)
	auto.start = inode
	node = inode
	maxmum = item[0]+item[1]
	if (item[0]+item[2]) > maxmum:
		maxmum = item[0]+item[2]
	breaking = 0
	for i in range(len(varstates)):
		auto.key[str(varstates[i])] = i
	auto.varconfig[str(inode)] = ['w','w']
	#[c,w] or [w,c]
	if item[1] <= item[2]:
		start = item[1]
	else:
		start = item[2]
	norepeat1 = 0
	norepeat2 = 0
	for i in range(1,len(string)+2):
		if i == item[1]:
			auto.transition[str(node)] = [(str(node+1),varstates[0]+'+')]
			auto.varconfig[str(node+1)] = copy.deepcopy(auto.varconfig[str(node)])
			auto.varconfig[str(node+1)][0] = 'o'
			node += 1
		if i == item[2]:
			auto.transition[str(node)] = [(str(node+1),varstates[1]+'+')]
			auto.varconfig[str(node+1)] = copy.deepcopy(auto.varconfig[str(node)])
			auto.varconfig[str(node+1)][1] = 'o'
			node += 1
		if i == (item[0]+item[1]):
			auto.transition[str(node)] = [(str(node+1),varstates[0]+'-')]
			auto.varconfig[str(node+1)] = copy.deepcopy(auto.varconfig[str(node)])
			auto.varconfig[str(node+1)][0] = 'c'
			node += 1
		if i == (item[0]+item[2]):
			auto.transition[str(node)] = [(str(node+1),varstates[1]+'-')]
			auto.varconfig[str(node+1)] = copy.deepcopy(auto.varconfig[str(node)])
			auto.varconfig[str(node+1)][1] = 'c'
			node += 1
		if i == maxmum and i < (len(string)+1):
			auto.transition[str(node)] = [(str(node),'(.)'),(str(node+1),'(.)')]
			auto.transition[str(node+1)] = []
			auto.varconfig[str(node+1)] = copy.deepcopy(auto.varconfig[str(node)])
			breaking = 1
			break
		elif i == len(string)+1:
			auto.transition[str(node)] = []
			#auto.varconfig[str(node)] = copy.deepcopy(auto.varconfig[str(node-1)])
		else:
			ext2 = ['\n','\r','\t']
			ext3 = [['w','c'],['c','w']]
			if not string[i-1] in ext2:
				#print(i,node,auto.varconfig[str(node)])
				#if auto.varconfig[str(node)] in ext3 and (item[2]-(item[0]+item[1]) > 1 or item[1]-(item[0]+item[2]) > 1):
				#	if norepeat2 == 0:
				#		auto.transition[str(node)] = [(str(node),'(.)'),(str(node+1),'(.)')]
				#		auto.varconfig[str(node+1)] = copy.deepcopy(auto.varconfig[str(node)])
				#		node += 1
				#		norepeat2 = 1
				#elif auto.varconfig[str(node)] == ['w','w'] and node > inode and (start > 2):
				#	if norepeat1 == 0:
				#		auto.transition[str(node)] = [(str(node),'(.)'),(str(node+1),'(.)')]
				#		auto.varconfig[str(node+1)] = copy.deepcopy(auto.varconfig[str(node)])
				#		node += 1
				#		norepeat1 = 1
				#else:

				auto.transition[str(node)] = [(str(node+1),string[i-1])]
				auto.varconfig[str(node+1)] = copy.deepcopy(auto.varconfig[str(node)])
				node += 1

	if breaking == 1:
		auto.end = node+1
		auto.last = node+1
	else:
		auto.end = node
		auto.last = node

	#temp = auto.transition[str(inode)]
	#auto.transition[str(inode)] = [temp]

	return auto, node, breaking
 
def combinationauto(mainauto,maindest,mainshortcut,item,string,varstates):
	auto, dest, shortcut = createauto(item,string,varstates,mainauto.last)

	if shortcut == 1 and mainshortcut == 1:
		lastedge = auto.transition[str(dest-1)][0]
		auto.transition[str(dest-1)] = [(str(maindest),lastedge[1])]
		auto.end = dest-1
		mainauto.transition[str(mainauto.start)].extend(auto.transition[str(auto.start)])
		for key in range(mainauto.last+1,auto.end+1):
			mainauto.transition[str(key)] = auto.transition[str(key)]
			mainauto.varconfig[str(key)] = auto.varconfig[str(key)]
			
	else:
		if shortcut == 1 and mainshortcut == 0:
			mainshortcut = 1
			maindest = dest
			auto.transition[str(auto.end-1)] = [(str(dest),'(.)'),(str(mainauto.end),'(.)')]
		else:
			lastedge = auto.transition[str(auto.end-1)][0]
			auto.transition[str(auto.end-1)] = [(str(mainauto.end),lastedge[1])]

		auto.end = auto.end-1
		mainauto.transition[str(mainauto.start)].extend(auto.transition[str(auto.start)])
		for key in range(mainauto.last+1,auto.end+1):
			mainauto.transition[str(key)] = auto.transition[str(key)]
			mainauto.varconfig[str(key)] = auto.varconfig[str(key)]

	mainauto.last = auto.end

	return mainauto, maindest, mainshortcut


def apply_conditions(s,i,j,conditions):
	temp = True
	for cond in conditions:
		temp = temp and bool(cond(s,i,j))
	#print(temp,s[j-1:j+i-1])
	return temp

def stringequality(string,mode,start=1,end=-1,condits=-1):
	#listoftup = []
	count = 0
	if end == -1:
		end = len(string)+2
	stor = []
	if mode == 2:
		string = string.replace('\n','')
		mode = 0
	if mode == 0:
		for i in range(start,end):
			for j in range(1,len(string)+2-i):
				for k in range(1,len(string)+2-i):
					if string[j-1:j+i-1] == string[k-1:k+i-1]:
						if count == 0:
							autostring, deststring, shortcut = createauto((i,j,k),string,['x','y'],0)	
						else:
							autostring,deststring,shortcut = combinationauto(autostring,deststring,shortcut,(i,j,k),string,['x','y'])
						count += 1
						stor.append( (j,string[j-1:j+i-1],k,string[k-1:k+i-1]) )
	if mode == 1:
		for i in range(start,end):
			for j in range(1,len(string)+2-i):
				skip = 0
				for k in range(1,len(string)+2-i):
					if skip == 0:
						if string[k+i-2] == '\n':
							skip = 1
						elif string[j-1:j+i-1] == string[k-1:k+i-1]:
							if condits != -1:
								othercond = apply_conditions(string,i,j,condits)
							else:
								othercond = True
						
							if othercond:
								if count == 0:
									autostring, deststring, shortcut = createauto((i,j,k),string,['x','y'],0)	
								else:
									autostring,deststring,shortcut = combinationauto(autostring,deststring,shortcut,(i,j,k),string,['x','y'])
								count += 1
								stor.append( (j,string[j-1:j+i-1],k,string[k-1:k+i-1]) )
					if skip == 1:
						if string[k-1] == '\n':
							skip = 0
		string = string.replace('\n','')

	print('count:',count)
	'''
	for item in stor:
		print (repr(item))
	'''
	print('autolast',autostring.last)
	
	autostring.start = str(autostring.start)
	autostring.end = str(autostring.end)
	autostring.states = []
	for i in range(autostring.last+1):
		autostring.states.append(str(i))

	temp = {}
	for key, items in autostring.transition.items():
		temp[str(key)] = []
		for item in items:
			nitem = (str(item[0]),str(item[1]))
			temp[str(key)].append(nitem)

	autostring.transition = temp
	
	'''
	for key, items in autostring.transition.items():
		if not isinstance(items, list):
			autostring.transition[key] = [items]
	'''
	#autostring.tostr() #Long

	return string, autostring

def union(auto1,auto2):
		auto1.toint()
		auto2.toint()
		
		auto1.renumber(int(1))
		auto2.renumber(int(auto1.end+1))
		auto1.last = auto2.end+1

		auto1.addedge(auto1.end,auto1.last,'[epsi]')
		auto1.addedge(auto2.end,auto1.last,'[epsi]')
		auto1.addedge(0,1,'[epsi]')
		auto1.addedge(0,auto2.start,'[epsi]')
		auto1.varconfig[0] = ['w','w']
		auto1.varconfig[auto1.last] = ['c','c']
		auto1.states = []
		
		for item in auto2.varstates:
			if item not in auto1.varstates:
				auto1.varstates.append(item)
		
		for key, item in auto2.transition.items():
			if not key in auto1.transition:
				auto1.transition[key] = []
			auto1.transition[key].extend(item)
			auto1.varconfig[key] = auto2.varconfig[key]
		temp = {}
		for i in range(auto1.last+1):
			auto1.states.append(str(i))
			temp[str(i)] = auto1.varconfig[i]
		auto1.varconfig = temp
		
		auto1.tostr()
		#auto1.printauto()

def concat(auto1,auto2):
	auto1.toint()
	auto2.toint()
	auto2.renumber(int(auto1.last+1))
	auto1.addedge(auto1.end,auto1.last+1,'[epsi]')
	for key, item in auto2.transition.items():
		if not key in auto1.transition:
			auto1.transition[key] = []
		auto1.transition[key].extend(item)
		auto1.varconfig[key] = auto2.varconfig[key]
	
	auto1.end = auto2.end
	auto1.last = auto2.last
	auto1.states = []
	temp = {}
	for i in range(auto1.last+1):
		auto1.states.append(str(i))
		temp[str(i)] = auto1.varconfig[i]
	
	auto1.varconfig = temp
	auto1.tostr()
	#sc1.funchk(auto1)
	#auto1.printauto()


def alpha(listings,varstate):
	auto = sc2.automata(0,0,0)
	auto.reset()
	auto.start = 0
	auto.varstates = [str(varstate)]
	auto.transition[str(0)] = [(str(0),'(.)'),(str(1),'x+')]
	auto.transition[str(1)] = []
	auto.last = 1
	for k in range(len(listings)):
		for i in range(len(listings[k])):
			if i == 0: 
				auto.last += 1
				auto.transition[str(1)].append((str(auto.last),listings[k][i]))
			elif i == len(listings[k])-1 and k != 0:
				auto.transition[str(auto.last)] = [(str(converging),listings[k][i])]
			else:
				auto.transition[str(auto.last)] = [(str(auto.last+1),listings[k][i])]
				auto.last += 1

		if k == 0:
			converging = auto.last
			auto.last += 1
			auto.end = auto.last
			auto.last += 1
			auto.transition[str(converging)] = [(str(auto.end),'x-')]

	auto.transition[str(auto.end)] = [(str(auto.end),'(.)')]
	for i in range(auto.last+1):
		auto.states.append(str(i))

	return auto


def main():
	start_time = time.time()
	string1 = 'a'*3
	auto1 = stringequality(string1)
	print("--- %s seconds ---" % (time.time() - start_time))
	objgraph.show_most_common_types()	

if __name__ == "__main__":
	main()

