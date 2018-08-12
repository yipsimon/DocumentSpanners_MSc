import script2rev as sc2
import scriptgrph as sg
import script1rev as sc1
import threading, time, sys, copy, objgraph, random, inspect

'''
def convertregex(regex):
	auto = sc2.main(regex)
	auto.tostr()
	#sg.printgraph(auto,'g1')

	return auto

def functionalcheck(auto):
	finallist, key, varedges = sc1.funchk(auto)

	sc1.csymtonull(auto,varedges)

	#sg.printgraph(auto,'g1')

	return finallist, key

def normalprocess(auto,text,finallist):

	#text = input('Enter your string: ')

	finalgraph = sc1.generateAg(auto,text,finallist)

	finalprintable = sc1.finalauto(finalgraph,finallist,auto.end)

	sg.printgraph(finalprintable,'g2')


	outputs = sc1.calcresults(finalgraph, len(text), finallist)

	return outputs

def printresults(outputs):
	
	sc1.printresults(outputs)
'''
def projection(automata,string,listofprojections):
	auto = sc2.automata(0,0,0)
	auto.reset()
	auto = copy.deepcopy(automata)
	ext = ['+','-']
	for key, edges in auto.transition.items():
		for edge in edges:
			if edge[1][-1] in ext:
				if not edge[1][0] in listofprojections:
					auto.transition[key].remove(edge)
					newedge = (edge[0],'[epsi]')
					auto.transition[key].append(newedge)
	
	auto.varstates = listofprojections
	newkey = {}
	templist = []
	for i in range(len(listofprojections)):
		newkey[str(listofprojections[i])] = i
	for state in list(auto.key):
		if not state in listofprojections:
			del auto.key[state]
		else:
			templist.append( auto.key[state] )

	for key, var in auto.varconfig.items():
		tempvar = []
		for pos in templist:
			tempvar.append(var[pos])
		auto.varconfig[key] = copy.deepcopy(tempvar)

	auto.key = newkey
	#auto.printauto()

	return auto
	'''
	sc1.csymtonulllong(auto)
	finalgraph = sc1.generateAg(auto,string)
	outputs = sc1.calcresults(finalgraph, len(string), auto.varconfig)
	sc1.printresults(outputs)
	sc1.printresultsv2(outputs,auto)

	sys.exit(1)
	'''

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
	#auto.states = auto.states | {str(auto.start)} | {str(auto.end)}
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
		#isnotlv5(finallist,dest)
		print('keytemp',keytemp)
		for variable in auto.varstates:
			tup = keytemp[variable]
			print('tup',tup)
			print ('dest',dest)
			print('finallist',finallist)
			if tup[0] != -1 and tup[1] == -1:
				#finallist[str(dest)][0] = finallist1[str(dest[0])][tup[0]]
				finallist[str(dest)][key3[variable]] = auto1.varconfig[str(dest[0])][tup[0]]
			elif tup[1] != -1 and tup[0] == -1:
				#finallist[str(dest)][1] = finallist2[str(dest[1])][tup[1]]
				finallist[str(dest)][key3[variable]] = auto2.varconfig[str(dest[1])][tup[1]]
			else:
				finallist[str(dest)][key3[variable]] = auto1.varconfig[str(dest[0])][tup[0]]
				#finallist[str(dest)][0] = finallist1[str(dest[0])][tup[0]]
				#finallist[str(dest)][1] = finallist2[str(dest[1])][tup[1]]
		end = (str(dest), endvalue)
		auto.transition[str(currentnode)].append(end)
		isnotlv5(auto.transition,str(dest))
		if not done & {dest}:
			todo.add(dest)
			

