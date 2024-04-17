import ast
import random


class baseOperator(ast.NodeVisitor):
    mutatedSet = set()  # set of ast nodes that were mutated

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
        # try:
        #     print(node.lineno)
        # except:
        #     pass
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
        # random.randint(5, 15) % 2
        choice = random.choice(listChoices)
        # choice = listChoices[random.randint(0, 50) % 2]
        return choice


