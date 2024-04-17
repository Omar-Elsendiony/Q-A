import ast
from .base import baseOperator


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
    def visit_If(self, node):
        if not self.wanted_line(node.lineno, node.col_offset):
            return node
        # remove the second branch of the if statement
        # node.orelse = []
        return None

    def visit_While(self, node):
        if not self.wanted_line(node.lineno, node.col_offset):
            return node
        return None

    def visit_For(self, node):
        if not self.wanted_line(node.lineno, node.col_offset):
            return node
        return None

    @classmethod
    def name(cls):
        return 'STD'  # Statement Deletion