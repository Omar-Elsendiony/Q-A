import ast


class BinOpMutate(ast.NodeTransformer):
    def __init__(self, target_node_lineno, code = None):
        self.target_node_lineno = target_node_lineno
        self.changedAnOperator = False
        self.code = code

    def visitC(self):
        return self.visit((self.code))
    def visit_BinOp(self, node):
        if node.lineno == self.target_node_lineno and not self.changedAnOperator:  # However if two operations are on the same line, it will change both
            self.changedAnOperator = True
            return ast.BinOp(left=self.visit(node.left), op=ast.Sub(), right=self.visit(node.right))
        else:
            # If it's not the target node, continue visiting other nodes without modifications
            return self.generic_visit(node)

    
