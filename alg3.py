import threading, time, random, traceback, uuid, json, Queue, sys, copy

def readauto():
    #filename = raw_input('Please enter a file name: ')
    fname = 'test'+'.txt'
    f = open(fname, 'r')
    data = []
    for line in f:
        data.extend(line.split(';'))
        del data[-1]

    f.close()
    return data

def sortedge(rdata):
	edata = {}
	sdata = {}
	for edge in rdata:
		edge = edge.split(',')
		if not edata.has_key(edge[0]):
			edata[edge[0]] = []
			sdata[edge[0]] = 'w'
		if not edata.has_key(edge[1]):
			edata[edge[1]] = []
			sdata[edge[1]] = 'w'

		if edge[2][-1] == '+':
			sdata[edge[1]] = 'o'
		elif edge[2][-1] == '-':
			sdata[edge[1]] = 'c'

		tup = (edge[1],edge[2])
		edata[edge[0]].append(tup)
		
	return edata, sdata


readdata = readauto()

edgedata, symdata = sortedge(readdata)

openlist = {'q0':set([])}
closelist = {'q0':set([])}
print 'readdata', readdata
print 'edgedata', edgedata
#print symdata

inptstr = 'aaa'
opening = 'x+' #opening 
closing = 'x-'
strlen = len(inptstr)
numnode = len(edgedata.keys())
symb = 'w'
functional = 1

seenlist = {'q0'}
todolist = {'q0'}
print openlist
print closelist
print seenlist
print todolist
#time.sleep(5)

while todolist:
	origin = todolist.pop()
	#print 'origin', origin
	#print 'edgedata[origin]', edgedata[origin]
	#time.sleep(2)
	for edge in edgedata[origin]:
		#print edge
		if edge[1][-1] == '+':
			#print 'in +'
			letter = edge[1][0]
			dest = edge[0]
			#print 'letter', letter
			#print 'dest', dest
			#time.sleep(2)
			if openlist[origin] & {letter}:
				#print 'in open already'
				functional = 0
				#print functional
				sys.exit(1)
			if seenlist & {dest}:
				#print 'seen'
				op = openlist[dest]
				oq = openlist[origin]
				cp = closelist[dest]
				cq = closelist[origin]
				if op != (oq | {letter}) or cp != cq:
					#print 'not the same'
					functional = 0
					#print functional
					sys.exit(1)
			else:
				#print 'not seen'
				seenlist.add(dest)
				todolist.add(dest)
				openlist[dest] = (openlist[origin] | {letter})
				closelist[dest] = closelist[origin]

		elif edge[1][-1] == '-':
			#print 'in -'
			letter = edge[1][0]
			dest = edge[0]
			#print 'letter', letter
			#print 'dest', dest
			#time.sleep(2)
			if (openlist[origin]-{letter} == openlist[origin]) or closelist[origin] & {letter}:
				#print 'in close already'
				functional = 0
				#print functional
				sys.exit(1)
			if seenlist & {dest}:
				#print 'seen'
				op = openlist[dest]
				oq = openlist[origin]
				cp = closelist[dest]
				cq = closelist[origin]
				#print cq | {letter}
				if op != oq  or cp != (cq | {letter}):
					#print 'not the same'
					functional = 0
					#print functional
					sys.exit(1)
			else:
				#print 'not seen'
				seenlist.add(dest)
				todolist.add(dest)
				openlist[dest] = openlist[origin] 
				closelist[dest] = (closelist[origin] | {letter})
		else:
			#print 'in letter'
			letter = edge[1][0]
			dest = edge[0]
			#print 'letter', letter
			#print 'dest', dest
			#time.sleep(2)
			if seenlist & {dest}:
				#print 'seen'
				op = openlist[dest]
				oq = openlist[origin]
				cp = closelist[dest]
				cq = closelist[origin]
				if op != oq  or cp != cq:
					#print 'not the same'
					functional = 0
					#print functional
					sys.exit(1)
			else:
				#print 'not seen'
				seenlist.add(dest)
				todolist.add(dest)
				openlist[dest] = openlist[origin] 
				closelist[dest] = closelist[origin]

		#print 'seenlist',seenlist
		#print 'todolist',todolist
		
		#time.sleep(6)
