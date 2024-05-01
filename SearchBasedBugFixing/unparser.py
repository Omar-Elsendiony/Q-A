import ast

class unparser(ast._Unparser):


    def visit_Compare(self, node):
        with self.require_parens(ast._Precedence.CMP, node):
            nodeLeft = node.left if (hasattr(node, 'left')) else None
            self.set_precedence(ast._Precedence.CMP.next(), nodeLeft, *node.comparators)
            if nodeLeft: self.traverse(node.left)
            for o, e in zip(node.ops, node.comparators):
                self.write(" " + self.cmpops[o.__class__.__name__] + " ")
                self.traverse(e)
