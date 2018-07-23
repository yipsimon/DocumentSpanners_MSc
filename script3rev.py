import script2rev as sc2
import scriptgrph as sg
import script1rev as sc1
import threading, time, sys, copy

def convertregex(regex):
	auto = sc2.main(regex)
	
	sg.printgraph(auto,'g1')

	return auto

def functionalcheck(auto):
	finallist, key, varedges = sc1.funchk(auto)

	sc1.csymtonull(auto,varedges)

	return finallist, key

def normalprocess(auto,text):

	#text = input('Enter your string: ')

	finalgraph = sc1.generateAg(auto,text,finallist)

	finalprintable = final(finalgraph,finallist,auto.end)

	sg.printgraph(finalprintable,'g2')

	outputs = sc1.calcresults(finalgraph, len(text), finallist)

	return outputs

def printresults(outputs):
	
	sc1.printresults(outputs)

def projectionver1(auto,text,listofprojections):
	
	sc1.projectionv1(auto,listofprojections)
	
	outputs = normalprocess(auto,text)

	printresults(outputs)

def projectionver2(auto,text,listofprojections):

	text = input('Enter your string: ')

	finalgraph = sc1.generateAg(auto,text,finallist)

	finalprintable = final(finalgraph,finallist,auto.end)

	sg.printgraph(finalprintable,'g2')

	#not sure whether to project during the minstring, nextstring or after producing the (w,w),(w,o)... list then pick the projected values
	#Currently, we only pick the results afterward 

	outputs = sc1.calcresults(finalgraph, len(text), finallist)

	sc1.projectionv2(outputs)

def isnotlv5(table,key):
	if not key in table:
		table[key] = []

def isnotlv6(table,key):
	if not key in table:
		table[key] = set([])

def joincreate(auto1,auto2,key1,key2):
	auto = sc2.automata(0,0,0)
	auto.reset()
	auto.start = (auto1.start,auto2.start)
	auto.end = (auto1.end,auto2.end)
	auto.states = auto.states | {str(auto.start)} | {str(auto.end)}
	auto.varstates.extend(auto1.varstates)
	for x in auto2.varstates:
		if x not in auto.varstates:
			auto.varstates.append(x)
	keytemp = {}
	for variable in auto.varstates:
		if variable not in key1:
			num1 = -1
		else:
			num1 = key1[variable]

		if variable not in key2:
			num2 = -1
		else:
			num2 = key2[variable]

		keytemp[variable] = (num1,num2)

	return auto, keytemp

def joinver1(auto1,auto2):	
	finallist1, key1, varedges1 = sc1.funchk(auto1)
	finallist2, key2, varedges2 = sc1.funchk(auto2)

	sc1.csymtonull(auto1,varedges1)
	sc1.csymtonull(auto2,varedges2)

	auto, keytemp = joincreate(auto1,auto2,key1,key2)

	key3 = {}
	template = list()
	for i in len(auto.varstates):
		key3[str(auto.varstates[i])] = i
		template.append('w')

	
	todo = set([(auto1.start,auto2.start)])
	done = set([])
	finallist = {(auto1.start,auto2.start): template}
	while todo:
		currentnode = todo.pop()
		seen = set([])
		for edge1 in auto1.transition[currentnode[0]]:
			fail = 0
			for variable in auto.varstates:
				if keytemp[variable][0] == -1 or keytemp[variable][1] == -1:
					fail = 0
				elif finallist1[edge1[0]][keytemp[variable][0]] != finallist2[currentnode[1]][keytemp[variable][1]]:
					fail = 1
					break
			dest = (edge1[0],currentnode[1])
			if fail == 0 and (not seen & {dest}):
				isnotlv5(auto.transition,currentnode)
				isnotlv5(finallist,dest)
				for variable in auto.varstates:
					if keytemp[variable][0] != -1 and keytemp[variable][1] == -1:
						finallist[dest].append(finallist1[edge1[0]][keytemp[variable][0]])
					elif keytemp[variable][1] != -1 and keytemp[variable][0] == -1:
						finallist[dest].append(finallist2[currentnode[1]][keytemp[variable][1]])
					else:
						finallist[dest].append(finallist1[edge1[0]][keytemp[variable][0]])

				end = (dest, edge1[1])
				auto.transition[currentnode].append(end)
				if not done & {dest}:
					todo.add(dest)
					seen.add(dest)

		for edge2 in auto1.transition[currentnode[1]]:
			fail = 0
			for variable in auto.varstates:
				if keytemp[variable][0] == -1 or keytemp[variable][1] == -1:
					fail = 0
				elif finallist1[currentnode[0]][keytemp[variable][0]] != finallist2[edge2[0]][keytemp[variable][1]]:
					fail = 1
					break
			dest = (currentnode[0],edge2[0])
			if fail == 0 and (not seen & {dest}):
				isnotlv5(auto.transition,currentnode)
				isnotlv5(finallist,dest)
				for variable in auto.varstates:
					if keytemp[variable][0] != -1 and keytemp[variable][1] == -1:
						finallist[dest].append(finallist1[edge2[0]][keytemp[variable][0]])
					elif keytemp[variable][1] != -1 and keytemp[variable][0] == -1:
						finallist[dest].append(finallist2[currentnode[1]][keytemp[variable][1]])
					else:
						finallist[dest].append(finallist1[edge2[0]][keytemp[variable][0]])

				end = (dest, edge2[1])
				auto.transition[currentnode].append(end)
				if not done & {dest}:
					todo.add(dest)
					seen.add(dest)

		done.add(currentnode)

	return auto

