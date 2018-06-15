from __future__ import unicode_literals, print_function
from arpeggio import Optional, ZeroOrMore, OneOrMore, EOF, \
    ParserPython, PTNodeVisitor, visit_parse_tree
from arpeggio import RegExMatch as _
from arpeggio import ParserPython
import sys
#dot -Tpng -O .dot

def alphabet():	return _(r'[a-z]')
def varconfig(): 	return "[", _(r'[a-z]') ,":", expression,"]"
def terminals():	return [alphabet, "\ety", varconfig, ("(", expression, ")")]
def plus(): 		return terminals,"+"
def concat():		return terminals, OneOrMore(".", terminals)
def union(): 		return terminals, OneOrMore("|", terminals)
def expression():	return [concat, union, varconfig, plus, terminals]
def formula():		return OneOrMore(expression)


class automata():
	def __init__(self,startnode,endnode,value):
		self.start = startnode
		self.end = [endnode]
		self.lastnum = endnode
		self.states = set([startnode,endnode])
		self.transition = {startnode: [(endnode,value)]}	

	def renumber(self,num):
		self.start += num
		temp = []
		for nodes in self.end:
			temp.append(nodes+num)
		self.end = temp
		temp = set([])
		for nodes in self.states:
			num1 = nodes+num
			temp.add(num1)
		self.states = temp
		self.lastnum = num1
		temp = {}
		for key, item in self.transition.iteritems():
			temp[key+num] = []
			for tup in item:
				ntup = (tup[0]+num,tup[1])
				temp[key+num].append(ntup)
		self.transition = temp

	def addedge(self,start,dest,value):
		tup = (dest,value)
		if dest > self.lastnum:
			self.lastnum = dest
		self.states = self.states | {start,dest}
		if not self.transition.has_key(start):
			self.transition[start] = []
		self.transition[start].append(tup)
		print('ADDEDGE',start,dest,value)
		self.printauto()

	def union(self,auto1):
		self.renumber(1)
		self.addedge(0,1,'/ety')
		self.start = 0
		count = self.lastnum+1
		self.addedge(0,count,'/ety')
		auto1.renumber(count)
		self.end.extend(auto1.end)
		self.lastnum = auto1.lastnum
		self.states = self.states | auto1.states
		for key, item in auto1.transition.iteritems():
			if not self.transition.has_key(key):
				self.transition[key] = []
			self.transition[key].extend(item)

		self.printauto()

	def concat(self,auto1):
		count = self.lastnum+1
		auto1.renumber(count)
		for node in self.end:
			self.addedge(node,count,'/ety')
		self.end = []
		self.end.extend(auto1.end)
		self.lastnum = auto1.lastnum
		self.states = self.states | auto1.states
		for key, item in auto1.transition.iteritems():
			if not self.transition.has_key(key):
				self.transition[key] = []
			self.transition[key].extend(item)

		self.printauto()

	def plus(self):
		for node in self.end:
			self.addedge(0,node,'/ety')
		self.renumber(1)
		self.start = 0
		self.addedge(0,1,'/ety')

		self.printauto()

	def varconfig(self,alpha):
		self.renumber(1)
		self.start = 0
		last = self.lastnum+1
		self.addedge(0,1,str(alpha)+'+')
		for node in self.end:
			self.addedge(node,last,str(alpha)+'-')
		self.end = [last]

		self.printauto()

	def printauto(self):
		print ('start',self.start)
		print ('end',self.end)
		print ('states',self.states)
		print ('transition',self.transition)


class formVisitor(PTNodeVisitor):

	def visit_alphabet(self, node, children):
		print ('LETTER')
		print ('node.value',node.value)
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
		return auto
	
	def visit_concat(self, node, children):
		print ('CONCAT')
		auto = children[0]
		print ('children',len(children))
		auto.printauto()
		for i in range(1,len(children)):
			children[i].printauto()
			auto.concat(children[i])
		return auto
	
	def visit_plus(self, node, children):
		print ('PLUS')
		auto = children[0]
		auto.plus()
		return auto

	def visit_varconfig(self, node, children):
		print ('VARCONFIG')
		auto = children[1]
		auto.varconfig(children[0])
		auto.printauto()
		return auto

def main():
	# Parsing
	parser = ParserPython(formula, debug=True) #, reduce_tree = True)
	input_regex = "[x:(a|b)]"
	#input_regex = raw_input('Enter regex formula: ')
	parse_tree = parser.parse(input_regex)
	result = visit_parse_tree(parse_tree, formVisitor(debug=True))

	result.printauto()
	return result
	#print("{} = {}".format(input_regex, result))

if __name__ == "__main__":
	main()