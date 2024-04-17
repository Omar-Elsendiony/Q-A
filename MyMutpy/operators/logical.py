"""
logical operators: Module meant to mutate logical operators
LTE: less than or equal to
GTE: greater than or equal to
LT: less than
GT: greater than
NE: not equal
EQ: equal
AND: and
OR: or
NOT: not
CR: comparison
MR: membership
"""
import ast
from .base import baseOperator

class LogicalOperator(baseOperator):
    """
    LogicalOperator: Class meant to mutate logical operators
    """
    # def __init__(self, target_node_lineno = None, code_ast = None, target_node_col_offset=None):
    #     super().__init__(target_node_lineno, code_ast, target_node_col_offset)

    @classmethod
    def name(cls):
        return 'LO'  # Logical Operator

class LogicalOperatorReplacement(LogicalOperator):
    """
    LogicalOperatorReplacement: Umbrella for all replacements of logical operators
    takes as argument the logical operator to be replaced, checks its type, based on the type of the operator,
    it will mutate based on the applicable operators.
    """
    def get_operator_type(self):
        """
        get_operator_type: Method to get the operator type
        """
        return ast.Lt, ast.Gt, ast.LtE, ast.GtE, ast.Eq, ast.NotEq, ast.And, ast.Or, ast.Not, ast.In, ast.NotIn

    def visit_Compare(self, node):
        """
        Visit a Compare node
        """
        if (node.lineno != self.target_node_lineno):
            return node

        if isinstance(node.ops[0], self.get_operator_type()):
            # mutation = self.choose_mutation_random_dist([])
            if node.ops[0] == ast.Lt():
                node.ops[0] = ast.Gt()
            elif node.ops[0] == ast.Gt():
                node.ops[0] = ast.Lt()
            elif node.ops[0] == ast.LtE():
                node.ops[0] = ast.GtE()
            elif node.ops[0] == ast.GtE():
                node.ops[0] = ast.LtE()
            elif node.ops[0] == ast.Eq():
                node.ops[0] = ast.NotEq()
            elif node.ops[0] == ast.NotEq():
                node.ops[0] = ast.Eq()
            elif node.ops[0] == ast.And():
                node.ops[0] = ast.Or()
            elif node.ops[0] == ast.Or():
                node.ops[0] = ast.And()
            elif node.ops[0] == ast.Not():
                node.ops[0] = ast.Not()
            elif node.ops[0] == ast.In():
                node.ops[0] = ast.NotIn()
            elif node.ops[0] == ast.NotIn():
                node.ops[0] = ast.In()
        return node

    @classmethod
    def name(cls):
        return 'LR'  # Logical Operator Replacement

# class LTE(LogicalOperatorReplacement):
#     """
#     LTE: Class meant to mutate less than or equal to
#     """
#     def visit_Compare(self, node):
#         """
#         Visit a Compare node
#         """
#         if node.ops[0] == ast.LtE():
#             node.ops[0] = ast.Lt()
#         return node
    
#     def name(cls):
#         return 'LTE'


# class GTE(LogicalOperatorReplacement):
#     """
#     LTE: Class meant to mutate less than or equal to
#     """
#     def visit_Compare(self, node):
#         """
#         Visit a Compare node
#         """
#         mutation = self.choose_mutation_random_dist([])
#         if node.ops[0] == ast.LtE():
#             node.ops[0] = ast.Lt()
#         return node
    
#     def name(cls):
#         return 'GTE'


# class LTE(LogicalOperator):
#     """
#     LTE: Class meant to mutate less than or equal to
#     """
#     def visit_Compare(self, node):
#         """
#         Visit a Compare node
#         """
#         if node.ops[0] == ast.LtE():
#             node.ops[0] = ast.Lt()
#         return node
#     def name(cls):
#         return 'LTE'