#Not sure 
def joinver2(auto1,auto2):
	finallist1, key1 = functionalcheck(auto1)
	finallist2, key2 = functionalcheck(auto2)

	text = input('Enter your string: ')

	finalgraph1 = sc1.generateAg(auto1,text,finallist1)
	finalgraph2 = sc1.generateAg(auto2,text,finallist2)

	auto, keytemp = joincreate(auto1,auto2,key1,key2)
	key3 = {}
	template = list()
	for i in len(auto.varstates):
		key3[str(auto.varstates[i])] = i
		template.append('w')

	finalgraph = {}
	for i in range(len(text)):
		finalgraph[i] = {}

	#finalgraph[-1] = {auto.start: set([])}
	finallist = {}
	nodes = set([])
	done = set([])
	for i in range(-1,len(text)):
		nextnodes = set([])
		if i == -1:
			for edge1 in finalgraph1[i][auto1.start]:
				for edge2 in finalgraph2[i][auto2.start]:
					dest = (edge1,edge2)
					fail = 0
					for variable in auto.varstates:
						if keytemp[variable][0] == -1 or keytemp[variable][1] == -1:
							fail = 0
						elif finallist1[edge1[0]][keytemp[variable][0]] != finallist2[currentnode[1]][keytemp[variable][1]]:
							fail = 1
							break
					if fail == 0:
						isnotlv5(auto.transition,currentnode)
						isnotlv5(finallist,dest)
						for variable in auto.varstates:
							if keytemp[variable][0] != -1 and keytemp[variable][1] == -1:
								finallist[dest].append(finallist1[edge1[0]][keytemp[variable][0]])
							elif keytemp[variable][1] != -1 and keytemp[variable][0] == -1:
								finallist[dest].append(finallist2[currentnode[1]][keytemp[variable][1]])
							else:
								finallist[dest].append(finallist1[edge1[0]][keytemp[variable][0]])

						end = (dest, edge1[1])
						auto.transition[currentnode].append(end)
						if not done & {dest}:
							nextnodes.add(dest)

		else:
			while nodes:
				currentnode = nodes.pop()
				for edge1 in finalgraph1[i][currentnode[0]]:
					for edge2 in finalgraph2[i][currentnode[1]]:
						dest = (edge1,edge2)
						fail = 0
						for variable in auto.varstates:
							if keytemp[variable][0] == -1 or keytemp[variable][1] == -1:
								fail = 0
							elif finallist1[currentnode[0]][keytemp[variable][0]] != finallist2[edge2[0]][keytemp[variable][1]]:
								fail = 1
								break
						
						if fail == 0 and (not seen & {dest}):
							isnotlv5(auto.transition,currentnode)
							isnotlv5(finallist,dest)
							for variable in auto.varstates:
								if keytemp[variable][0] != -1 and keytemp[variable][1] == -1:
									finallist[dest].append(finallist1[edge2[0]][keytemp[variable][0]])
								elif keytemp[variable][1] != -1 and keytemp[variable][0] == -1:
									finallist[dest].append(finallist2[currentnode[1]][keytemp[variable][1]])
								else:
									finallist[dest].append(finallist1[edge2[0]][keytemp[variable][0]])

							end = (dest, edge2[1])
							auto.transition[currentnode].append(end)
							if not done & {dest}:
								nextnodes.add(dest)

				done.add(currentnode)

		nodes = nextnodes						
		
	return auto

