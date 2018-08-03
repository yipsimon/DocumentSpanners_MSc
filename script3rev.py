import script2rev as sc2
import scriptgrph as sg
import script1rev as sc1
import threading, time, sys, copy, objgraph, random, inspect


def convertregex(regex):
	auto = sc2.main(regex)
	
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

def projectionver1(auto,text,listofprojections,finallist, key):
	
	sc1.projectionv1(auto,listofprojections)

	print('key',key)
	print('finallist',finallist)
	newkey = {}
	subtract = 0
	listing = []
	listingletters = []
	for k in key.keys():
		if k in listofprojections:
			listing.append(key[k])
			listingletters.append(k)
	for i in range(len(listingletters)):
		newkey[str(listingletters[i])] = i

	for ky, item in finallist.items():
		tempstate = []
		print('ky',ky)
		print('item',item)
		for pos in listing:
			print('pos',pos)
			tempstate.append(item[pos])
		print('tempstate',tempstate)
		finallist[ky] = tempstate
	print('key',key)
	print('newkey',newkey)
	print('finallist',finallist)


	outputs = normalprocess(auto,text,finallist)

	printresults(outputs)

def projectionver2(auto,text,listofprojections,finallist, key):

	finalgraph = sc1.generateAg(auto,text,finallist)

	finalprintable = sc1.finalauto(finalgraph,finallist,auto.end)

	sg.printgraph(finalprintable,'g2')

	#sc1.projectionv2(finallist,key,listofprojections)
	print('key',key)
	print('finallist',finallist)
	newkey = {}
	subtract = 0
	listing = []
	listingletters = []
	for k in key.keys():
		if k in listofprojections:
			listing.append(key[k])
			listingletters.append(k)
	for i in range(len(listingletters)):
		newkey[str(listingletters[i])] = i

	for ky, item in finallist.items():
		tempstate = []
		print('ky',ky)
		print('item',item)
		for pos in listing:
			print('pos',pos)
			tempstate.append(item[pos])
		print('tempstate',tempstate)
		finallist[ky] = tempstate
	print('key',key)
	print('newkey',newkey)
	print('finallist',finallist)

	outputs = sc1.calcresults(finalgraph, len(text), finallist)

	printresults(outputs)


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


def addepsilon(auto,finallist):
	for startnode, tuples in auto.transition.items():
		for tup in tuples:
			if tup[1] == '[epsi]' and finallist[startnode] != finallist[tup[0]]:
				checkfunction(auto,finallist,startnode,tup[0])

def checkfunction(auto,finallist,start,search):
	for tup in auto.transition[search]:
		if tup[1] == '[epsi]' and finallist[search] != finallist[tup[0]] and tup[0] != start:
			auto.addedge(start,tup[0],'[epsi]')
			checkfunction(auto,finallist,start,tup[0])

