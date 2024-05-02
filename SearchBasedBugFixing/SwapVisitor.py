import ast
import random
from utils import parentify

class SwapVisitor(ast.NodeVisitor):
    countNodes = 0
    handleLst = [] # handles for candidates that can be swaped in the body of the parent node
    def visit(self, node):
        if (hasattr(node.parent, 'body') and node.__class__.__name__ != "Compare"):  # check if it falls directly under a node that has body attr that can encompass it
            self.handleLst.append(node)
        return super().visit(node)









def swapNodes(parent_node):
    parentify(parent_node)
    changed = False
    upperLimit = 10
    u = 0
    SwapVisitor().visit(parent_node)
    candidates = SwapVisitor.handleLst
    while (not changed and u < upperLimit):
        cand_dash = random.choices(candidates, k=2)
        if (cand_dash[0].parent.__class__.__name__ == cand_dash[1].parent.__class__.__name__):
            changed = True
            try:
                cand_dash[0].parent.body[cand_dash[0].parent.body.index(cand_dash[0])], cand_dash[1].parent.body[cand_dash[1].parent.body.index(cand_dash[1])] = cand_dash[1], cand_dash[0]
            except: pass
    return
        
