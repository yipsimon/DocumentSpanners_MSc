import script2rev as sc2
import script3rev as sc3
import scriptgrph as sg
import script1rev as sc1
import threading, time, sys, copy, objgraph, random, inspect, re

start_time = time.time()
key1 = {0: [1,2,3], 1:[4,5,6], 3:[7]}
key2 = {0: [2,3,4], 4:[1,3,5], 5:[]}

key1.update(key2)
print(key1)

print("--- %s seconds ---" % (time.time() - start_time))
sys.exit(1)