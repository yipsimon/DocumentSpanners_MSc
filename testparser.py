from __future__ import unicode_literals, print_function
'''
try:
    text=unicode
except:
    text=str
'''
from arpeggio import Optional, ZeroOrMore, OneOrMore, EOF, \
    ParserPython, PTNodeVisitor, visit_parse_tree
from arpeggio import RegExMatch as _
from arpeggio import ParserPython
#dot -Tpng -O .dot
'''
def number():     return _(r'\d*\.\d*|\d+')
def factor():     return Optional(["+","-"]), [number, ("(", expression, ")")]
def term():       return factor, ZeroOrMore(["*","/"], factor)
def expression(): return term, ZeroOrMore(["+", "-"], term)
def calc():       return OneOrMore(expression), EOF

parser = ParserPython(calc)


parse_tree = parser.parse("-(4-1)*5+(2+4.67)+5.89/(.2+7)")
'''

# Grammar
'''
def foo(): return "a", bar, "b", baz, "c", ZeroOrMore(bar)
def bar(): return "bar"
def baz(): return "baz"
'''
'''
def regform(): return OneOrMore(statement), EOF
def statement(): return [("(",expression,")",Optional(symb)), (expression,Optional(symb))]
def symb():	return ["*","+"]
def expression(): return statetype,Optional(symb), ZeroOrMore(["&",".","|"],statetype)
def statetype():	return [letter,varconfig]
def letter():	return _(r'[a-z]')
def varconfig():	return ["{", letter, ":", statement, "}"]
'''
'''
#def regform(): return OneOrMore(expression), EOF
#def statement(): return expression
def symb():	return ["*","+"]
def expression(): return Optional("("), statetype, Optional(")"), ZeroOrMore(["&",".","|"],statetype), Optional(")"),
def statetype():	return [(letter,Optional(symb)),varconfig]
def letter():	return _(r'[a-z]')
def varconfig():	return "{", letter, ":", expression, "}"
'''
'''
def alpha():	return [("(",alpha,"&",alpha,")"), ("(",alpha,".",alpha,")"), ("(",alpha,"|",alpha,")"), (alpha,symb), varconfig, letter]
def letter():	return _(r'[a-z]')
def symb():	return ["*","+"]
def varconfig():	return "{", letter, ":", alpha, "}"
'''
'''
def regform2(): return OneOrMore(statement), EOF
def statement(): return [statetype,varconfig]
def statetype():	return Optional("("),letter, ZeroOrMore(["&",".","|"],letter),Optional(")"), Optional(symb)
def symb():	return ["*","+"]
def varconfig():	return Optional("("), "{", letter, ":", statement, "}",ZeroOrMore(["&",".","|"],varconfig),Optional(")")
def letter():	return _(r'[a-z]')
'''
'''
def regform2(): return OneOrMore(statement), EOF
def statement(): return [statetype,statetype]
def statetype():	return Optional("("),letter,Optional(symb), ZeroOrMore(["&",".","|"],letter,Optional(symb)),Optional(")"), Optional(symb)
def symb():	return ["*","+"]
def varconfig():	return Optional("("), "{", letter, ":", statetype, "}",ZeroOrMore(["&",".","|"],varconfig),Optional(")")
def letter():	return _(r'[a-z]')
'''
'''
def regex(): return [letter, star, union]
def letter():	return _(r'[a-z]')
def star(): return '(', regex, ')','*'
def union(): return '(', regex ,'|', regex,')'
'''
'''
#def regform1():	return OneOrMore(regform2), EOF
def regform1(): return expression, ZeroOrMore(["&",".","|"],expression)
def expression(): return [varconfig, statement]
def statement():	return [(letter,symb), ("(",letter,ZeroOrMore(["&",".","|"],statement),")",Optional(symb)), letter]
def varconfig():	return "{", letter, ":", statement, "}"
def symb():	return ["*","+"]
def letter():	return _(r'[a-z]')
'''
'''
def regform1(): return expression, ZeroOrMore(["&",".","|"],expression)
def expression(): return [varconfig, statement, ("(",varconfig,")"),("(",statement,")")]
def statement():	return [(letter,symb), (statement,ZeroOrMore(["&",".","|"],statement)), letter]
def varconfig():	return ["{", letter, ":", statement, "}", (varconfig,ZeroOrMore(["&",".","|"],varconfig))]
def symb():	return ["*","+"]
def letter():	return _(r'[a-z]')
'''
'''
def formula():		return OneOrMore(expression)
def expression():	return ["\ety", letter, concat, star, union, plus, varconfig]
def letter():	return _(r'[a-z]')
def concat():	return "(", expression, ".", expression, ")"
def star(): return "(", expression, ")","*"
def union(): return "(", expression ,"|", expression,")"
def plus(): return "(", expression, ")","+"
def varconfig(): return "{", letter ,":", expression,"}"
'''
'''
def formula():		return OneOrMore(expression)
def expression():	return ["\ety", letter, algop, varalg]
def algop():		return [("(", expression, [".","|"], expression, ")"), ("(", expression, ")", ["*","+"])]
def varalg(): return "{", letter ,":", expression,"}"
def letter():	return _(r'[a-z]')
'''
def formula():		return OneOrMore(expression)
def expression():	return [concat, union, plus, varconfig, brackets,letter]
def letter():	return [_(r'[a-z]'), "\ety"]
def concat():	return letter, OneOrMore(".", expression)
def union(): return letter, OneOrMore("|", expression)
def plus(): return letter,"+"
def varconfig(): return "{", letter ,":", expression,"}"
def brackets():	return "(", expression, ")"
'''
def formula():		return OneOrMore(expression)
def expression():	return [concat, union, varconfig, brackets, letter]
#def relations():	return [concat, union, plus]
def letter():	return [_(r'[a-z]'), "\ety", varconfig, plus]
def alphabet():	return _(r'[a-z]')
def concat():	return letter, OneOrMore(".", expression)
def union(): return letter, OneOrMore("|", expression)
def plus(): return letter,"+"
def varconfig(): return "[", alphabet ,":", letter,"]"
def brackets():	return "(", expression, ")"
'''