def joinver1(auto1,auto2):
	'''	
	openlist1, closelist1 = sc1.funchk(auto1)
	openlist2, closelist2 = sc1.funchk(auto2)
	
	finallist1, key1 = sc1.getvarconfig(auto1,openlist1,closelist1)
	finallist2, key2 = sc1.getvarconfig(auto2,openlist2,closelist2)

	print('finallist1',finallist1)
	print('finallist2',finallist2)
	sc1.csymtonulllong(auto1)
	sc1.csymtonulllong(auto2)
	'''
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
		print('todo\n',todo)
		currentnode = todo.pop()
		auto.states.add(str(currentnode))
		done.add(currentnode)
		print('currentnode\n',currentnode)
		print('\n')
		seen = set([])
		for edge1 in auto1.transition[str(currentnode[0])]:
			for edge2 in auto2.transition[str(currentnode[1])]:
				if edge1[1] == edge2[1]:
					dest = (edge1[0],edge2[0])
					checklegal(auto,keytemp,auto1,auto2,seen,dest,template,currentnode,finallist,edge1[1],todo,done,key3)

			if edge1[1] == '[epsi]':
				dest = (edge1[0],currentnode[1])
				checklegal(auto,keytemp,auto1,auto2,seen,dest,template,currentnode,finallist,edge1[1],todo,done,key3)

		for edge3 in auto2.transition[str(currentnode[1])]:
			if edge3[1] == '[epsi]':
				dest = (currentnode[0],edge3[0])
				checklegal(auto,keytemp,auto1,auto2,seen,dest,template,currentnode,finallist,edge3[1],todo,done,key3)		
	'''
	tokeepnodes = set([str((auto1.end,auto2.end))])
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
		

	print('\nfinalgraph \n', finalgraph)
	'''
	auto.varconfig = finallist
	auto.key = key3
	auto.printauto()
	
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
	for i in range(-1,len(text)):
		finalgraph[i] = {}

	#finalgraph[-1] = {auto.start: set([])}
	finallist = {}
	nodes = set([])
	nextnodes = set([])
	for i in range(-1,len(text)):
		if i == -1:
			for edge1 in finalgraph1[i]['0']:
				for edge2 in finalgraph2[i]['0']:
					fail = 0
					for variable in auto.varstates:
						if keytemp[variable][0] == -1 or keytemp[variable][1] == -1:
							fail = 0
						elif finallist1[currentnode[0]][keytemp[variable][0]] != finallist2[edge2[0]][keytemp[variable][1]]:
							fail = 1
							break
					dest = (edge1,edge2)
					if fail == 0:
						finallist[str(dest)] = []
						finallist[str(dest)].extend(template)
						isnotlv5(auto.transition,str(currentnode))
						#isnotlv5(finallist,dest)
						for variable in auto.varstates:
							tup = keytemp[variable]
							if tup[0] != -1 and tup[1] == -1:
								finallist[str(dest)][0] = finallist1[str(dest[0])][tup[0]]
							elif tup[1] != -1 and tup[0] == -1:
								finallist[str(dest)][1] = finallist2[str(dest[1])][tup[1]]
							else:
								finallist[str(dest)][0] = finallist1[str(dest[0])][tup[0]]
								finallist[str(dest)][1] = finallist2[str(dest[1])][tup[1]]
					end = (str(dest), edge2[1])
					ed = str(dest)
					finalgraph[i]['0'].append(ed)
					nextnodes.add(dest)
			nodes = nodes | nextnodes
		else:
			while nodes:
				currentnode = nodes.pop()
				for edge1 in finalgraph1[i][currentnode[0]]:
					for edge2 in finalgraph2[i][currentnode[1]]:
						fail = 0
						for variable in auto.varstates:
							if keytemp[variable][0] == -1 or keytemp[variable][1] == -1:
								fail = 0
							elif finallist1[currentnode[0]][keytemp[variable][0]] != finallist2[edge2[0]][keytemp[variable][1]]:
								fail = 1
								break
						dest = (edge1,edge2)
						if fail == 0:
							finallist[str(dest)] = []
							finallist[str(dest)].extend(template)
							isnotlv5(auto.transition,str(currentnode))
							#isnotlv5(finallist,dest)
							for variable in auto.varstates:
								tup = keytemp[variable]
								if tup[0] != -1 and tup[1] == -1:
									finallist[str(dest)][0] = finallist1[str(dest[0])][tup[0]]
								elif tup[1] != -1 and tup[0] == -1:
									finallist[str(dest)][1] = finallist2[str(dest[1])][tup[1]]
								else:
									finallist[str(dest)][0] = finallist1[str(dest[0])][tup[0]]
									finallist[str(dest)][1] = finallist2[str(dest[1])][tup[1]]
						end = (str(dest), edge2[1])
						ed = str(dest)
						finalgraph[i][str(currentnode)].append(ed)
						nextnodes.add(dest)
			nodes = nodes | nextnodes
		
	return auto

