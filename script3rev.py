import script2rev as sc2
import scriptgrph as sg
import script1rev as sc1
import threading, time, sys, copy, objgraph, random, inspect, re


def projection(automata,listofprojections,before=0):
	auto = sc2.automata(0,0,0)
	auto.reset()
	auto = copy.deepcopy(automata)
	#If performed before csymtonulllong() function see sc1
	if before == 1:
		ext = ['+','-']
		for key, edges in auto.transition.items():
			for edge in edges:
				if edge[1][-1] in ext:
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

def isnotlv6(table,key):
	if not key in table:
		table[key] = set([])

def joincreate(auto1,auto2):
	auto = sc2.automata(0,0,0)
	auto.reset()
	auto.start = (str(auto1.start),str(auto2.start))
	auto.end = (str(auto1.end),str(auto2.end))
	auto.varstates.extend(auto1.varstates)
	for item in auto1.varstates:
		if not item in auto.varstates:
			auto.varstates.append(item)

	for x in auto2.varstates:
		if x not in auto.varstates:
			auto.varstates.append(x)
	keytemp = {}
	for variable in auto.varstates:
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


def addepsilon(auto):
	for startnode, tuples in auto.transition.items():
		for tup in tuples:
			if tup[1] == '[epsi]':
				checkfunction(auto,startnode,tup[0])

def checkfunction(auto,start,search):
	for tup in auto.transition[search]:
		if tup[1] == '[epsi]' and tup[0] != start:
			if (tup[0],'[epsi]') not in auto.transition[str(start)]:
				auto.transition[str(start)].append( (tup[0],'[epsi]') )
			checkfunction(auto,start,tup[0])

def checklegal(auto,keytemp,auto1,auto2,seen,dest,template,currentnode,finallist,endvalue,todo,done,key3):
	fail = 0
	for variable in auto.varstates:
		if keytemp[variable][0] == -1 or keytemp[variable][1] == -1:
			fail = 0
		elif auto1.varconfig[str(dest[0])][keytemp[variable][0]] != auto2.varconfig[str(dest[1])][keytemp[variable][1]]:
			fail = 1
			break

	if fail == 0 and (not seen & {dest}):
		seen.add(dest)
		finallist[str(dest)] = []
		finallist[str(dest)].extend(template)
		isnotlv5(auto.transition,str(currentnode))
		for variable in auto.varstates:
			tup = keytemp[variable]
			if tup[0] != -1 and tup[1] == -1:
				finallist[str(dest)][key3[variable]] = auto1.varconfig[str(dest[0])][tup[0]]
			elif tup[1] != -1 and tup[0] == -1:
				finallist[str(dest)][key3[variable]] = auto2.varconfig[str(dest[1])][tup[1]]
			else:
				finallist[str(dest)][key3[variable]] = auto1.varconfig[str(dest[0])][tup[0]]
	
		end = (str(dest), endvalue)
		auto.transition[str(currentnode)].append(end)
		isnotlv5(auto.transition,str(dest))
		if not done & {dest}:
			todo.add(dest)
			

def joinver1(auto1,auto2):

	addepsilon(auto1)
	addepsilon(auto2)
	
	auto, keytemp = joincreate(auto1,auto2)
	
	key3 = {}
	template = list()
	for i in range(len(auto.varstates)):
		key3[str(auto.varstates[i])] = i
		template.append('w')

	isnotlv5(auto.transition,str((auto1.end,auto2.end)))
	todo = set([(str(auto1.start),str(auto2.start))])
	done = set([])
	finallist = {str((str(auto1.start),str(auto2.start))): template}
	while todo:
		currentnode = todo.pop()
		auto.states.append(str(currentnode))
		done.add(currentnode)
		seen = set([])

		for edge1 in auto1.transition[str(currentnode[0])]:
			for edge2 in auto2.transition[str(currentnode[1])]:
				if edge1[1] == edge2[1]:
					dest = (edge1[0],edge2[0])
					if len(edge1[1]) == 1:
						matchs = re.match('\W',edge1[1])
						if matchs:
							 val = "\\"+str(edge1[1])
						else:
							val = edge1[1]	
					else:
						val = edge1[1]
					checklegal(auto,keytemp,auto1,auto2,seen,dest,template,currentnode,finallist,val,todo,done,key3)
				else:
					if edge1[1] != '[epsi]' and edge2[1] != '[epsi]':
						dest = (edge1[0],edge2[0])
						if edge1[1][0:3] == "(?=" and edge2[1][0:3] != "(?=":
							if len(edge2[1]) == 1:
								matchs2 = re.match('\W',edge2[1])
								if matchs2:
									val2 = "\\"+str(edge2[1])
								else:
									val2 = str(edge2[1])
							else:
								val2 = str(edge2[1])
							value = edge1[1]+'(?='+val2+')'
						elif edge1[1][0:3] != "(?=" and edge2[1][0:3] == "(?=":
							if len(edge1[1]) == 1:
								matchs1 = re.match('\W',edge1[1])
								if matchs1:
									val1 = "\\"+str(edge1[1])
								else:
									val2 = str(edge2[1])
							else:
								val1 = str(edge1[1])
							value = '(?='+val1+')'+edge2[1]
						elif edge1[1][0:3] == "(?=" and edge2[1][0:3] == "(?=":
							value = edge1[1]+edge2[1]
						else:
							if len(edge1[1]) == 1:
								matchs1 = re.match('\W',edge1[1])
								if matchs1:
									val1 = "\\"+str(edge1[1])
								else:
									val1 = str(edge1[1])
							else:
								val1 = str(edge1[1])
							
							if len(edge2[1]) == 1:
								matchs2 = re.match('\W',edge2[1])
								if matchs2:
									val2 = "\\"+str(edge2[1])
								else:
									val2 = str(edge2[1])
							else:
								val2 = str(edge2[1])
							value = '(?='+val1+')(?='+val2+')'
						
						checklegal(auto,keytemp,auto1,auto2,seen,dest,template,currentnode,finallist,value,todo,done,key3)

			if edge1[1] == '[epsi]':
				dest = (edge1[0],currentnode[1])
				checklegal(auto,keytemp,auto1,auto2,seen,dest,template,currentnode,finallist,edge1[1],todo,done,key3)

		for edge3 in auto2.transition[str(currentnode[1])]:
			if edge3[1] == '[epsi]':
				dest = (currentnode[0],edge3[0])
				checklegal(auto,keytemp,auto1,auto2,seen,dest,template,currentnode,finallist,edge3[1],todo,done,key3)

	auto.varconfig = finallist
	auto.key = key3
	return auto


