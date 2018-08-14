import script2rev as sc2
import script3rev as sc3
import scriptgrph as sg
import script1rev as sc1
import threading, time, sys, copy, objgraph, random, inspect, re

start_time = time.time()
matching = re.match('(?=(.))(?=a)','A')
print(matching.groups())


print("--- %s seconds ---" % (time.time() - start_time))
sys.exit(1)