def ifnotlv7(table,key):
	if not key in table:
		table[key] = set([])

def createauto(item,string,varstates):
	auto = sc2.automata(0,0,0)
	auto.reset()
	auto.varstates.extend(varstates)
	auto.states.add(0)
	node = 0
	maxmum = item[0]+item[1]
	if (item[0]+item[2]) > maxmum:
		maxmum = item[0]+item[2]
	breaking = 0
	for i in range(1,len(string)+2):
		if i == item[1]:
			ifnotlv7(auto.transition,node)
			auto.transition[node].add((node+1,'x+'))
			auto.states.add(node+1)
			node += 1
		if i == item[2]:
			ifnotlv7(auto.transition,node)
			auto.transition[node].add((node+1,'y+'))
			auto.states.add(node+1)
			node += 1
		if i == (item[0]+item[1]):
			ifnotlv7(auto.transition,node)
			auto.transition[node].add((node+1,'x-'))
			auto.states.add(node+1)
			node += 1
		if i == (item[0]+item[2]):
			ifnotlv7(auto.transition,node)
			auto.transition[node].add((node+1,'y-'))
			auto.states.add(node+1)
			node += 1
		if i == maxmum and i < (len(string)+1):
			ifnotlv7(auto.transition,node)
			auto.transition[node].add((node+1,'[sum]'))
			ifnotlv7(auto.transition,node+1)
			auto.states.add(node+1)
			breaking = 1
			break
		elif i == len(string)+1:
			ifnotlv7(auto.transition,node)
			#node += 1
		else:
			ifnotlv7(auto.transition,node)
			auto.transition[node].add((node+1,string[i-1]))
			auto.states.add(node+1)
			node += 1
	if breaking == 1:
		auto.end = node+1
		auto.last = node+1
	else:
		auto.end = node
		auto.last = node
	#print('node',node)
	#print('autocreate',auto.transition)
	#auto.transition[node+1] = []

	return auto, node, breaking
 
def combinationauto(mainauto,maindest,mainshortcut,item,string,varstates):
	auto, dest, shortcut = createauto(item,string,varstates)
	#print('mainauto',mainauto.transition)
	#print('maindest',maindest)
	#print('mainshortcut',mainshortcut)
	#print('auto',auto.transition)
	#print('dest',dest)
	#print('shortcut',shortcut)
	if shortcut == 1 and mainshortcut == 1:
		#print ('mode 1')
		for item in auto.transition[dest-1]:
			lastedge = item
		#lastedge = auto.transition[dest-1][0]
		
		#print('lastedge',lastedge)
		for i in range(auto.end,dest-2,-1):
			del auto.transition[i]
			auto.states.remove(i)
		auto.transition[dest-1] = set([])
		auto.states.add(dest-1)
		#print('beforeauto',auto.transition)
		auto.end = dest-1
		auto.renumber2(mainauto.last)
		mainauto.states = mainauto.states | auto.states
		#print('afterauto',auto.transition)
		for key, item in auto.transition.items():
			if not key in mainauto.transition:
				mainauto.transition[key] = set([])
			if key == auto.start:
				#mainauto.addedge(mainauto.start,item[0],item[1])
				mainauto.transition[mainauto.start].update(item)
			else:
				#mainauto.addedge(key,item[0],item[1])
				mainauto.transition[key].update(item)
		#print('auto.end',auto.end)
		#print('beforemainauto',mainauto.transition)
		mainauto.transition[auto.end].add( (maindest,lastedge[1]) )
		mainauto.states = mainauto.states | {auto.end}
		#mainauto.addedge(auto.end,maindest,lastedge[1])
		#print('automainauto',mainauto.transition)

	else:
		#print ('mode 2')
		for item in auto.transition[dest-1]:
			lastedge = item
		#lastedge = auto.transition[auto.end-1][0]
		
		#print('lastedge',lastedge)
		del auto.transition[auto.end]
		auto.transition[auto.end-1] = set([])
		auto.states.remove(auto.end)
		auto.states.remove(auto.end-1)
		#print('beforeauto',auto.transition)
		auto.end = auto.end-1
		auto.renumber2(mainauto.last)
		mainauto.states = mainauto.states | auto.states
		#print('afterauto',auto.transition)
		for key, item in auto.transition.items():
			if not key in mainauto.transition:
				mainauto.transition[key] = set([])
			if key == auto.start:
				#mainauto.addedge(mainauto.start,item[0],item[1])
				mainauto.transition[mainauto.start].update(item)
			else:
				#mainauto.addedge(key,item[0],item[1])
				mainauto.transition[key].update(item)
		#print('auto.end',auto.end)
		#print('beforemainauto',mainauto.transition)
		mainauto.transition[auto.end].add( (mainauto.end,lastedge[1]) )
		mainauto.states = mainauto.states | {auto.end}
		#mainauto.addedge(auto.end,mainauto.end,lastedge[1])
		#print('aftermainauto',mainauto.transition)

	if shortcut == 1 and mainshortcut == 0:
		mainshortcut = 1
		maindest = dest+mainauto.last

	mainauto.last = auto.end
	#time.sleep(10)
	#mainauto.printauto()
	return mainauto, maindest, mainshortcut

