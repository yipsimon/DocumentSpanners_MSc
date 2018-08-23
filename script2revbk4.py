from __future__ import unicode_literals, print_function
from arpeggio import Optional, ZeroOrMore, OneOrMore, EOF, \
    ParserPython, PTNodeVisitor, visit_parse_tree
from arpeggio import RegExMatch as _
from arpeggio import ParserPython
import sys, time, re, copy
#dot -Tpng -O .dot
'''
def alphabet():		return _(r'([^"])+')
def varconfig(): 	return "<", _(r'[a-zA-Z0-9]') ,":", expression,">"
def terminals():	return [('"',alphabet,'"'), varconfig, ("(", expression, ")")]
def plus(): 		return terminals,"+"
def star():			return terminals,"*"
def concat():		return terminals, OneOrMore(",", terminals)
def union(): 		return terminals, OneOrMore("|", terminals)
def expression():	return [concat, union, varconfig, plus, star, terminals]
def formula():		return OneOrMore(expression)
'''
def alphabet():		return _(r'([^\,\|\<\>\*\+])+')
def varconfig(): 	return "<", _(r'[a-zA-Z0-9]') ,":", expression,">"
def terminals():	return [plus, star,("(", expression, ")"), alphabet, varconfig]
def plus(): 		return alphabet,"+"
def star():			return alphabet,"*"
def concat():		return terminals, OneOrMore(",", terminals)
def union(): 		return terminals, OneOrMore("|", terminals)
def expression():	return [concat, union, varconfig, terminals]
def formula():		return OneOrMore(expression), EOF

