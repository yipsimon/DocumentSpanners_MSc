import threading, time, random, traceback, uuid, json, Queue, sys

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
	print 'origin', origin
	print 'edgedata[origin]', edgedata[origin]
	#time.sleep(2)
	for edge in edgedata[origin]:
		print edge
		if edge[1][-1] == '+':
			print 'in +'
			letter = edge[1][0]
			dest = edge[0]
			print 'letter', letter
			print 'dest', dest
			#time.sleep(2)
			if openlist[origin] & {letter}:
				print 'in open already'
				functional = 0
				print functional
				sys.exit(1)
			if seenlist & {dest}:
				print 'seen'
				op = openlist[dest]
				oq = openlist[origin]
				cp = closelist[dest]
				cq = closelist[origin]
				if op != (oq | {letter}) or cp != cq:
					print 'not the same'
					functional = 0
					print functional
					sys.exit(1)
			else:
				print 'not seen'
				seenlist.add(dest)
				todolist.add(dest)
				openlist[dest] = (openlist[origin] | {letter})
				closelist[dest] = closelist[origin]

		elif edge[1][-1] == '-':
			print 'in -'
			letter = edge[1][0]
			dest = edge[0]
			print 'letter', letter
			print 'dest', dest
			#time.sleep(2)
			if (openlist[origin]-{letter} == openlist[origin]) or closelist[origin] & {letter}:
				print 'in close already'
				functional = 0
				print functional
				sys.exit(1)
			if seenlist & {dest}:
				print 'seen'
				op = openlist[dest]
				oq = openlist[origin]
				cp = closelist[dest]
				cq = closelist[origin]
				print cq | {letter}
				if op != oq  or cp != (cq | {letter}):
					print 'not the same'
					functional = 0
					print functional
					sys.exit(1)
			else:
				print 'not seen'
				seenlist.add(dest)
				todolist.add(dest)
				openlist[dest] = openlist[origin] 
				closelist[dest] = (closelist[origin] | {letter})
		else:
			print 'in letter'
			letter = edge[1][0]
			dest = edge[0]
			print 'letter', letter
			print 'dest', dest
			#time.sleep(2)
			if seenlist & {dest}:
				print 'seen'
				op = openlist[dest]
				oq = openlist[origin]
				cp = closelist[dest]
				cq = closelist[origin]
				if op != oq  or cp != cq:
					print 'not the same'
					functional = 0
					print functional
					sys.exit(1)
			else:
				print 'not seen'
				seenlist.add(dest)
				todolist.add(dest)
				openlist[dest] = openlist[origin] 
				closelist[dest] = closelist[origin]

		print 'seenlist',seenlist
		print 'todolist',todolist
		print 'openlist',openlist
		print 'closelist',closelist
		#time.sleep(6)






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

print readdata
print edgedata
print symdata
print graphg

#Prouming, getting the agraph lines
listofnodes = [(3,'qf')]
agraph = {}
for i in range(strlen):
	agraph[i] = {}

num = numnode-1
print listofnodes

for i in range(numnode,0,-1):
	templist = []
	for j in range(len(listofnodes)-1,-1,-1):
		if listofnodes[j][0] == i:
			temptemplist = graphg[ listofnodes[j][0] ][ listofnodes[j][1] ]
			templist.extend(temptemplist)	
			for item in temptemplist:
				if not agraph[ item[0] ].has_key( item[1] ):
						agraph[item[0]][item[1]] = []

				tup = (listofnodes[j][0], symdata[ listofnodes[j][1] ], listofnodes[j][1])
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
print listofnodes
print agraph


