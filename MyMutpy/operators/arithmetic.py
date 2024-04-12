import ast
import copy


    # ArithmeticOperatorDeletion,
    # ArithmeticOperatorReplacement,
    # AssignmentOperatorReplacement

class ArithmeticOperator(ast.NodeTransformer):
    mutatedSet = set()  # set of ast nodes that were mutated
    OPERATORS = {'ADD', 'SUB', 'MUL', 'DIV', 'MOD'}
    def __init__(self, target_node_lineno = None, code=None, target_node_col_offset=None):
        self.target_node_lineno = target_node_lineno
        self.node = code
        self.target_node_col_offset= target_node_col_offset

    @classmethod
    def name(cls):
        return 'AR' # aRITHMETIC SHORT FORM

class ArithmeticOperatorDeletion(ArithmeticOperator):
    def get_operator_type(self):
        return ast.UAdd, ast.USub

    def visit_UnaryOp(self, node):
        if isinstance(node.op, self.get_operator_type()):
            return node.operand
        return self.generic_visit(node)
    
    @classmethod
    def name(cls):
        return 'ARD' # aRITHMETIC SHORT FORM for deletion

class ArithmeticOperatorReplacement(ArithmeticOperator):

    def __init__(self, target_node_lineno = None, code=None, target_node_col_offset=None, operator = 'ADD'):
        super().__init__(target_node_lineno, code, target_node_col_offset)
        self.operator = operator
    def visitC(self):
        """
        Intermediate visit that takes care of copying the node and setting the parent attribute
        
        This method is responsible for performing an intermediate visit on a node. It copies the node, removes the 'lineno' attribute if present, sets the parent attribute, and initializes the children list. It then calls the `visit` method to perform the actual visit on the copied node. After the visit, it updates the parent and children attributes of the copied node and returns the result of the visit.
        
        Returns:
            The result of the visit on the copied node.
        """
        node = self.node
        if getattr(node, 'parent', None):
            node = copy.copy(node)
            if hasattr(node, 'lineno'):
                del node.lineno
        node.parent = getattr(self, 'parent', None)
        node.children = []
        self.parent = node
        result_node = self.visit(node)
        self.parent = node.parent
        if self.parent:
            self.parent.children += [node] + node.children
        return result_node
    
    def visit_BinOp(self, node):
        if node.lineno == self.target_node_lineno and node not in self.mutatedSet:
            print("Mutating BinOp at line: ", node.lineno)
            self.mutatedSet.add(node)

            return ast.BinOp(left=self.visit(node.left), op=ast.Sub(), right=self.visit(node.right))
        else:
            return self.generic_visit(node)

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
        return 'ARR' # aRITHMETIC SHORT FORM

    
