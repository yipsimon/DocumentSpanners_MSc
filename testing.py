seenlist = set([1,2,3])
b = set([3])
if seenlist & {3}:
	print seenlist

let = 'abcds'
for letter in let:
	print letter
results = {0:[5,6],1:[7,8],2:[9,9]}
graphing = {0:{0:[5,6],1:[7,8],2:[9,9]},1:{0:[1,2],1:[3,4],2:[5,6]},2:{}}
print graphing[1] 
print results
states = set([])
for key, liste in graphing[0].iteritems():
	states = states | set(liste)
print states
graphing[2] = results
print graphing[2]
endnode = (0,'q'+str('0'))
enode = str(endnode)
print enode
test = {enode : [1,2,3]}
print test

list1 = ['w','w']
list2 = ['w','o']
if list1 == list2:
	print 'ok'
