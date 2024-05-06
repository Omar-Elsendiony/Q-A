import astunparse
import ast
code = """
x = 2
print()
if x == 2:
    if x != 5:
        pass
    y = 2
    for i in range(10):
        print(i)
        if i == 5:
            break
else:
    print("x is not 2")
    y = 3
"""
code_ast = ast.parse(code)

# print(ast.dump(code_ast, indent = 4))


class kimoMutator(ast.NodeVisitor):

    def __init__(self):
        self.parents = []
        self.indices = []
        self.target_line_no = None

    def store_parent(self, index, parent):
        self.parents.append(parent)
        self.indices.append(index)

    def set_line_no(self, linenumbers):
        self.target_line_numbers = linenumbers

    @property
    def get_indices(self):
        return self.indices

    @property
    def get_parents(self):
        return self.parents

    def visit_If(self, node):
        x = node.parent
        # new_node = ast.parse("print('hello')")
        if (node.lineno in self.target_line_numbers):
            for i, nodeParent in enumerate(node.parent.body):
                # node.parent.body
                if (nodeParent is node):
                    # print("OK")
                    self.store_parent(i, node.parent)

                    # x.append(new_node)
                    # node._fields = node._fields + ("test",)
                    # setattr(node, "body", x)
                    # node.parent.body.insert(i - 1, ast.parse("print('hello')"))

            # print(node)
        return self.generic_visit(node)
    
def parentify(tree):
    tree.parent = None
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node

parentify(code_ast)
mutator = kimoMutator()
new_node = ast.parse("print('hello')\n")
lineNos = {4, 5, 10}
mutator.set_line_no(lineNos)
##############################################################


mutator.visit(code_ast)
# mutator.parent.body.insert(mutator.index, new_node)
# print(mutator.parent.body)
# print(astunparse.to_source(code_ast))


for i, parent in enumerate(mutator.get_parents):
    parent.body.insert(mutator.get_indices[i], new_node.body[0])
    ast.fix_missing_locations(code_ast)
    # break


ast.fix_missing_locations(code_ast)
print(ast.unparse(code_ast))
