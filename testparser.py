from __future__ import unicode_literals
from arpeggio import Optional, ZeroOrMore, OneOrMore, EOF, \
    ParserPython, PTNodeVisitor, visit_parse_tree
from arpeggio import RegExMatch as _
from arpeggio import ParserPython

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

def regex(): return [letter, star, union]
def letter():	return _(r'[a-z]')
def star(): return '(', regex, ')','*'
def union(): return '(', regex ,'|', regex,')'

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



# Parsing
parser = ParserPython(regex, debug=True)
result = parser.parse("(a)*")
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



from arpeggio.export import PMDOTExporter
PMDOTExporter().exportFile(parser.parser_model,"my_parser_model.dot")

PTDOTExporter().exportFile(parse_tree,"my_parse_tree.dot")
'''