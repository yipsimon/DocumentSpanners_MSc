import script2rev as sc2
import script3rev as sc3
import scriptgrph as sg
import script1rev as sc1
import threading, time, sys, copy, objgraph, random, inspect, re, texttable

start_time = time.time()

tab = texttable.Texttable()
headings = ['Names','Weights','Costs','Unit_Costs']
tab.header(headings)
names = ['bar', 'chocolate','chips']
weights = [0.05, 0.1, 0.25]
costs = [2.0, 5.0, 3.0]
unit_costs = [40.0, 50.0, 12.0]

for row in zip(names, weights, costs, unit_costs):
	tab.add_row(row)

s = tab.draw()

print(s)


sys.exit(1)