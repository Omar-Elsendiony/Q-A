"""
Module Description:
Module entails all the classes that are involved in the mutation of arithmetic operators in the code
These includes:
- BinOp: Binary operators that are infix operators
- UnaryOp: Unary operators that are prefix operators
- Mult: Multiplication operator
- Div: Division operator
- Mod: Modulus operator
- Pow: Power operator
- LShift: Left shift operator
- RShift: Right shift operator

"""
import ast
import random # useful for choosing random mutation from a pool of applicable mutations
# import base
from .base import baseOperator

class ArithmeticOperator(baseOperator):
    """
    Base Class for all arithmetic operators
    Inherits from Node transformer
    """


    @classmethod
    def name(cls):
        return 'AR' # Arithmetic short form

class ArithmeticOperatorDeletion(ArithmeticOperator):
    def get_operator_type(self):
        return ast.UAdd, ast.USub

    def visit_UnaryOp(self, node):
        """
        Unary operators talk
        """
        if isinstance(node.op, self.get_operator_type()):
            return node.operand
        return self.generic_visit(node)
    
    @classmethod
    def name(cls):
        return 'ARD' # Arithmetic short form for deletion

class BinaryOperatorReplacement(ArithmeticOperator):

    OPERATORS = {'ADD', 'SUB'} # class Attributes

    def __init__(self, target_node_lineno = None, code=None, target_node_col_offset=None, operator = 'ADD'):
        super().__init__(target_node_lineno, code, target_node_col_offset)
        self.operator = operator


    def visit_BinOp(self, node):
        """
        function targets the addition and subtraction operators that are considered infix operators
        """
        # print(ArithmeticOperator.mutatedSet)

        if node.lineno == self.target_node_lineno :
            self.finishedMutation = True
            # print("The End", node.lineno)
            self.mutatedSet.add(node)
            if self.operator == 'ADD':
                return ast.BinOp(left=self.visit(node.left), op=ast.Sub(), right=self.visit(node.right))
            elif self.operator == 'SUB':
                return ast.BinOp(left=self.visit(node.left), op=ast.Add(), right=self.visit(node.right))
            else:
                raise ("Invalid Operator")
        else:
            return node # if you do not want to continue visiting child nodes, if not self.generic_visit(node)



    @property
    def lineno(self):
        return self.target_node_lineno

    @lineno.setter
    def lineno(self, lineno):
        self.target_node_lineno = lineno

    @classmethod
    def printMutatedSet(cls):
        print(cls.mutatedSet)

    @classmethod
    def name(cls):
        return 'Bin' # Arithmetic replacement short form



class MultiplicationOperatorReplacement(ArithmeticOperator):

    # By default it calls the __init__ method of the parent class so, it is redundant to define it again
    # and we do not want to add any logic or whatsoever to it
    mutations = [ast.Div(), ast.Pow()] # list of mutations that can be performed on the node that represents multiplication


    def visit_Mult(self, node):
        # print("Multiplication")
        lineno = getattr(node, 'lineno', None)
        if (lineno is None): parent = getattr(node, 'parent', None); lineno = getattr(parent, 'lineno', None)
        if lineno == self.target_node_lineno :
            self.finishedMutation = True
            self.mutatedSet.add(node)
            mutation = self.choose_mutation_random_dist(MultiplicationOperatorReplacement.mutations)
            return mutation
        # ast.Pow()
        else:
            return node # if you do not want to mutate this multiplication

    @classmethod
    def name(cls):
        return 'MUL' # Multiplication short form

class DivisionOperatorReplacement(ArithmeticOperator):
    mutations = [ast.Mult(), ast.FloorDiv()]

    def visit_Div(self, node):
        lineno = getattr(node, 'lineno', None)
        if (lineno is None): parent = getattr(node, 'parent', None); lineno = getattr(parent, 'lineno', None)
        if lineno == self.target_node_lineno :
            self.finishedMutation = True
            self.mutatedSet.add(node)
            mutation = self.choose_mutation_random_dist(DivisionOperatorReplacement.mutations)
            return mutation
        else:
            return node

    @classmethod
    def name(cls):
        return 'DIV' # Division short form


class FloorDivisionOperatorReplacement(ArithmeticOperator):
    mutations = [ast.Mult(), ast.Div(), ast.Mod()]

    def visit_Div(self, node):
        lineno = getattr(node, 'lineno', None)
        if (lineno is None): parent = getattr(node, 'parent', None); lineno = getattr(parent, 'lineno', None)
        if lineno == self.target_node_lineno :
            self.finishedMutation = True
            self.mutatedSet.add(node)
            mutation = self.choose_mutation_random_dist(DivisionOperatorReplacement.mutations)
            return mutation
        else:
            return node

    @classmethod
    def name(cls):
        return 'FLOORDIV' # Division short form

class ModuloOperatorReplacement(ArithmeticOperator):
    mutations = [ast.Mult(), ast.FloorDiv(), ast.Mod()]

    def visit_Div(self, node):
        lineno = getattr(node, 'lineno', None)
        if (lineno is None): parent = getattr(node, 'parent', None); lineno = getattr(parent, 'lineno', None)
        if lineno == self.target_node_lineno :
            self.finishedMutation = True
            self.mutatedSet.add(node)
            mutation = self.choose_mutation_random_dist(DivisionOperatorReplacement.mutations)
            return mutation
        else:
            return node

    @classmethod
    def name(cls):
        return 'MOD' # Division short form


class ModuloOperatorReplacement(ArithmeticOperator):
    mutations = [ast.Mult(), ast.FloorDiv(), ast.Mod()]

    def visit_Div(self, node):
        lineno = getattr(node, 'lineno', None)
        if (lineno is None): parent = getattr(node, 'parent', None); lineno = getattr(parent, 'lineno', None)
        if lineno == self.target_node_lineno :
            self.finishedMutation = True
            self.mutatedSet.add(node)
            mutation = self.choose_mutation_random_dist(DivisionOperatorReplacement.mutations)
            return mutation
        else:
            return node

    @classmethod
    def name(cls):
        return 'MOD' # Division short form

class PowerOperatorReplacement(ArithmeticOperator):
    mutations = [ast.Mult()]

    def visit_Div(self, node):
        lineno = getattr(node, 'lineno', None)
        if (lineno is None): parent = getattr(node, 'parent', None); lineno = getattr(parent, 'lineno', None)
        if lineno == self.target_node_lineno :
            self.finishedMutation = True
            self.mutatedSet.add(node)
            mutation = self.choose_mutation_random_dist(DivisionOperatorReplacement.mutations)
            return mutation
        else:
            return node

    @classmethod
    def name(cls):
        return 'POW' # Division short form

class UnaryOperator(ast.NodeTransformer):
    pass
    
