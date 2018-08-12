import script2rev as sc2
import script3rev as sc3
import scriptgrph as sg
import script1rev as sc1
import threading, time, sys, copy, objgraph, random, inspect

start_time = time.time()
regex = "'[a]',<x:'a'>,'@'"
auto = sc2.main(regex)


print("--- %s seconds ---" % (time.time() - start_time))