import script2
import threading, time, random, traceback, uuid, json, Queue, sys, copy

s2_out = script2.main()
print 's2_out' 
s2_out.printauto()
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