def ifnotlv7(table,key):
	if not key in table:
		table[key] = []

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


	for i in range(1,len(string)+2):
		if i == item[1]:
			auto.transition[str(node)] = [(str(node+1),'x+')]
			node += 1
		if i == item[2]:
			auto.transition[str(node)] = [(str(node+1),'y+')]
			node += 1
		if i == (item[0]+item[1]):
			auto.transition[str(node)] = [(str(node+1),'x-')]
			node += 1
		if i == (item[0]+item[2]):
			auto.transition[str(node)] = [(str(node+1),'y-')]
			node += 1
		if i == maxmum and i < (len(string)+1):
			auto.transition[str(node)] = [(str(node),'(.)'),(str(node+1),'(.)')]
			auto.transition[str(node+1)] = []
			breaking = 1
			break
		elif i == len(string)+1:
			auto.transition[str(node)] = []
		else:
			ext2 = ['\n','\r','\t']
			if not string[i-1] in ext2:
				auto.transition[str(node)] = [(str(node+1),string[i-1])]
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

	mainauto.last = auto.end

	return mainauto, maindest, mainshortcut


def apply_conditions(s,i,j,conditions):
	for cond, replace in conditions:
		if cond(s,i,j):
			return replace
	return i

def stringequality(string,mode,start=1,end=-1,condits=-1):
	#listoftup = []
	count = 0
	if end == -1:
		end = len(string)+2
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
	if mode == 1:
		
		for i in range(start,end):
			for j in range(1,len(string)+2-i):
				skip = 1
				for k in range(j+1,len(string)+2-i):
					if skip == 0:
						if string[k+i-2:k+i-1] == '\n':
							skip = 1
						elif string[j-1:j+i-1] == string[k-1:k+i-1]:
							if condits != -1:
								othercond = apply_conditions(string,i,j,condits)
							else:
								othercond = 'true'
							
							if othercond == 'true':
							#if string[j-1:j] in ['0','1','2','3','4','5','6','7','8','9']:
								if count == 0:
									autostring, deststring, shortcut = createauto((i,j,k),string,['x','y'],0)	
								else:
									autostring,deststring,shortcut = combinationauto(autostring,deststring,shortcut,(i,j,k),string,['x','y'])
								count += 1
							#stor.append( (j,string[j-1:j+i-1],k,string[k-1:k+i-1]) )
					if skip == 1:
						if string[k-1:k] == '\n':
							skip = 0
		string = string.replace('\n','')

	print('count:',count)
	autostring.start = str(autostring.start)
	autostring.end = str(autostring.end)
	autostring.states = []
	for i in range(autostring.last+1):
		autostring.states.append(str(i))
	#autostring.printauto()
	print('totalnodes:',autostring.last)
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
		auto1.rename2()
		auto2.rename2()
		
		auto1.renumber(int(1))
		auto2.renumber(int(auto1.end+1))
		auto1.last = auto2.end+1
		sg.printgraph(auto1,'text0')
		sg.printgraph(auto2,'text1')
		auto1.addedge(auto1.end,auto1.last,'[epsi]')
		auto1.addedge(auto2.end,auto1.last,'[epsi]')
		auto1.addedge(0,1,'[epsi]')
		auto1.addedge(0,auto2.start,'[epsi]')
		auto1.states = set([])
		for i in range(auto1.last):
			auto1.states.add(str(i))

		for item in auto2.varstates:
			if item not in auto1.varstates:
				auto1.varstates.append(item)
		
		for key, item in auto2.transition.items():
			if not key in auto1.transition:
				auto1.transition[key] = []
			auto1.transition[key].extend(item)
		
		auto1.tostr()
		auto1.printauto()

def concat(auto1,auto2):
	auto1.rename2()
	auto2.rename2()
	auto2.renumber(int(auto1.last+1))
	auto1.addedge(auto1.end,auto1.last+1,'[epsi]')
	for key, item in auto2.transition.items():
		if not key in auto1.transition:
			auto1.transition[key] = []
		auto1.transition[key].extend(item)
	auto1.end = auto2.end
	auto1.last = auto2.last
	auto1.tostr()
	auto1.printauto()


def alpha(listings):
	auto = sc2.automata(0,0,0)
	auto.reset()
	auto.start = 0
	auto.varstates = ['x']
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
		auto.states.add(str(i))

	return auto


def main():
	start_time = time.time()
	string1 = 'a'*3
	auto1 = stringequality(string1)
	print("--- %s seconds ---" % (time.time() - start_time))
	objgraph.show_most_common_types()	

if __name__ == "__main__":
	main()

