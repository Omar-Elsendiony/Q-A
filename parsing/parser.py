import ast
string = "s = 5"
x = compile(source = string, filename ="test", mode="exec", flags= ast.PyCF_ONLY_AST)
print(ast.dump(x, indent=4))  # either this 
print("+++++++++++++++++++++++++++++++++++++++")
print(ast.dump(ast.parse(string), indent = 4)) # or this

from typing import AnyStr
import ast
string = "s = 5\nmyString = 'Hell'\nprint(myString)"
tree = compile(source = string, filename ="test", mode="exec", flags= ast.PyCF_ONLY_AST)
from graphviz import Digraph
dot = Digraph()
# Define a function to recursively add nodes to the Digraph
def add_node(node, parent=None):
    node_name = str(node.__class__.__name__)
    dot.node(str(id(node)), node_name)
    if parent:
        dot.edge(str(id(parent)), str(id(node)))
    for child in ast.iter_child_nodes(node):
        add_node(child, node)


# Add nodes to the Digraph
add_node(tree)

# Render the Digraph as a PNG file
dot.format = 'png'
dot.render('my_ast', view=True)