from __future__ import unicode_literals, print_function
from arpeggio import Optional, ZeroOrMore, OneOrMore, EOF, \
    ParserPython, PTNodeVisitor, visit_parse_tree
from arpeggio import RegExMatch as _
from arpeggio import ParserPython
import sys
#dot -Tpng -O .dot

def formula():		return OneOrMore(expression)
def expression():	return [concat, union, plus, varconfig, brackets,letter]
def letter():	return [_(r'[a-z]'), "\ety"]
def concat():	return letter, OneOrMore(".", expression)
def union(): return letter, OneOrMore("|", expression)
def plus(): return letter,"+"
def varconfig(): return "{", letter ,":", expression,"}"
def brackets():	return "(", expression, ")"

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
		self.states = self.states | auto1.states
		for key, item in auto1.transition.iteritems():
			if not self.transition.has_key(key):
				self.transition[key] = []
			self.transition[key].extend(item)
		self.printauto()

	def printauto(self):
		print ('start',self.start)
		print ('end',self.end)
		print ('states',self.states)
		print ('transition',self.transition)


class formVisitor(PTNodeVisitor):

	def visit_letter(self, node, children):	
		print ('LETTER')
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
	'''
	def visit_concat(self, node, children):
		templist = []

		for i in range(0, len(children), 2):
			if isinstance(children[i], list):
				templist.extend(children[i])
				for item in children[i+1]:
					if item[0][-1] == 's':
						startnode = item[0]
				for item in children[i]:
					if item[1][-1] == 'f':
						utup = (item[1],startnode,"empty")
						templist.append(utup)
				templist.extend(children[i+1])

		return templist	

	'''

def main():
	# Parsing
	parser = ParserPython(formula, debug=True) #, reduce_tree = True)
	input_regex = 'a|(b|c)'
	parse_tree = parser.parse(input_regex)
	result = visit_parse_tree(parse_tree, formVisitor(debug=True))

	print (result.printauto())
	return result
	#print("{} = {}".format(input_regex, result))

if __name__ == "__main__":
	main()