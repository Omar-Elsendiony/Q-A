import ast
from .base import baseOperator
from typing import Any

class BreakContinueReplacement(baseOperator):
    def visit_Break(self, node):
        if not self.wanted_line(node.lineno, node.col_offset):
            return node
        return ast.Continue()

    def visit_Continue(self, node):
        if not self.wanted_line(node.lineno, node.col_offset):
            return node
        return ast.Break()


    @classmethod
    def name(cls):
        return 'BCR'  # Break Continue Replacement


class SliceIndexRemove(baseOperator):

    def mutate_Slice_remove_lower(self, node):
        return ast.Slice(lower=None, upper=node.upper, step=node.step)

    def mutate_Slice_remove_upper(self, node):
        return ast.Slice(lower=node.lower, upper=None, step=node.step)

    def mutate_Slice_remove_step(self, node):


        return ast.Slice(lower=node.lower, upper=node.upper, step=None)
    
    def visit_Slice(self, node):
        if not self.wanted_line(node.lineno, node.col_offset):
            return node
        func = self.choose_mutation_random_dist(self.mutate_Slice_remove_lower, self.mutate_Slice_remove_upper, self.mutate_Slice_remove_step)
        return func(node)

    @classmethod
    def name(cls):
        return 'SIR'  # Slice Index Remove
    
class StatementDeletion(baseOperator):
    """
    Delete 
    """
    def visit_If(self, node):
        if not self.wanted_line(node.lineno, node.col_offset):
            return node
        # remove the second branch of the if statement
        # node.orelse = []
        return None


    @classmethod
    def name(cls):
        return 'STD'  # Statement Deletion


class MembershipReplacement(baseOperator):
    """
    Membership replacement for the members: 
    is
    is not
    in
    not in
    """
    def visit_In(self, node: ast.In) -> Any:
        if not self.wanted_line(node.lineno, node.col_offset):
            return node
        return ast.NotIn()

    def visit_Is(self, node: ast.Is) -> Any:
        if not self.wanted_line(node.lineno, node.col_offset):
            return node
        return ast.IsNot()

    def visit_IsNot(self, node: ast.IsNot):
        if not self.wanted_line(node.lineno, node.col_offset):
            return node
        return ast.Is()

    def visit_NotIn(self, node: ast.NotIn):
        if not self.wanted_line(node.lineno, node.col_offset):
            return node
        return ast.In()


    @classmethod
    def name(cls):
        return 'MER'  # Statement Deletion

class ConstantReplacement(baseOperator):

    def is_docstring(node):
        def_node = node.parent.parent
        return (isinstance(def_node, (ast.FunctionDef, ast.ClassDef, ast.Module)) and def_node.body and
                isinstance(def_node.body[0], ast.Expr) and isinstance(def_node.body[0].value, ast.Str) and
                def_node.body[0].value == node)

    def mutate_Num_zero(self, node):
        if not node.n:
            raise node

        return ast.Num(n=0)
    
    def mutate_Num_one(self, node):
        if not node.n:
            raise node

        return ast.Num(n=1)
    
    def mutate_Num_minus_one(self, node):
        if not node.n:
            raise node

        return ast.Num(n=-1)


    def mutate_Num_empty(self, node):
        if not node.n:
            raise node

        return ast.Num(n=0)
    

    def mutate_Str_empty(self, node):
        if not node.s or self.is_docstring(node):
            raise node

        return ast.Str(s='')