import ast
from .base import baseOperator
from typing import Any
import random

class FunctionArgumentReplacement(baseOperator):

    def visit_Name(self, node):
        if not (hasattr(node, 'parent')): return node
        if (node.parent.__class__.__name__ == "Call"):
            # print(node.parent.func.id + "weeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
            if (node.parent.func.id == node.id): return node
            return ast.BinOp(left=ast.Name(id=node.id, ctx=ast.Load()), op=ast.Sub(), right=ast.Constant(value=1))
        else:
            return node
    
    @classmethod
    def name(cls):
        return 'FAR'  # Function Argument Replacement


class IdentifierReplacement(baseOperator):
        def visit_Name(self, node):
            if self.wanted_line(node.lineno):
                l = self.get_identifiers()
                # print(l)
                if node.id in self.get_identifiers():
                    # self.mutatedSet.add(node)
                    selectedIdentifier = random.choice(self.identifiers)
                    while(selectedIdentifier == node.id and len(self.identifiers) > 1):
                        selectedIdentifier = random.choice(self.identifiers)
                    node.id = selectedIdentifier
                    # print(node.id)
                    self.finishedMutation = True
            return node

        @classmethod
        def name(cls):
            return 'IDR'
