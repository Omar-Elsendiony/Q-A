import ast



# code to add child to a node in ast tree
# Create the parent node
# parent_node = ast.parse("x = 1")

# Create the child node
parent_node = ast.parse("""
y = 5
x = 1
while (y < 10):
    if x == 1:
        print("Hello World")
    else:
        print("Bye World")
    y += 1
x = 2   
                       """)

# check if the node type is ast node, if yes take it
# if isinstance(child_node, ast.AST):
#     parent_node.body.append(child_node)

# # Add the child node to the parent node
# parent_node.body.append(child_node)

# Print the modified AST tree
print(ast.dump(parent_node, indent=4))

def parentify(tree):
    tree.parent = None
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node
parentify(parent_node)


class trialVisitor(ast.NodeVisitor):
    countNodes = 0

    def visit(self, node):
        if (hasattr(node.parent, 'body')):  # check if it falls directly under a node that has body attr that can encompass it
            print(node.__class__.__name__)
            trialVisitor.countNodes += 1
        return super().visit(node)


trialVisitor().visit(parent_node)
print(trialVisitor.countNodes)


