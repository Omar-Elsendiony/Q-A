import ast
import random


class baseOperator(ast.NodeVisitor):
    mutatedSet = set()  # set of ast nodes that were mutated
    identifiers = []  # list of identifiers in the code
    maxRand = 100  # maximum random number


    @classmethod
    def set_identifiers(cls, identifiers):
        cls.identifiers = identifiers

    @classmethod
    def get_identifiers(cls):
        return cls.identifiers


    def __init__(self, target_node_lineno = None, code_ast = None, target_node_col_offset=None):
        self.target_node_lineno = target_node_lineno
        self.node = code_ast
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
    

    def visitC(self):
        """
        This method is responsible for performing an intermediate visit on a node.
        
        Returns:
            The result of the visit on the copied node.
        """
        node = self.node
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

    def visit(self, node):
        """Visit a node."""
        # if isinstance(node, list): node = node[0] # as it will be a list with first element only
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        if (visitor != self.generic_visit and not self.finishedMutation): # this means that the mutation has already been done
            return visitor(node)
        if (self.finishedMutation): # this means that the mutation has already been done
            return node
        return visitor(node)

    def choose_mutation_random_dist(self, listChoices):
        """
        This method is responsible for choosing the mutation to be performed on the node.
        It is called by the visit method.
        """
        choice = random.choice(listChoices)
        return choice


    def wanted_line(self, line_no, col_offset):
        """
        This method is responsible for checking if the current line is the line we want to mutate.
        """
        if line_no == self.target_node_lineno:
            return True
        return False

    def visit_Name(self, node):
        # generate a random number and according you will replace the node identifier with another in the identifiers list
        gen = random.randint(0, self.maxRand) / self.maxRand
        if (gen < 0.7):
            return node
        

        if self.wanted_line(node.lineno, node.col_offset):
            if node.id in self.identifiers:
                # print("OKKKKKKKKKKKKKKKKK")
                self.mutatedSet.add(node)
                # print(node.id)

                selectedIdentifier = random.choice(self.identifiers)
                while(selectedIdentifier == node.id and len(self.identifiers) > 1):
                    selectedIdentifier = random.choice(self.identifiers)
                node.id = selectedIdentifier
                # print(node.id)
                # self.finishedMutation = True # no this is not the intended mutation
        return node
