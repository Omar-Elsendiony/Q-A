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
    handleLst = []
    setBodyNodes = set()
    def visit(self, node):
        if (hasattr(node.parent, 'body') and node.__class__.__name__ != "Compare"):  # check if it falls directly under a node that has body attr that can encompass it
            self.setBodyNodes.add(node.parent)
            self.handleLst.append(node)
        return super().visit(node)


class InsertChildNode(ast.NodeTransformer):
    def visit(self, node):
        print(node.__class__.__name__)
        return super().visit(node)

tree = """if (val is none):
    print('None')"""
treeAST = ast.parse(tree)
print(ast.dump(treeAST, indent=4))
# InsertChildNode().visit(treeAST)

import random
# random.randint will take the integers in the range inclusive of the two numbers

# for i, parent in enumerate(mutator.get_parents):
#     parent.body.insert(mutator.get_indices[i], new_node.body[0])

# trialVisitor().visit(parent_node)
# print(trialVisitor.handleLst)
# print(trialVisitor.setBodyNodes)

# # choose from elements body nodes
# # choose a random body node
# k = random.choice(list(trialVisitor.setBodyNodes))
# # print(k)

# # choose a random index
# indexBody = random.randint(0, len(k.body) - 1)
# k.body.insert(indexBody, ast.parse("print('Hello World')").body[0])

# print('------------------------------------')
# print(ast.unparse(parent_node))
# print('------------------------------------')