def joinver1(auto1,auto2):	
	finallist1, key1, varedges1 = sc1.funchk(auto1)
	finallist2, key2, varedges2 = sc1.funchk(auto2)
	print('finallist1',finallist1)
	print('finallist2',finallist2)
	sc1.csymtonull(auto1,varedges1)
	sc1.csymtonull(auto2,varedges2)
	addepsilon(auto1,finallist1)
	addepsilon(auto2,finallist2)


	auto, keytemp = joincreate(auto1,auto2,key1,key2)

	key3 = {}
	template = list()
	for i in range(len(auto.varstates)):
		key3[str(auto.varstates[i])] = i
		template.append('w')

	
	todo = set([(auto1.start,auto2.start)])
	done = set([])
	finallist = {str((auto1.start,auto2.start)): template}
	while todo:
		print('todo\n',todo)
		currentnode = todo.pop()
		auto.states.add(str(currentnode))
		done.add(currentnode)
		print('currentnode\n',currentnode)
		print('\n')
		seen = set([])
		for edge1 in auto1.transition[currentnode[0]]:
			print('edge1',edge1)
			fail = 0
			for variable in auto.varstates:
				if keytemp[variable][0] == -1 or keytemp[variable][1] == -1:
					fail = 0
				elif finallist1[edge1[0]][keytemp[variable][0]] != finallist2[currentnode[1]][keytemp[variable][1]]:
					fail = 1
					break
			dest = (edge1[0],currentnode[1])
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
						finallist[str(dest)][key3[variable]] = finallist1[str(dest[0])][tup[0]]
					elif tup[1] != -1 and tup[0] == -1:
						#finallist[str(dest)][1] = finallist2[str(dest[1])][tup[1]]
						finallist[str(dest)][key3[variable]] = finallist2[str(dest[1])][tup[1]]
					else:
						finallist[str(dest)][key3[variable]] = finallist1[str(dest[0])][tup[0]]
						#finallist[str(dest)][0] = finallist1[str(dest[0])][tup[0]]
						#finallist[str(dest)][1] = finallist2[str(dest[1])][tup[1]]

				end = (str(dest), edge1[1])
				auto.transition[str(currentnode)].append(end)
				if not done & {dest}:
					todo.add(dest)
					
		print('final',finallist)
		for edge2 in auto2.transition[currentnode[1]]:
			print('edge2',edge2)
			fail = 0
			for variable in auto.varstates:
				if keytemp[variable][0] == -1 or keytemp[variable][1] == -1:
					fail = 0
				elif finallist1[currentnode[0]][keytemp[variable][0]] != finallist2[edge2[0]][keytemp[variable][1]]:
					fail = 1
					break
			dest = (currentnode[0],edge2[0])
			if fail == 0 and (not seen & {dest}):
				seen.add(dest)
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
				auto.transition[str(currentnode)].append(end)
				if not done & {dest}:
					todo.add(dest)
					

		

	return auto, finallist, key3

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
		table[key] = []

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
			auto.transition[node].append((node+1,'x+'))
			auto.states.add(node+1)
			node += 1
		if i == item[2]:
			ifnotlv7(auto.transition,node)
			auto.transition[node].append((node+1,'y+'))
			auto.states.add(node+1)
			node += 1
		if i == (item[0]+item[1]):
			ifnotlv7(auto.transition,node)
			auto.transition[node].append((node+1,'x-'))
			auto.states.add(node+1)
			node += 1
		if i == (item[0]+item[2]):
			ifnotlv7(auto.transition,node)
			auto.transition[node].append((node+1,'y-'))
			auto.states.add(node+1)
			node += 1
		if i == maxmum and i < (len(string)+1):
			ifnotlv7(auto.transition,node)
			auto.transition[node].append((node+1,'[sum]'))
			ifnotlv7(auto.transition,node+1)
			auto.states.add(node+1)
			breaking = 1
			break
		elif i == len(string)+1:
			ifnotlv7(auto.transition,node)
			#node += 1
		else:
			ifnotlv7(auto.transition,node)
			auto.transition[node].append((node+1,string[i-1]))
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
		lastedge = auto.transition[dest-1][0]
		#print('lastedge',lastedge)
		for i in range(auto.end,dest-2,-1):
			del auto.transition[i]
			auto.states.remove(i)
		auto.transition[dest-1] = []
		auto.states.add(dest-1)
		#print('beforeauto',auto.transition)
		auto.end = dest-1
		auto.renumber(mainauto.last)
		mainauto.states = mainauto.states | auto.states
		#print('afterauto',auto.transition)
		for key, item in auto.transition.items():
			if not key in mainauto.transition:
				mainauto.transition[key] = []
			if key == auto.start:
				#mainauto.addedge(mainauto.start,item[0],item[1])
				mainauto.transition[mainauto.start].extend(item)
			else:
				#mainauto.addedge(key,item[0],item[1])
				mainauto.transition[key].extend(item)
		#print('auto.end',auto.end)
		#print('beforemainauto',mainauto.transition)
		mainauto.transition[auto.end].append( (maindest,lastedge[1]) )
		mainauto.states = mainauto.states | {auto.end}
		#mainauto.addedge(auto.end,maindest,lastedge[1])
		#print('automainauto',mainauto.transition)

	else:
		#print ('mode 2')
		lastedge = auto.transition[auto.end-1][0]
		#print('lastedge',lastedge)
		del auto.transition[auto.end]
		auto.transition[auto.end-1] = []
		auto.states.remove(auto.end)
		auto.states.remove(auto.end-1)
		#print('beforeauto',auto.transition)
		auto.end = auto.end-1
		auto.renumber(mainauto.last)
		mainauto.states = mainauto.states | auto.states
		#print('afterauto',auto.transition)
		for key, item in auto.transition.items():
			if not key in mainauto.transition:
				mainauto.transition[key] = []
			if key == auto.start:
				#mainauto.addedge(mainauto.start,item[0],item[1])
				mainauto.transition[mainauto.start].extend(item)
			else:
				#mainauto.addedge(key,item[0],item[1])
				mainauto.transition[key].extend(item)
		#print('auto.end',auto.end)
		#print('beforemainauto',mainauto.transition)
		mainauto.transition[auto.end].append( (mainauto.end,lastedge[1]) )
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
	#listoftup = []
	count = 0
	for i in range(1,len(string)+2):
		for j in range(1,len(string)+2-i):
			for k in range(1,len(string)+2-i):
				if string[j-1:j+i-1] == string[k-1:k+i-1]:
					if count == 0:
						autostring, deststring, shortcut = createauto((i,j,k),string,['x','y'])	
					else:
						autostring,deststring,shortcut = combinationauto(autostring,deststring,shortcut,(i,j,k),string,['x','y'])
					#listoftup.append((i,j,k))
					count += 1
	#print(listoftup)
	#print(len(listoftup))
	#print(count)
	#print('listoftup mem',sys.getsizeof(listoftup))
	'''
	autostring, deststring, shortcut = createauto(listoftup[0],string,['x','y'])	

	for i in range(1,len(listoftup)):
		autostring,deststring,shortcut = combinationauto(autostring,deststring,shortcut,listoftup[i],string,['x','y'])
		#sg.printgraph(autostring,str(i))
	'''
	autostring.tostr()
	autostring.start = str(autostring.start)
	autostring.end = str(autostring.end)
	#autostring.printauto()
	#sg.printgraph(autostring,'final')
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
	string1 = 'a'*20
	print(string1)
	print(sys.getsizeof(string1))
	auto1 = stringequality(string1)
	print(sys.getsizeof(auto1))
	auto1.printauto()
	print("--- %s seconds ---" % (time.time() - start_time))
	objgraph.show_most_common_types()	

if __name__ == "__main__":
	main()

