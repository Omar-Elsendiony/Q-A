import ast
from .base import baseOperator
from typing import Any
import random

class FunctionArgumentReplacement(baseOperator):

    def visit_Name(self, node):
        if (node.id in self.get_functionIdentifiers()):   
            if (self.wanted_line(node.lineno)):
                if (node.parent.__class__.__name__ == "Call" and node.parent.func.id != node.id) or node.parent.__class__.__name__ == "Tuple":
                    self.finishedMutation = True
                    return ast.BinOp(left=ast.Name(id=node.id, ctx=ast.Load()), op=ast.Sub(), right=ast.Constant(value=1))
        # else:
        return node
    
    @classmethod
    def name(cls):
        return 'FAR'  # Function Argument Replacement


class IdentifierReplacement(baseOperator):
        def visit_Name(self, node):
            id = self.get_identifiers()
            if node.id in id:
                if self.wanted_line(node.lineno):
                        # self.mutatedSet.add(node)
                        selectedIdentifier = random.choice(self.identifiers)
                        numRepeat = 0
                        while(selectedIdentifier == node.id and len(self.identifiers) > 1 and numRepeat < 2):
                            selectedIdentifier = random.choice(self.identifiers)
                            numRepeat += 1
                        node.id = selectedIdentifier
                        # print(node.id)
                        self.finishedMutation = True
            return node

        @classmethod
        def name(cls):
            return 'IDR'
