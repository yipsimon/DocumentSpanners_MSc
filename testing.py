a = set([1,2,3])
print a
a = a | {3,4,5}
print a

temp = set([])
for item in a:
	temp.add(item+1)
print temp
a = temp
temp = set([])
print a
print temp
for item in a:
	temp.add(item+2)
b = temp
print a
print temp
print b
temp = {}
transition = {1: [(2,'a'),(3,'b')], 2: [(3,'c'),(4,'d')]}
for key, item in transition.iteritems():
	print key, item
	temp[key+1] = []
	for tup in item:
		ntup = (tup[0]+1,tup[1])
		temp[key+1].append(ntup)

print transition
print temp