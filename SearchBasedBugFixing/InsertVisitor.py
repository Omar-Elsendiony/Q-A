import ast
import random
from utils import parentify


def isInBody(node):
    for child in node.parent.body:
        if (child is node):
            return True
    return False


class InsertionVisitor(ast.NodeVisitor):
    countNodes = 0
    handleLst = [] # handles for candidates that can be inserted in the body of the parent node
    setBodyNodes = set()  # set of nodes that can be the vessel for another statements
    def visit(self, node):
        if (hasattr(node.parent, 'body') and node.__class__.__name__ != "Compare" and node.__class__.__name__ != "arguments" and node.__class__.__name__ != "FunctionDef" and node.parent.__class__.__name__ != "FunctionDef" and node.__class__.__name__ != "Name"):  # check if it falls directly under a node that has body attr that can encompass it
            if (isInBody(node)):
                self.setBodyNodes.add(node.parent)
                self.handleLst.append(node)
        return super().visit(node)


def insertNode(parent_node):
    parentify(parent_node)
    InsertionVisitor().visit(parent_node)
    candInsertNodes = InsertionVisitor.handleLst
    # print(candInsertNodes)
    vesselNodes = list(InsertionVisitor.setBodyNodes)
    if (len(vesselNodes) == 0): # more verbose than the previous
        return

    try:
        vesselNode = random.choice(vesselNodes)
    except:
        return
        # print(ast.unparse(parent_node))
        # print("No vessel node found")
    candInsertNode = None
    for j in range(5): # only 5 trials :)
        candInsertNode = random.choice(candInsertNodes)
        if (candInsertNode.__class__.__name__ != "While" and candInsertNode.__class__.__name__ != "If"):
            break

    # choose a random line in the vessel to insert your new code into
    indexBody = random.randint(0, len(vesselNode.body) - 1)
    vesselNode.body.insert(indexBody, candInsertNode)

    return
        
