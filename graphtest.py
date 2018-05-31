import functools
import graphviz as gv

graph = functools.partial(gv.Graph, format='pdf')
digraph = functools.partial(gv.Digraph, filename='fsm', format='pdf')

def add_nodes(graph, nodes):
    for n in nodes:
        if isinstance(n, tuple):
            graph.node(n[0], **n[1])
        else:
            graph.node(n)
    return graph

def add_edges(graph, edges):
    for e in edges:
        if isinstance(e[0], tuple):
            graph.edge(*e[0], **e[1])
        else:
            graph.edge(*e)
    return graph

f = digraph()
f.attr(rankdir='LR', size='8,5')
f.attr('node', shape='doublecircle')
add_nodes(f, ['LR_0', 'LR_3','LR_4','LR_8'] )
f.attr('node', shape='circle')
add_edges(f, [ (('LR_0', 'LR_2'), {'label': 'SS(B)'}),
				(('LR_0', 'LR_1'), {'label': 'SS(S)'}),
				(('LR_1', 'LR_3'), {'label': 'S($end)'}),
				(('LR_2', 'LR_6'), {'label': 'SS(b)'}),
				(('LR_2', 'LR_5'), {'label': 'SS(a)'}),
				(('LR_2', 'LR_4'), {'label': 'SS(A)'}),
				(('LR_5', 'LR_7'), {'label': 'SS(b)'}),
				(('LR_5', 'LR_5'), {'label': 'SS(a)'}),
				(('LR_6', 'LR_6'), {'label': 'SS(b)'}),
				(('LR_6', 'LR_5'), {'label': 'SS(a)'}),
				(('LR_7', 'LR_8'), {'label': 'SS(b)'}),
				(('LR_7', 'LR_5'), {'label': 'SS(a)'}),
				(('LR_8', 'LR_6'), {'label': 'SS(b)'}),
				(('LR_8', 'LR_5'), {'label': 'SS(a)'})
				]
)
f.view()
'''
from graphviz import Digraph

f = Digraph('finite_state_machine', filename='fsm')
f.attr(rankdir='LR', size='8,5')

f.attr('node', shape='doublecircle')
f.node('LR_0')
f.node('LR_3')
f.node('LR_4')
f.node('LR_8')

f.attr('node', shape='circle')
f.edge('LR_0', 'LR_2', label='SS(B)')
f.edge('LR_0', 'LR_1', label='SS(S)')
f.edge('LR_1', 'LR_3', label='S($end)')
f.edge('LR_2', 'LR_6', label='SS(b)')
f.edge('LR_2', 'LR_5', label='SS(a)')
f.edge('LR_2', 'LR_4', label='S(A)')
f.edge('LR_5', 'LR_7', label='S(b)')
f.edge('LR_5', 'LR_5', label='S(a)')
f.edge('LR_6', 'LR_6', label='S(b)')
f.edge('LR_6', 'LR_5', label='S(a)')
f.edge('LR_7', 'LR_8', label='S(b)')
f.edge('LR_7', 'LR_5', label='S(a)')
f.edge('LR_8', 'LR_6', label='S(b)')
f.edge('LR_8', 'LR_5', label='S(a)')

f.view()
'''