print 'openlist',openlist
print 'closelist',closelist
#all possible paths
graphg = {}
for i in range(strlen):
	graphg[int(i+1)] = {}
	for j in range(numnode):
		if j == numnode-1:
			name = 'qf'
		else:
			name = 'q'+str(j)
		tup = (i,name)
		avalue = 0
		ovalue = 0
		for item in edgedata[name]:
			if item[1] == inptstr[i]:
				if not graphg[int(i+1)].has_key(item[0]):
					graphg[int(i+1)][item[0]] = []
				graphg[int(i+1)][item[0]].append(tup)
				avalue = 1
			elif item[1] == opening and avalue == 1:
				if not graphg[int(i+1)].has_key(item[0]):
					graphg[int(i+1)][item[0]] = []
				graphg[int(i+1)][item[0]].append(tup)
				ovalue = 1
				oitem = item
			elif item[1] == closing and avalue == 1:
				if not graphg[int(i+1)].has_key(item[0]):
					graphg[int(i+1)][item[0]] = []
				graphg[int(i+1)][item[0]].append(tup)
		if ovalue == 1:
			for item in edgedata[oitem[0]]:
				if item[1] == closing:
					if not graphg[int(i+1)].has_key(item[0]):
						graphg[int(i+1)][item[0]] = []
					graphg[int(i+1)][item[0]].append(tup)
		avalue = 0
		ovalue = 0

#print readdata
#print edgedata
#print symdata

print 'graphg', graphg

#Prouming, getting the agraph lines
listofnodes = [(3,'qf')]
agraph = {}
for i in range(strlen):
	agraph[i] = {}

num = numnode-1
#print listofnodes

def varconfig(state):
	openset = openlist[state]
	closeset = closelist[state]
	if openset == set([]):
		output = 'w'
	else:
		if closeset == set([]):
			output = 'o'
		elif openset-closeset:
			opens = openset-closeset
			closes = closeset
			output = 'o:'
			for letter in opens:
				output = output+str(letter)
			output = output+',c:'
			for letter in closes:
				output = output+str(letter)
		else:
			output = 'c'

	return output




for i in range(numnode,0,-1):
	templist = []
	for j in range(len(listofnodes)-1,-1,-1):
		if listofnodes[j][0] == i:
			temptemplist = graphg[ listofnodes[j][0] ][ listofnodes[j][1] ]
			templist.extend(temptemplist)	
			for item in temptemplist:
				if not agraph[ item[0] ].has_key( item[1] ):
						agraph[item[0]][item[1]] = []
				varconf = varconfig(listofnodes[j][1])
				tup = (listofnodes[j][0], varconf, listofnodes[j][1])
				agraph[item[0]][item[1]].append(tup)

		if listofnodes[j][0] > i:
			break
	remove = 1
	while remove and len(templist) > 0:
		remove = 0
		item = templist[0]
		k = 1
		while k < len(templist):
			if item == templist[k]:
				templist.remove(templist[k])
				remove = 1
			k += 1

	listofnodes.extend(templist)


listofnodes.sort(key=lambda tup: tup[0])
print 'listofnodes', listofnodes

agraph[-1] = {'q0':[]}
zeroedges = agraph[0]
#print zeroedges
for key, value in zeroedges.iteritems():
	#print key, value
	temp = []
	for item in value:
		temp.append(item[1])
	#print temp
	temp.sort()
	#print temp
	zerostate = temp[-1]
	tup = (0,zerostate,key)
	agraph[-1]['q0'].append(tup)

print 'agraph', agraph


stackS = {}
seenstack = {}
for i in range(strlen+1):
	stackS[i] = []
	seenstack[i] = set()
print 'stackS',stackS
print 'seenstack', seenstack
print strlen

def minString(start):
	output = ''
	for i in range(start,strlen):
		for j in range(len(stackS[i])):
			currentnode = stackS[i][j]
			minletter = agraph[i-1][currentnode][0][1]
			for k in range(len(agraph[i-1][currentnode])):
				tup = agraph[i-1][currentnode][k]
				if tup[1] != minletter:
					if tup[1] == 'w':
						minletter = 'w'
					elif tup[1] == 'o' and minletter != 'w':
						minletter = 'o'

		#print minletter
		seenstack[i] = seenstack[i] | set(minletter)
		output = output+minletter
		for j in range(len(stackS[i])):
			currentnode = stackS[i][j]
			for k in range(len(agraph[i-1][currentnode])):
				tup = agraph[i-1][currentnode][k]
				if tup[1] == minletter:
					stackS[i+1].append(tup[2])
	output = output+'c'
	return output

