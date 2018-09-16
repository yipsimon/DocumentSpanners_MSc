from __future__ import unicode_literals, print_function
from arpeggio import Optional, ZeroOrMore, OneOrMore, EOF, \
    ParserPython, PTNodeVisitor, visit_parse_tree
from arpeggio import RegExMatch as _
from arpeggio import ParserPython
import sys, time, re, copy
#dot -Tpng -O .dot

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
		self.states = [startnode,endnode]
		self.transition = {startnode: [(endnode,value)], endnode: []}

	def reset(self):
		self.start = 0
		self.end = 0
		self.last = 0
		self.varstates = []
		self.key = {}
		self.varconfig = {} 
		self.states = []
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

	def rename(self):
		ref = {}
		ref[str(self.start)] = 0
		i = 1
		for node in self.states:
			if node != str(self.start) and node != str(self.end):
				ref[str(node)] = i
				i += 1
		ref[str(self.end)] = i
		self.start = str(ref[str(self.start)])
		self.end = str(ref[str(self.end)])
		self.last = i
		self.states = []
		for node in range(i+1):
			self.states.append(str(node))

		temp2 = {}
		for name in self.varconfig.keys():
			temp2[str(ref[str(name)])] = self.varconfig[name]
		self.varconfig = temp2

		temp3 = {}
		for begin in self.transition.keys():
			temp = []
			for tup in self.transition[begin]:
				temp.append( (str(ref[tup[0]]),tup[1]) )
			temp3[str(ref[begin])] = copy.deepcopy(temp)
		self.transition = temp3


	def toint(self):
		ref = {}
		ref[str(self.start)] = 0
		i = 1
		for node in self.states:
			if node != str(self.start) and node != str(self.end):
				ref[str(node)] = i
				i += 1
		ref[str(self.end)] = i

		self.start = ref[str(self.start)]
		self.end = ref[str(self.end)]
		self.last = i
		self.states = []
		for node in range(i+1):
			self.states.append(node)

		temp2 = {}
		for name in self.varconfig.keys():
			temp2[ref[name]] = self.varconfig[name]
		self.varconfig = temp2

		temp3 = {}
		for begin in self.transition.keys():
			temp = []
			for tup in self.transition[begin]:
				temp.append( (ref[str(tup[0])],tup[1]) )
			temp3[ref[begin]] = copy.deepcopy(temp)
		self.transition = temp3
		
	def renumber(self,num):
		self.start += num
		self.end += num
		temp = []
		for nodes in self.states:
			num1 = int(nodes)+num
			temp.append(num1)
		self.states = temp
		self.last += num
		temp = {}
		for key, item in self.transition.items():
			temp[int(key)+num] = []
			for tup in item:
				ntup = (int(tup[0])+num,tup[1])
				temp[int(key)+num].append(ntup)
		self.transition = temp
		temp = {}
		for key, item in self.varconfig.items():
			temp[int(key)+num] = []
			for tup in item:
				temp[int(key)+num].append(tup)
		self.varconfig = temp

	def addedge(self,start,dest,value):
		tup = (dest,value)
		if dest > self.end:
			self.end = dest
			self.last = dest

		if not start in self.transition:
			self.transition[start] = []
			self.states.append(start)
		self.transition[start].append(tup)
		if not dest in self.transition:
			self.transition[dest] = []
			self.states.append(dest)
		

	def union(self,auto1):
		auto1.renumber(self.end)
		for item in auto1.varstates:
			if item not in self.varstates:
				self.varstates.append(item)
		for key, item in auto1.transition.items():
			if not key in self.transition:
				self.transition[key] = []
				self.states.append(key)
			if key == auto1.start:
				self.transition[self.start].extend(item)
			else:
				self.transition[key].extend(item)
		
		self.addedge(self.end,auto1.end+1,'[epsi]')
		self.addedge(auto1.end,auto1.end+1,'[epsi]')

	def concat(self,auto1):
		auto1.renumber(self.end)
		for item in auto1.varstates:
			if item not in self.varstates:
				self.varstates.append(item)
		for key, item in auto1.transition.items():
			if not key in self.transition:
				self.transition[key] = []
				self.states.append(key)
			self.transition[key].extend(item)
		
		self.end = auto1.end
		self.last = auto1.end

	def plus(self):
		self.addedge(self.end,0,'[epsi]')
		self.start = 0
		self.addedge(self.end,self.end+1,'[epsi]')
		
	def star(self):
		self.addedge(self.end,0,'[epsi]')
		self.start = 0
		self.addedge(self.end,self.end+1,'[epsi]')
		self.addedge(0,self.end,'[epsi]')

	def addvarconfig(self,alpha):
		self.renumber(1)
		self.start = 0
		self.varstates.append(str(alpha))
		self.addedge(0,1,str(alpha)+'+')
		self.addedge(self.end,self.end+1,str(alpha)+'-')

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
			print ('varconfiguration: None ')
		if self.transition:
			print ('All transitions ')
			for key, edges in self.transition.items():
				print ('key : ',key)
				print('edges : ',edges)
		else:
			print ('All transitions: None ')
		

class formVisitor(PTNodeVisitor):

	def visit_alphabet(self, node, children):
		#print ('LETTER')
		#print ('node.value',node.value)
		auto = automata(0,1,node.value)
		return auto

	def visit_union(self, node, children):
		#print ('UNION')
		auto = children[0]
		#print ('children',len(children))
		for i in range(1,len(children)):
			#children[i].printauto()
			auto.union(children[i])
		return auto
	
	def visit_concat(self, node, children):
		#print ('CONCAT')
		auto = children[0]
		#print ('children',len(children))
		for i in range(1,len(children)):
			#children[i].printauto()
			auto.concat(children[i])
		return auto
	
	def visit_plus(self, node, children):
		#print ('PLUS')
		auto = children[0]
		auto.plus()
		return auto

	def visit_star(self, node, children):
		#print ('STAR')
		auto = children[0]
		auto.star()
		return auto

	def visit_varconfig(self, node, children):
		#print ('VARCONFIG')
		auto = children[1]
		auto.addvarconfig(children[0])
		return auto

def main(argv):
	# Parsing
	#different alg relation next to each other i.e a*|b require brackets (a*)|b
	parser = ParserPython(formula)#, debug=True) #, reduce_tree = True)
	parse_tree = parser.parse(argv)
	result = visit_parse_tree(parse_tree, formVisitor())
	result.tostr()
	return result
	#print("{} = {}".format(input_regex, result))

if __name__ == "__main__":
	main(sys.argv[1])