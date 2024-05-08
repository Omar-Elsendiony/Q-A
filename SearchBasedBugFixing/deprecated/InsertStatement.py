import ast



# code to add child to a node in ast tree
# Create the parent node
# parent_node = ast.parse("x = 1")

# Create the child node
parent_node = ast.parse("""
def calculate_average(numbers):
  # Bug: We're adding the numbers but dividing by one less than the length
  total_sum = sum(numbers)
  average = total_sum / (len(numbers) - 1)  # This is incorrect
  return average""")

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

def isInBody(node):
    for child in node.parent.body:
        if (child is node):
            return True
    return False

class insertionVisitor(ast.NodeVisitor):
    countNodes = 0
    handleLst = [] # handles for candidates that can be inserted in the body of the parent node
    setBodyNodes = set()  # set of nodes that can be the vessel for another statements
    def visit(self, node):
        if (hasattr(node.parent, 'body') and node.__class__.__name__ != "FunctionDef"):  # check if it falls directly under a node that has body attr that can encompass it
            if (isInBody(node)):
                self.setBodyNodes.add(node.parent)
                self.handleLst.append(node)
        return super().visit(node)


# class InsertChildNode(ast.NodeTransformer):
#     def visit(self, node):
#         print(node.__class__.__name__)
#         return super().visit(node)

# tree = """if (val is none):
#     print('None')"""
# treeAST = ast.parse(tree)
# print(ast.dump(treeAST, indent=4))
# InsertChildNode().visit(treeAST)

import random
# random.randint will take the integers in the range inclusive of the two numbers

# for i, parent in enumerate(mutator.get_parents):
#     parent.body.insert(mutator.get_indices[i], new_node.body[0])

insertionVisitor().visit(parent_node)
candInsertNodes = insertionVisitor.handleLst
print(candInsertNodes)
print(insertionVisitor.setBodyNodes)

# choose from elements body nodes
# choose a random body node
vesselNodes = list(insertionVisitor.setBodyNodes)
# vesselNodesDash = []
# for v in vesselNodes:
#     if (v.__class__.__name__ != "While" and v.__class__.__name__ != "If"):
#         vesselNodesDash.append(v)
# vesselNodes = vesselNodesDash
vesselNode = random.choice(vesselNodes)

candInsertNode = None
for i in range(13):
    for i in range(13): # only 3 trials :)
        candInsertNode = random.choice(candInsertNodes)
        if (candInsertNode.__class__.__name__ != "While" and candInsertNode.__class__.__name__ != "If"):
            break
    # print(k)

    # choose a random line in the vessel to insert your new code into
    indexBody = random.randint(0, len(vesselNode.body) - 1)
    if vesselNode.parent == candInsertNode or vesselNode is candInsertNode:
        continue
    print(vesselNode.__class__.__name__)
    print(candInsertNode.__class__.__name__)
    try:
        vesselNode.body.insert(indexBody, candInsertNode)
        ast.fix_missing_locations(candInsertNode)
        print(ast.unparse(parent_node))

    except Exception as e:
        # print(ast.dump(parent_node, indent=4))
        print(e)
        break
    except:
        print("Error")
        break

print("Finished!!!!!!!!!!!!!!!!!!!!!")
# print(ast.dump(parent_node, indent=4))
# print('------------------------------------')
# print(ast.unparse(parent_node))
# print('------------------------------------')


