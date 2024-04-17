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
import base

class LogicalOperator(base.baseOperator):
    """
    LogicalOperator: Class meant to mutate logical operators
    """
    def __init__(self, target_node_lineno = None, code_ast = None, target_node_col_offset=None):
        super().__init__(target_node_lineno, code_ast, target_node_col_offset)

    @classmethod
    def class_name(cls):
        return 'LO'  # Logical Operator

class LTE(LogicalOperator):
    """
    LTE: Class meant to mutate less than or equal to
    """
    def visit_Compare(self, node):
        """
        Visit a Compare node
        """
        if node.ops[0] == ast.LtE():
            node.ops[0] = ast.Lt()
        return node