def nextString(kstring):
	for i in range(strlen-1,-1,-1):
		cletter = kstring[i]
		#print i
		#print cletter
		#time.sleep(5)
		xletter = 0
		if cletter == 'w' or cletter == 'o':
			xletter = 1
		if xletter:
			nextletter = 0
			findletter = ''

			for j in range(len(stackS[i])):
				currentnode = stackS[i][j]
				for k in range(len(agraph[i-1][currentnode])):
					tup = agraph[i-1][currentnode][k]

					if tup[1] != cletter:
						if seenstack[i] != (seenstack[i] | set(tup[1])):
							if not findletter:
								findletter = tup[1]
							elif tup[1] == 'o':
								findletter = tup[1]
							nextletter = 1
			
			if nextletter == 1:
				seenstack[i] = seenstack[i] | set(findletter)
				for j in range(len(stackS[i])):
					currentnode = stackS[i][j]
					for k in range(len(agraph[i-1][currentnode])):
						tup = agraph[i-1][currentnode][k]
						if tup[1] == findletter:
							stackS[i+1].append(tup[2])
				#print 'kstring[i:]',kstring[:i]
				newk = kstring[:i]+findletter+minString(i+1)
				#print newk
				return newk
		else:
			stackS[i] = []
			seenstack[i] = set()

	return ''


stackS[0].append('q0')
kstr = minString(0)
print seenstack
while kstr:
	print kstr
	kstr = nextString(kstr)


						









ilist = copy.deepcopy(agraph[-1]['q0'])
#print 'ilist',ilist
default = 'c'
for i in range(strlen):
	default = default+'c'
word = list(default)
#print default
results = []
#print ilist
ilist.sort(key=lambda tup:tup[1], reverse = True)
#print ilist
while ilist:
	item = ilist[-1]
	ilist.remove(item)
	pos = item[0]
	letter = item[1]
	state = item[2]
	if letter == 'c':
		output = ''
		for i in range(pos):
			output = output+word[i]
		output = output+default[pos:]
		results.append(output)
	else:
		word[pos] = letter
		temp = agraph[pos][state]
		temp.sort(key=lambda tup:tup[1], reverse = True)
		ilist.extend(temp)

print 'results',results
'''
import functools
import graphviz as gv

graph = functools.partial(gv.Graph, format='pdf')
digraph = functools.partial(gv.Digraph, filename='fsm1', format='pdf')
digraph2 = functools.partial(gv.Digraph, filename='fsm2', format='pdf')

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

g = digraph()
g.attr(rankdir='LR', size='8,5')
g.attr('node', shape='doublecircle')
add_nodes(g, ['qf'] )
g.attr('node', shape='circle')
edgess = []
for item in readdata:
	item = item.split(',')
	tup = ((item[0],item[1]),{'label':item[2]})
	edgess.append(tup)

add_edges(g, edgess)
g.view()


#print agraph[-1]
f = digraph2()
f.attr(rank='same', rankdir='LR', size='8,5', splines='false')
f.attr('node', shape='doublecircle')
naming = '('+str(numnode)+', '+'qf'+')'
add_nodes(f, [naming] )
f.attr('node', shape='circle')
edgelisting = []
for i in range(-1,numnode):
	#print i
	if i == -1:
		source = 'q0'
		#print 'source',source
		templisting = agraph[-1]
		#print 'templisting',templisting
		for item in templisting:
			dest = '('+str(item[0])+', '+item[2]+')'
			tup = ((source,dest),{'label':item[1]})
			edgelisting.append(tup)
	else:
		templisting = agraph[i]
		for key, value in templisting.iteritems():
			for edge in value:
				source = '('+str(i)+', '+str(key)+')'
				dest = '('+str(edge[0])+', '+str(edge[2])+')'
				tup = ((source,dest),{'label':edge[1]})
				edgelisting.append(tup)
#print edgelisting


add_edges(f, edgelisting)
f.view()

'''