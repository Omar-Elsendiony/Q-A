import ast

class IdentifierVisitor(ast.NodeVisitor):
    def __init__(self):
        self.assignmentIdentifiers = set()
        self.functionIdentifiers = set()
        self.unknownIdentifiers = set()

    def visit_Name(self, node):
        if isinstance(node.parent, ast.Assign):
            self.assignmentIdentifiers.add(node.id)
        elif isinstance(node.parent, ast.Call):
            self.functionIdentifiers.add(node.id)
        else:
            self.unknownIdentifiers.add(node.id)
        # self.identifiers.add(node.id)

    @property
    def get_identifiers(self):
        return self.assignmentIdentifiers |  self.unknownIdentifiers