class automata():
	def __init__(self,startnode,endnode,value):
		self.start = startnode
		self.end = endnode
		self.last = endnode
		self.varstates = []
		self.key = {}
		self.varconfig = {} 
		self.states = set([startnode,endnode])
		self.transition = {startnode: [(endnode,value)], endnode: []}

	def reset(self):
		self.start = 0
		self.end = 0
		self.last = 0
		self.varstates = []
		self.key = {}
		self.varconfig = {} 
		self.states = set([])
		self.transition = {}

	def tostr(self):
		temp = {}
		for key, items in self.transition.items():
			temp[str(key)] = []
			for item in items:
				nitem = (str(item[0]),str(item[1]))
				temp[str(key)].append(nitem)

		self.transition = temp
		temp2 = []
		for item in self.states:
			temp2.append(str(item))
		self.states = temp2
		self.start = str(self.start)
		self.end = str(self.end)

	def tostr2(self):
		temp = {}
		for key, items in self.transition.items():
			temp[str(key)] = set([])
			for item in items:
				nitem = (str(item[0]),str(item[1]))
				temp[str(key)].add(nitem)

		self.transition = temp
		temp2 = set([])
		for item in self.states:
			temp2.add(str(item))
		self.states = temp2
		self.start = str(self.start)
		self.end = str(self.end)

	def tostr3(self):
		temp = {}
		for key, items in self.transition.items():
			if key == 0:
				temp[str(key)] = []
				for item in items:
					nitem = (str(item[0]),str(item[1]))
					temp[str(key)].append(nitem)
			elif items != '':
				nitem = (str(items[0]),str(items[1]))
				temp[str(key)] = nitem

		self.transition = temp
		temp2 = set([])
		for item in self.states:
			temp2.add(str(item))
		self.states = temp2
		self.start = str(self.start)
		self.end = str(self.end)

	def tostr4(self):
		temp = {}
		for key, items in self.transition.items():
			temp[str(key)] = []
			for item in items:
				nitem = (str(item[0]),str(item[1]))
				temp[str(key)].append(nitem)
		
		self.transition = temp
		temp2 = []
		for item in self.states:
			temp2.append(str(item))
		self.states = temp2
		self.start = str(self.start)
		self.end = str(self.end)

	def rename(self):
		ref = {}
		ref[str(self.start)] = 0
		i = 1
		for node in self.states:
			if node != str(self.start) and node != str(self.end):
				ref[str(node)] = i
				i += 1
		ref[str(self.end)] = i
		print(ref)
		self.start = str(ref[str(self.start)])
		self.end = str(ref[str(self.end)])
		print(self.start)
		print(self.end)
		
		self.last = i
		self.states = set([])
		for node in range(i+1):
			self.states.add(str(node))
		for name in list(self.varconfig.keys()):
			temp2 = self.varconfig[name]
			del self.varconfig[name]
			self.varconfig[str(ref[name])] = copy.deepcopy(temp2)
		for begin in list(self.transition.keys()):
			temp = []
			for tup in self.transition[begin]:
				print(tup)
				temp.append( (str(ref[str(tup[0])]),tup[1]) )
			del self.transition[begin]
			print(temp)
			self.transition[str(ref[begin])] = copy.deepcopy(temp)


	def rename2(self):
		ref = {}
		ref[str(self.start)] = 0
		i = 1
		for node in self.states:
			if node != str(self.start) and node != str(self.end):
				ref[str(node)] = i
				i += 1
		ref[str(self.end)] = i
		print(ref)
		self.start = ref[str(self.start)]
		self.end = ref[str(self.end)]
		self.last = self.end
		print(self.start)
		print(self.end)
		
		self.last = i
		self.states = set([])
		for node in range(i+1):
			self.states.add(str(node))
		for name in list(self.varconfig.keys()):
			temp2 = self.varconfig[name]
			del self.varconfig[name]
			self.varconfig[str(ref[name])] = copy.deepcopy(temp2)

		temptran = {}
		for begin in list(self.transition.keys()):
			temp = []
			for tup in self.transition[begin]:
				print(tup)
				temp.append( (ref[str(tup[0])],tup[1]) )
			#del self.transition[begin]
			#print(temp)
			temptran[ref[begin]] = copy.deepcopy(temp)
		self.transition = temptran

	def renumber2(self,num):
		self.start += num
		self.end += num
		temp = set([])
		for nodes in self.states:
			num1 = int(nodes)+num
			temp.add(num1)
		self.states = temp
		self.lastnum = num1
		temp = {}
		for key, item in self.transition.items():
			temp[int(key)+num] = set([])
			for tup in item:
				ntup = (tup[0]+num,tup[1])
				temp[int(key)+num].add(ntup)
		self.transition = temp

	def renumber3(self,num):
		self.start += num
		self.end += num
		temp = []
		for nodes in self.states:
			num1 = int(nodes)+num
			temp.append(num1)
		self.states = temp
		self.lastnum = num1
		temp = {}
		for key, item in self.transition.items():
			#temp[int(key)+num] = set([])
			if isinstance(item,list):
				for tup in item:
					#print(tup)
					ntup = (int(tup[0])+num,tup[1])
					temp[int(key)+num] = ntup
			elif item != '':
				nitem = (int(item[0])+num,item[1])
				temp[int(key)+num] = nitem
		self.transition = temp

	def renumber5(self,num):
		self.start += num
		self.end += num
		self.last += num
		temp = {}
		for key, items in self.transition.items():
			temp[int(key)+num] = []
			for item in items:
				nitem = (int(item[0])+num,item[1])
				temp[int(key)+num].append(nitem)
		self.transition = temp

	def renumber6(self,num):
		self.start += num
		self.end += num
		self.last += num
		temp = {}
		for key, items in self.transition.items():
			if isinstance(items, list):
				temp[int(key)+num] = []
				for item in items:
					nitem = (int(item[0])+num,item[1])
					temp[int(key)+num].append(nitem)
			else:
				nitem = (int(items[0])+num,items[1])
				temp[int(key)+num] = nitem

		self.transition = temp
		
	def renumber(self,num):
		self.start += num
		self.end += num
		temp = set([])
		for nodes in self.states:
			num1 = int(nodes)+num
			temp.add(num1)
		self.states = temp
		self.lastnum = num1
		temp = {}
		for key, item in self.transition.items():
			temp[int(key)+num] = []
			for tup in item:
				ntup = (int(tup[0])+num,tup[1])
				temp[int(key)+num].append(ntup)
		self.transition = temp

	def renumber4(self,num):
		self.start += num
		self.end += num
		temp = []
		for nodes in self.states:
			num1 = int(nodes)+num
			temp.append(num1)
		self.states = temp
		self.lastnum = num1
		temp = {}
		for key, item in self.transition.items():
			temp[int(key)+num] = []
			for tup in item:
				ntup = (tup[0]+num,tup[1])
				temp[int(key)+num].append(ntup)
		self.transition = temp

	def addedge(self,start,dest,value):
		tup = (dest,value)
		if dest > self.end:
			self.end = dest
			self.transition[dest] = []
		self.states = self.states | {start,dest}
		if not start in self.transition:
			self.transition[start] = []
		self.transition[start].append(tup)
		#print('ADDEDGE',start,dest,value)
		#self.printauto()

	def union(self,auto1):
		'''
		self.renumber(1)
		self.start = 0
		auto1.renumber(self.end+1)
		lastnode = auto1.end+1
		self.addedge(self.end,lastnode,'[epsi]')
		self.addedge(auto1.end,lastnode,'[epsi]')
		self.addedge(0,1,'[epsi]')
		self.addedge(0,auto1.start,'[epsi]')
		'''
		auto1.renumber(self.end)
		for item in auto1.varstates:
			if item not in self.varstates:
				self.varstates.append(item)
		for key, item in auto1.transition.items():
			if not key in self.transition:
				self.transition[key] = []
			if key == auto1.start:
				self.transition[self.start].extend(item)
			else:
				self.transition[key].extend(item)
		
		lastnode = auto1.end+1
		self.addedge(self.end,lastnode,'[epsi]')
		self.addedge(auto1.end,lastnode,'[epsi]')
		self.states = self.states | auto1.states
		#self.printauto()

	def concat(self,auto1):
		#or
		#self.addedge(self.end,self.end+1,'[epsi]')
		auto1.renumber(self.end)
		self.states = self.states | auto1.states
		for item in auto1.varstates:
			if item not in self.varstates:
				self.varstates.append(item)

		for key, item in auto1.transition.items():
			if not key in self.transition:
				self.transition[key] = []
			self.transition[key].extend(item)
		self.end = auto1.end
		#self.printauto()


	def plus(self):
		self.addedge(self.end,0,'[epsi]')
		#self.renumber(1)
		self.start = 0
		#self.addedge(0,1,'[epsi]')
		self.addedge(self.end,self.end+1,'[epsi]')
		#self.addedge(0,self.end,'[epsi]')
		#self.printauto()

	def star(self):
		self.addedge(self.end,0,'[epsi]')
		#self.renumber(1)
		self.start = 0
		#self.addedge(0,1,'[epsi]')
		self.addedge(self.end,self.end+1,'[epsi]')
		self.addedge(0,self.end,'[epsi]')
		#self.printauto()		

	def addvarconfig(self,alpha):
		self.renumber(1)
		self.start = 0
		self.varstates.append(str(alpha))
		self.addedge(0,1,str(alpha)+'+')
		self.addedge(self.end,self.end+1,str(alpha)+'-')

		#self.printauto()

	def printauto(self):
		print(' -- automata data --')
		print ('start : ',self.start)
		print ('end : ',self.end)
		print ('last : ',self.last)
		print ('varstates : ',self.varstates)
		print ('states : ',self.states)
		print ('key : ',self.key)
		if self.varconfig:
			print ('varconfiguration ')
			for key, var in self.varconfig.items():
				print ('key : ', key, ' varconfig : ', var)
		else:
			print ('varconfiguration ', self.varconfig)
		if self.transition:
			print ('All transitions ')
			for key, edges in self.transition.items():
				print ('key : ',key)
				print('edges : ',edges)
		else:
			print ('All transitions ', self.transition)
		

