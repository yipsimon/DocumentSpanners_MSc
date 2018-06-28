graphing = {0: {0: set([0,1,2]), 1: set([1,2]), 2: set([2]) }, \
			1: {0: set([0,1,2]), 1: set([1,2]), 2: set([2]) }, \
			2: {0: set([2]), 1: set([2]), 2: set([2]) }, \
			-1: {0: set([0,1,2]) } }
varstate = {0: ['w'], 1: ['o'], 2:['c']}
#renaming
finalgraph = {}

def ghaskey(graph,node):
	if not graph.has_key(node):
		graph[node] = []

for key, item in graphing.iteritems():
	for key2, item2 in item.iteritems():
		for item3 in item2:
			if key == -1:
				node1 = 'q0'
			else:
				node1 = (key,key2)
			node2 = (key+1,item3)
			value = varstate[item3]
			ghaskey(finalgraph,node1)
			finalgraph[node1].append([node2,value])

print finalgraph

s = {}
avali = {}
edging = {}

for i in range(-1,3):
	s[i] = set([])
	edging[i] = {}
	avali[i] = []

s[-1].add(0)
#test = [(1,2),(1,1),(2,2),(2,1),(1,0),(0,2),(0,1),(2,0),(0,0)]
test = [['w','o'],['o','c'],['c','w'],['o','w'],['o','o'],['w','w'],['c','o'],['w','c'],['c','c']]
test.sort(key=lambda tup:tup[1], reverse=1)
test.sort(key=lambda tup:tup[0], reverse=1)
print test
def haskey(graph,node):
	if not graph.has_key(node):
		graph[node] = set([])


def minString(num):
	tempedge = {}
	letter = []
	last = []
	leng = len(varstate[0])
	for i in range(num,2):
		for item1 in s[i]:
			for item in graphing[i][int(item1)]:
				temp = varstate[int(item)]
				if not temp in avali[i]:
					avali[i].append(temp)
				haskey(tempedge,str(temp))
				tempedge[str(temp)].add(item)
				edging[i] = tempedge

		for j in range(leng-1,0,-1):
			avali[i].sort(key=lambda tup: tup[j])
		print 'avali',avali
		print 'tempedge',tempedge

		letter.append(avali[i][0])

		print 'letter',letter

		s[i+1] = s[i+1] | tempedge[str(avali[i][0])]
		print 's',s
		print '\n'

	for j in range(leng):
		last.append(['c'])
	letter.extend(last)
	return letter

k = minString(-1)
print k
print 'edging',edging

def nextString(word):
	print 'start nextString'
	output = word
	output.pop()
	for i in range(1,-2,-1):
		print 'i',i
		let = word[i+1]
		print 'let',let
		output.pop()
		print 'output', output
		if len(avali[i]) != 1:
			print 'avali',avali[i]
			avali[i].remove(let)
			print 'avali removed',avali[i]
			output.append(avali[i][0])
			print 'output1',output
			s[i+1] = edging[i][str(avali[i][0])]
			print 's',s
			nk = minString(i+1)
			output.extend(nk)
			print 'outputfinal',output
			return output
		else:
			s[i+1] = set([])
			avali[i] = []
			edging[i]
			print 's',s
			print 'avali[i]',avali

	return output
listofout = []
while k != []:
	print 'k',k
	listofout.append(str(k))
	k = nextString(k)

for i in range(len(listofout)):
	print listofout[i]