class automata():
	def __init__(self,startnode,endnode,value):
		self.start = startnode
		self.end = [endnode]
		self.lastnum = endnode
		self.states = set([startnode,endnode])
		self.transition = {startnode: [(endnode,value)]}	

	'''
	def initialise(self):
		self.end = []
		self.lastnum = 0
		self.states = set([0])
		self.transition = {}			
	'''

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
		#print ('start',start)
		#print ('dest',dest)
		#print ('value',value)
		tup = (dest,value)
		self.states = self.states | {start,dest}
		#print ('states',self.states)
		#print ('transition',self.transition)
		if not self.transition.has_key(start):
			self.transition[start] = []
		self.transition[start].append(tup)
		#print ('transition',self.transition)
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
	#def visit_expression(self, node, children):
	global count
	count = 0

	def visit_letter(self, node, children):
		global count
		'''
		if self.debug:
			print ('Converting edge {}'.format(node.value))
			print (count)
		let = str(node.value)
		tup = (str(count)+let+'s',str(count+1)+let+'f',let)
		count += 2
		return [tup]
		'''
		print ('LETTER')
		auto = automata(0,1,node.value)
		auto.printauto()
		return auto


	def visit_union(self, node, children):
		'''
		templist = []
		#print (len(children))
		global count
		if self.debug:
			print ('Converting list {}'.format(node.value))
			print (count)
		for i in range(0,len(children),2):
			#print (i)
			#print (children[i])

			if isinstance(children[i], list):
				#utup1 = ('u'+children[i][0][0][:-1]+children[i+1][0][0][:-1],children[i][0][0],"empty")
				#utup2 = ('u'+children[i][0][0][:-1]+children[i+1][0][0][:-1],children[i+1][0][0],"empty")
				utup1 = ('u'+str(count)+'s',children[i][0][0],"empty")
				utup2 = ('u'+str(count)+'s',children[i+1][0][0],"empty")
				#utup2 = ('u'+children[i][0][0][:-1]+children[i+1][0][0][:-1],children[i+1][0][0],"empty")
				#if self.debug:
				#	print ('Converting edge {}'.format(utup))
				templist.append(utup1)
				templist.append(utup2)
				templist.extend(children[i])
				templist.extend(children[i+1])
				count += 1


		return templist
		'''
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



# Parsing
parser = ParserPython(formula, debug=True) #, reduce_tree = True)
input_regex = 'a|(b|c)'
parse_tree = parser.parse(input_regex)
result = visit_parse_tree(parse_tree, formVisitor(debug=True))

result.printauto()

print("{} = {}".format(input_regex, result))
'''
result = parser.parse("a bar b baz c bar bar bar")

# Accessing parse tree nodes. All asserts will pass.
# Index access
assert result[1].rule_name  == 'bar'
# Access by rule name
assert result.bar.rule_name == 'bar'

# There are 8 children nodes of the root 'result' node.
# Each child is a terminal in this case.
assert len(result) == 8

# There is 4 bar matched from result (at the beginning and from ZeroOrMore)
# Dot access collect all NTs from the given path
assert len(result.bar) == 4
# You could call dot access recursively, e.g. result.bar.baz if the
# rule bar called baz. In that case all bars would be collected from
# the root and for each bar all baz will be collected.

# Verify position
# First 'bar' is at position 2 and second is at position 14
assert result.bar[0].position == 2
assert result.bar[1].position == 14

'''
'''
from arpeggio.export import PMDOTExporter

PMDOTExporter().exportFile(parser.parser_model,"formula_parser_model.dot")
PTDOTExporter().exportFile(parse_tree,"concat_parse_tree.dot")
'''