class formVisitor(PTNodeVisitor):

	def visit_alphabet(self, node, children):
		print ('LETTER')
		print ('node.value',node.value)
		#time.sleep(5)
		auto = automata(0,1,node.value)
		auto.printauto()
		return auto

	def visit_union(self, node, children):
		print ('UNION')
		auto = children[0]
		print ('children',len(children))
		auto.printauto()
		for i in range(1,len(children)):
			children[i].printauto()
			auto.union(children[i])

		auto.printauto()
		return auto
	
	def visit_concat(self, node, children):
		print ('CONCAT')
		auto = children[0]
		print ('children',len(children))
		auto.printauto()
		for i in range(1,len(children)):
			children[i].printauto()
			auto.concat(children[i])

		auto.printauto()
		return auto
	
	def visit_plus(self, node, children):
		print ('PLUS')
		auto = children[0]
		auto.plus()

		auto.printauto()
		return auto

	def visit_star(self, node, children):
		print ('STAR')
		auto = children[0]
		auto.star()

		auto.printauto()
		return auto

	def visit_varconfig(self, node, children):
		print ('VARCONFIG')
		auto = children[1]
		auto.addvarconfig(children[0])
		
		auto.printauto()
		return auto

def main(argv):
	#print(str(argv))
	
	# Parsing
	#different alg relation next to each other i.e a*|b require brackets (a*)|b
	parser = ParserPython(formula, debug=True) #, reduce_tree = True)
	#input_regex = " (a*) & [x:(b&[y:c])]"
	#input_regex = input('Enter regex formula: ')
	parse_tree = parser.parse(argv)
	result = visit_parse_tree(parse_tree, formVisitor())

	result.printauto()

	#time.sleep(10)
	result.tostr()
	return result
	#print("{} = {}".format(input_regex, result))
	
	

if __name__ == "__main__":
	main(sys.argv[1])