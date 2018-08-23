import script2rev as sc2
import script3rev as sc3
import scriptgrph as sg
import script1rev as sc1
import threading, time, sys, copy, objgraph, random, inspect, re

start_prctime = time.time()
start_time = time.time()

automata1 = sc2.automata(0,0,0)
automata1.reset()
automata1.states = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17']
automata1.varstates = ['x']
automata1.transition['0'] = [('0','(.)'),('1','x+')]
automata1.transition['1'] = [('2','[0-9]')]
automata1.transition['2'] = [('3','[0-9]'),('4','[epsi]')]
automata1.transition['3'] = [('4','[0-9]'),('4','[epsi]')]
automata1.transition['4'] = [('5','.')]
automata1.transition['5'] = [('6','[0-9]')]
automata1.transition['6'] = [('7','[0-9]'),('8','[epsi]')]
automata1.transition['7'] = [('8','[0-9]'),('8','[epsi]')]
automata1.transition['8'] = [('9','.')]
automata1.transition['9'] = [('10','[0-9]')]
automata1.transition['10'] = [('11','[0-9]'),('12','[epsi]')]
automata1.transition['11'] = [('12','[0-9]'),('12','[epsi]')]
automata1.transition['12'] = [('13','.')]
automata1.transition['13'] = [('14','[0-9]')]
automata1.transition['14'] = [('15','[0-9]'),('16','[epsi]')]
automata1.transition['15'] = [('16','[0-9]'),('16','[epsi]')]
automata1.transition['16'] = [('17','x-')]
automata1.transition['17'] = [('17','(.)')]
automata1.start = '0'
automata1.end = '17'
automata1.last = 17


sc1.funchk(automata1)
sc1.csymtonulllong(automata1)
#sg.printgraph(automata1,'test00')

f = open('access_log2', 'r')
string = f.read()
f.close() #\d+\.

#condits = [(lambda s,i,j: re.match(r'^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$',s[j-1:j+i-1]))] #,(lambda s,i,j: s[j+i-2:j+i-1] in ['0','1','2','3','4','5','6','7','8','9'], 'true')] #,(lambda i: i % 7 == 0, "seven")]
#,(lambda s,i,j: re.match(r'^(?<=' ')\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?=' ')$',s[j-2:j+i-1]))]
condits = [(lambda s,i,j: re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$',s[j-1:j+i-1])),\
			(lambda s,i,j: True if j-1 == 0 else (True if re.match(r'^[^0-9]$',s[j-2]) else False) ),\
			(lambda s,i,j: True if j+i-1 == len(string) else (True if re.match(r'^[^0-9]$',s[j+i-1]) else False) )]

string, automata = sc3.stringequality(string,1,7,16,condits)
print("stringeq : %s seconds" % (time.time() - start_time))
start_time = time.time()
#sg.printgraphconfig(automata,automata.varconfig,'test2')
#sys.exit(1)
#objgraph.show_most_common_types()
#sc1.funchk(automata)

sc1.csymtonulllong(automata)
print("toepsilion : %s seconds" % (time.time() - start_time))
start_time = time.time()

automata = sc3.joinver1(automata,automata1)
print("Joined : %s seconds" % (time.time() - start_time))
start_time = time.time()

finalgraph = sc1.generateAg(automata,string)
print("Ag graph : %s seconds" % (time.time() - start_time))
start_time = time.time()

outputs = sc1.calcresults(finalgraph, len(string), automata.varconfig)
print("Calc : %s seconds" % (time.time() - start_time))
start_time = time.time()


sc1.printresultsv2(outputs,automata,string,0,0,1)
print("Total Time: %s seconds" % (time.time() - start_prctime))
#objgraph.show_most_common_types()


sys.exit(1)