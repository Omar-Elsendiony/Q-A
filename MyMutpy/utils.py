import ast
import copy
import re
import sys
import time
import types



def create_module(ast_node, module_name='mutant', module_dict=None):
    code = compile(ast_node, module_name, 'exec')
    module = types.ModuleType(module_name)
    module.__dict__.update(module_dict or {})
    exec(code, module.__dict__)
    return module


def notmutate(sth):
    return sth




class ParentNodeTransformer(ast.NodeTransformer):
    def visit(self, node):
        if getattr(node, 'parent', None):
            node = copy.copy(node)
            if hasattr(node, 'lineno'):
                del node.lineno
        node.parent = getattr(self, 'parent', None)
        node.children = []
        self.parent = node
        result_node = super().visit(node)
        self.parent = node.parent
        if self.parent:
            self.parent.children += [node] + node.children
        return result_node


def create_ast(code):
    return ParentNodeTransformer().visit(ast.parse(code))


def is_docstring(node):
    def_node = node.parent.parent
    return (isinstance(def_node, (ast.FunctionDef, ast.ClassDef, ast.Module)) and def_node.body and
            isinstance(def_node.body[0], ast.Expr) and isinstance(def_node.body[0].value, ast.Str) and
            def_node.body[0].value == node)




def sort_operators(operators):
    return sorted(operators, key=lambda cls: cls.name())


def f(text):
    lines = text.split('\n')[1:-1]
    indention = re.search('(\s*).*', lines[0]).group(1)
    return '\n'.join(line[len(indention):] for line in lines)