def stringequality(string):
	listoftup = []
	count = 0
	for i in range(1,len(string)+2):
		for j in range(1,len(string)+2-i):
			for k in range(1,len(string)+2-i):
				if string[j-1:j+i-1] == string[k-1:k+i-1]:
					if count == 0:
						autostring, deststring, shortcut = createauto((i,j,k),string,['x','y'])	
					else:
						autostring,deststring,shortcut = combinationauto(autostring,deststring,shortcut,(i,j,k),string,['x','y'])
					listoftup.append((i,j,k))
					count += 1
	#print(listoftup)
	print(len(listoftup))
	#print(count)
	#print('listoftup mem',sys.getsizeof(listoftup))
	'''
	autostring, deststring, shortcut = createauto(listoftup[0],string,['x','y'])	

	for i in range(1,len(listoftup)):
		autostring,deststring,shortcut = combinationauto(autostring,deststring,shortcut,listoftup[i],string,['x','y'])
		#sg.printgraph(autostring,str(i))
	'''
	autostring.tostr2()
	autostring.start = str(autostring.start)
	autostring.end = str(autostring.end)
	#autostring.printauto()
	#sg.printgraph(autostring,'final')
	#finallist, key, varedges = sc1.funchk(autostring)
	#finallist, key = functionalcheck(autostring)
	'''
	openlist, closelist = sc1.funchk(autostring)
	finallist, key = sc1.getvarconfig(autostring,openlist,closelist)
	print('key',key)
	for node, states in finallist.items():
		print ('node: ', node, ' varconfig: ', states)
	sg.printgraphconfig(autostring,finallist,'test3')
	sc1.csymtonulllong(autostring)

	addepsilon(autostring,finallist)

	for key, edges in autostring.transition.items():
		print('key: ', key)
		for edge in edges:
			print(edge)
		print('\n')

	sg.printgraph(autostring,'test4')
	print('auto1.tran',autostring.transition)
	print('auto1.start',autostring.start)
	print('auto1.end',autostring.end)
	'''

	return autostring


'''
auto1, dest1, shortcut = createauto((1,1,1),'abc',['x','y'])
auto1,dest1,shortcut = combinationauto(auto1,dest1,shortcut,(2,1,1),'abc',['x','y'])
print('space/n')
sg.printgraph(auto1,'test1')
auto1,dest1,shortcut = combinationauto(auto1,dest1,shortcut,(1,1,1),'abc',['x','y'])
#auto1.printauto()
sg.printgraph(auto1,'test')
'''

def main():
	start_time = time.time()
	string1 = 'a'*30
	
	auto1 = stringequality(string1)
	
	print("--- %s seconds ---" % (time.time() - start_time))
	#objgraph.show_most_common_types()	

if __name__ == "__main__":
	main()