def ifnotlv7(table,key):
	if not key in table:
		table[key] = []

def createauto(item,string,varstates):
	auto = sc2.automata(0,0,0)
	auto.reset()
	auto.varstates.extend(varstates)
	auto.states.add('0')
	node = 0
	maxmum = item[0]+item[1]
	if (item[0]+item[2]) > maxmum:
		maxmum = item[0]+item[2]

	for i in range(len(string)+1):
		if i+1 == item[1]:
			ifnotlv7(auto.transition,node)
			auto.transition[node].append((node+1,'x+'))
			auto.states.add(str(node+1))
			node += 1
		if i+1 == item[2]:
			ifnotlv7(auto.transition,node)
			auto.transition[node].append((node+1,'y+'))
			auto.states.add(str(node+1))
			node += 1
		if i+1 == (item[0]+item[1]):
			ifnotlv7(auto.transition,node)
			auto.transition[node].append((node+1,'x-'))
			auto.states.add(str(node+1))
			node += 1
		if i+1 == (item[0]+item[2]):
			ifnotlv7(auto.transition,node)
			auto.transition[node].append((node+1,'y-'))
			auto.states.add(str(node+1))
			node += 1
		if i+1 == maxmum and i+1 != (len(string)+1):
			ifnotlv7(auto.transition,node)
			auto.transition[node].append((node+1,'[sum]'))
			auto.states.add(str(node+1))
			break
		else:
			ifnotlv7(auto.transition,node)
			auto.transition[node].append((node+1,string[i]))
			auto.states.add(str(node+1))
			node += 1

	auto.end = node+1
	print(node)
	print(auto.transition)
	#auto.transition[node+1] = []

	return auto, node

def unionv2(mainauto,mainlastsum,auto,lastnum,mode):
	print(auto.transition)
	print('lastsum',lastsum)
	temp = auto.transition[lastsum-1][0]
	print(temp)
	lastconfigedge = temp[1]
	for i in range(lastsum,lastsum-1-mode,-1):
		del auto.transition[i]
	#auto.transition[lastnum-mode] = []
	auto.end = lastnum-mode+1
	print('auto.end',auto.end)
	time.sleep(5)
	auto.renumber(int(mainauto.end))
	for key, item in auto.transition.items():
		if not key in mainauto.transition:
			mainauto.transition[key] = []
		if key == auto.start:
			mainauto.transition[mainauto.start].extend(item)
		else:
			mainauto.transition[key].extend(item)

	print(mainauto.transition)
	mainauto.addedge(auto.end,mainlastsum,lastconfigedge)

	mainlastsum = lastsum

	return mainauto, mainlastsum



def combinationauto(mainauto,mainlastsum,item,string,varstates):
	auto, lastsum = createauto(item,string,varstates)
	print('lastsum',lastsum)
	if lastsum != len(string)+4 and mainlastsum != len(string)+4:
		toend = 1
	else:
		toend = 0

	if toend == 1:
		newauto, newlastsum = unionv2(mainauto,mainlastsum,auto,lastsum,1)
	elif toend == 0:
		newauto, newlastsum = unionv2(mainauto,mainlastsum,auto,lastsum,0)

	mainauto = newauto
	mainlastsum = newlastsum


def stringequality(auto,string):
	listofauto = []
	listoftup = []
	for i in range(len(string)+1):
		for j in range(1,len(string)+2-i):
			for k in range(1,len(string)+2-i):
				if string[j-1:j+i-1] == string[k-1:k+i-1]:
					listoftup.append((i,j,k))




auto1, lastsum = createauto((0,1,1),'abc',['x','y'])
combinationauto(auto1,lastsum,(0,1,2),'abc',['x','y'])
auto1.printauto()
sg.printgraph(auto1,'test')

	

