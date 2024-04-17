
import ast
from .base import baseOperator


class ConditionalOperatorInsertion(baseOperator):
    """
    Class that is very unique to the project.
    it negates the condition of the target node
    The negation is in the relational operator
    """
    def negate_test(self, node):
        not_node = ast.UnaryOp(op=ast.Not(), operand=node.test)
        node.test = not_node
        return node

    def mutate_While(self, node):
        if (node.lineno != self.target_node_lineno):
            return node
        return self.negate_test(node)

    def mutate_If(self, node):
        if (node.lineno != self.target_node_lineno):
            return node
        return self.negate_test(node)

    # def mutate_In(self, node):
    #     if (node.lineno != self.target_node_lineno):
    #         return node
    #     return ast.NotIn()

    # def mutate_NotIn(self, node):
    #     if (node.lineno != self.target_node_lineno):
    #         return node
    #     return ast.In()
    
    @classmethod
    def name(cls):
        return 'COI'  # Conditional Operator Insertion