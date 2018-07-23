node = set(['x','y'])
node2 = set(['x'])


if (node & {'x'}) and (node2 & {'x'}):
	print ('close')

if (node & {'y'}) and (not node2 & {'y'}):
	print ('open')

if (not node & {'z'}) and (not node2 & {'z'}):
	print ('waiting')


print (node & {'c'})

temp = [(1,2),(3,4)]

temp.append((5,6))
print (temp)




