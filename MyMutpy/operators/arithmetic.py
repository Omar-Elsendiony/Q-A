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
import copy

from sympy import false


    # ArithmeticOperatorDeletion,
    # ArithmeticOperatorReplacement,
    # AssignmentOperatorReplacement

class ArithmeticOperator(ast.NodeTransformer):
    """
    Base Class for all arithmetic operators
    Inherits from Node transformer
    """
    mutatedSet = set()  # set of ast nodes that were mutated
    OPERATORS = {'ADD', 'SUB'}
    def __init__(self, target_node_lineno = None, code=None, target_node_col_offset=None):
        self.target_node_lineno = target_node_lineno
        self.node = code
        self.target_node_col_offset= target_node_col_offset
        self.finishedMutation = False
    
    def generic_visit(self, node):
        for field, old_value in ast.iter_fields(node):
            if isinstance(old_value, list):
                new_values = []
                for value in old_value:
                    if isinstance(value, ast.AST):
                        value = self.visit(value)
                        if value is None:
                            continue
                        elif not isinstance(value, ast.AST):
                            new_values.extend(value)
                            continue
                    new_values.append(value)
                old_value[:] = new_values
            elif isinstance(old_value, ast.AST):
                new_node = self.visit(old_value)
                if new_node is None:
                    delattr(node, field)
                else:
                    setattr(node, field, new_node)
        return node
    def visit(self, node):
        """Visit a node."""
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        if (visitor != self.generic_visit and not self.finishedMutation): # this means that the mutation has already been done
            print("The mutation has already been done")
            copied = copy.copy(node)
            return visitor(node)
        if (self.finishedMutation): # this means that the mutation has already been done
            return node
        return visitor(node)

    @classmethod
    def name(cls):
        return 'AR' # aRITHMETIC SHORT FORM

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

    def __init__(self, target_node_lineno = None, code=None, target_node_col_offset=None, operator = 'ADD'):
        super().__init__(target_node_lineno, code, target_node_col_offset)
        self.operator = operator
    def visitC(self):
        """
        
        This method is responsible for performing an intermediate visit on a node.
        
        Returns:
            The result of the visit on the copied node.
        """
        node = self.node
        node = copy.copy(node)

        # if getattr(node, 'parent', None):
        #     node = copy.copy(node)
        #     if hasattr(node, 'lineno'):
        #         del node.lineno
        # node.parent = getattr(self, 'parent', None)
        # node.children = []
        # self.parent = node
        result_node = self.visit(node)
        # self.parent = node.parent
        # if self.parent:
        #     self.parent.children += [node] + node.children
        return result_node
    
    def visit_BinOp(self, node):
        """
        function targets the addition and subtraction operators that are considered infix operators
        """
        if node.lineno == self.target_node_lineno :
            self.finishedMutation = True
            print("The End", node.lineno)
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
        return 'ARR' # Arithmetic replacement short form



class UnaryOperator(ast.NodeTransformer):

    pass
    
