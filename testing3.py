import script2rev as sc2
import script3rev as sc3
import scriptgrph as sg
import script1rev as sc1
import threading, time, sys, copy, objgraph, random, inspect, re

start_time = time.time()
f = open('access_log', 'r')
#with open('access_log2') as f:
#readdata = ''
#for line in f:
#	readdata = readdata + line
string = f.read()
f.close()
#print(len(string))
count = 0
#string = 'aaa\naaaa'
stor = []
for i in range(12,13):
	for j in range(1,len(string)+2-i):
		skip = 1
		for k in range(j+1,len(string)+2-i):
			if skip == 0:
				if string[k+i-2:k+i-1] == '\n':
					skip = 1
				elif string[j-1:j+i-1] == string[k-1:k+i-1]:
					stor.append( (j,string[j-1:j+i-1],k,string[k-1:k+i-1]) )
					count += 1
			if skip == 1:
				if string[k-1:k] == '\n':
					skip = 0

print (count)
for item in stor:
	print (item)

'''
for i in range(12,13):
	for j in range(1,len(string)+2-i):
		skip = 1
		for k in range(1,len(string)+2-i):
			if string[k+i-2:k+i-1] != '\n':
				k = k+i-1

			if string[k-1:k] != '\n':
				if string[j-1:j+i-1] == string[k-1:k+i-1]:
					stor.append( (j,string[j-1:j+i-1],k,string[k-1:k+i-1]) )
					count += 1




for line in f:
	print(line)

whole = ''
for j in readdata:
	for k in readdata:

	whole = whole+let
	ip = '64.242.88.10'
	if let == '\n':
		print(whole)
		whole = ''

'''

print("--- %s seconds ---" % (time.time() - start_time))
sys.exit(1)