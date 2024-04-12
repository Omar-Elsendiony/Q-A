from typing import AnyStr
import ast
from graphviz import Digraph
string = """


import random

# Generate a list of 10 random numbers between 1 and 100
random_numbers = [random.randint(1, 100) for _ in range(10)]

# Print the unsorted list
print("Unsorted numbers:", random_numbers)

# Sort the list
random_numbers.sort()

# Print the sorted list
print("Sorted numbers:", random_numbers)

"""
tree :ast = compile(source = string, filename ="test", mode="exec", flags= ast.PyCF_ONLY_AST)
# Create a Graphviz Digraph object
dot = Digraph()
# Define a function to recursively add nodes to the Digraph
def add_node(node, parent=None):
    node_name = str(node.__class__.__name__)
    for field, val in ast.iter_fields(node):
        if (field == "id"):
            print(node)
            print(field, val)
            node_name += ":" + str(val)
    # print("=========================================")
    
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

# def get_height(node):
# print(dot.)
# print(nodes)
# tree.NodeVisitor()

# dump function
# is very beneficial in debugging by allowing printing ast data 
print(ast.dump((tree), indent=3))


# n = ast.NodeVisitor()
# print(n.visit(tree))