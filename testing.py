a = set([1,2,3])
b = set([3])
for item in a:
	item = str(item)
	print item[-1]
	print int(item[-1])
	if item[-1] == '1':
		print item
