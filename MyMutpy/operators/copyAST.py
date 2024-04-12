import ast

class copyMutate(ast.NodeTransformer):

    def visit_Module(self, node):
        return ast.copy_location(ast.Module(body=[self.visit(x) for x in node.body]), node)

    def visit_Num(self, node):
        return ast.copy_location(ast.Constant(n=node.n), node)
    
    def visit_Constant(self, node):
        return ast.copy_location(ast.Constant(n=node.n), node)

    def visit_Str(self, node):
        return ast.copy_location(ast.Constant(s=node.s), node)

    def visit_Name(self, node):
        return ast.copy_location(ast.Name(id=node.id, ctx=node.ctx), node)

    def visit_List(self, node):
        return ast.copy_location(ast.List(elts=[self.visit(x) for x in node.elts], ctx=node.ctx), node)

    def visit_Tuple(self, node):
        return ast.copy_location(ast.Tuple(elts=[self.visit(x) for x in node.elts], ctx=node.ctx), node)

    def visit_Set(self, node):
        return ast.copy_location(ast.Set(elts=[self.visit(x) for x in node.elts], ctx=node.ctx), node)

    def visit_Dict(self, node):
        return ast.copy_location(ast.Dict(keys=[self.visit(x) for x in node.keys], values=[self.visit(x) for x in node.values]), node)

    def visit_Attribute(self, node):
        return ast.copy_location(ast.Attribute(value=self.visit(node.value), attr=node.attr+"1", ctx=node.ctx), node)

    def visit_Subscript(self, node):
        return ast.copy_location(ast.Subscript(value=self.visit(node.value), slice=self.visit(node.slice), ctx=node.ctx), node)

    def visit_Index(self, node):
        return ast.copy_location(ast.Index(value=self.visit(node.value)), node)

    def visit_Slice(self, node):
        return ast.copy_location(ast.Slice(lower=self.visit(node.lower), upper=self.visit(node.upper), step=self.visit(node.step)), node)

    def visit_ExtSlice(self, node):
        return ast.copy_location(ast.ExtSlice(dims=[self.visit(x) for x in node.dims]), node)

    def visit_IfExp(self, node):
        return ast.copy_location(ast.IfExp(test=self.visit(node.test), body=self.visit(node.body), orelse=self.visit(node.orelse)), node)

    def visit_Compare(self, node):
        return ast.copy_location(ast.Compare(left=self.visit(node.left), ops=node.ops, comparators=[self.visit(x) for x in node.comparators]), node)

    def visit_Call(self, node):
        return ast.copy_location(ast.Call(func=self.visit(node.func), args=[self.visit(x) for x in node.args], keywords=[self.visit(x) for x in node.keywords]), node)
    def visit_keyword(self, node):
        return ast.copy_location(ast.keyword(arg=node.arg, value=self.visit(node.value)), node)
    def visit_Starred(self, node):
        return ast.copy_location(ast.Starred(value=self.visit(node.value), ctx=node.ctx), node)
    
    def visit_NameConstant(self, node):
        return ast.copy_location(ast.NameConstant(value=node.value), node)
    
    def visit_UnaryOp(self, node):
        return ast.copy_location(ast.UnaryOp(op=node.op, operand=self.visit(node.operand)), node)
    
    def visit_BinOp(self, node):
        return ast.copy_location(ast.BinOp(left=self.visit(node.left), op=node.op, right=self.visit(node.right)), node)
    
    def visit_BoolOp(self, node):
        return ast.copy_location(ast.BoolOp(op=node.op, values=[self.visit(x) for x in node.values]), node)
    
    def visit_If(self, node):
        return ast.copy_location(ast.If(test=self.visit(node.test), body=[self.visit(x) for x in node.body], orelse=[self.visit(x) for x in node.orelse]), node)
    
    def visit_For(self, node):
        return ast.copy_location(ast.For(target=self.visit(node.target), iter=self.visit(node.iter), body=[self.visit(x) for x in node.body], orelse=[self.visit(x) for x in node.orelse]), node)
    
    def visit_While(self, node):
        return ast.copy_location(ast.While(test=self.visit(node.test), body=[self.visit(x) for x in node.body], orelse=[self.visit(x) for x in node.orelse]), node)
    
    def visit_With(self, node):
        return ast.copy_location(ast.With(items=[self.visit(x) for x in node.items], body=[self.visit(x) for x in node.body]), node)
    
    def visit_withitem(self, node):
        return ast.copy_location(ast.withitem(context_expr=self.visit(node.context_expr), optional_vars=self.visit(node.optional_vars)), node)
    
    def visit_FunctionDef(self, node):
        return ast.copy_location(ast.FunctionDef(name=node.name, args=self.visit(node.args), body=[self.visit(x) for x in node.body], decorator_list=[self.visit(x) for x in node.decorator_list], returns=self.visit(node.returns)), node)
    
    def visit_Lambda(self, node):
        return ast.copy_location(ast.Lambda(args=self.visit(node.args), body=self.visit(node.body)), node)
    def visit_arguments(self, node):
        return ast.copy_location(ast.arguments(posonlyargs=[self.visit(x) for x in node.posonlyargs], args=[self.visit(x) for x in node.args], vararg=self.visit(node.vararg), kwonlyargs=[self.visit(x) for x in node.kwonlyargs], kw_defaults=[self.visit(x) for x in node.kw_defaults], kwarg=self.visit(node.kwarg), defaults=[self.visit(x) for x in node.defaults]), node)
    def visit_arg(self, node):
        return ast.copy_location(ast.arg(arg=node.arg, annotation=self.visit(node.annotation)), node)
    def visit_Return(self, node):
        return ast.copy_location(ast.Return(value=self.visit(node.value)), node)
    def visit_Delete(self, node):
        return ast.copy_location(ast.Delete(targets=[self.visit(x) for x in node.targets]), node)
    def visit_Assign(self, node):
        return ast.copy_location(ast.Assign(targets=[self.visit(x) for x in node.targets], value=self.visit(node.value)), node)
    def visit_AnnAssign(self, node):
        return ast.copy_location(ast.AnnAssign(target=self.visit(node.target), annotation=self.visit(node.annotation), value=self.visit(node.value), simple=node.simple), node)
    def visit_AugAssign(self, node):
        return ast.copy_location(ast.AugAssign(target=self.visit(node.target), op=node.op, value=self.visit(node.value)), node)
    def visit_Print(self, node):
        return ast.copy_location(ast.Print(dest=self.visit(node.dest), values=[self.visit(x) for x in node.values], nl=node.nl), node)
    def visit_Raise(self, node):
        return ast.copy_location(ast.Raise(exc=self.visit(node.exc), cause=self.visit(node.cause)), node)
    def visit_Assert(self, node):
        return ast.copy_location(ast.Assert(test=self.visit(node.test), msg=self.visit(node.msg)), node)
    def visit_Import(self, node):
        return ast.copy_location(ast.Import(names=[self.visit(x) for x in node.names]), node)
    def visit_ImportFrom(self, node):
        return ast.copy_location(ast.ImportFrom(module=node.module, names=[self.visit(x) for x in node.names], level=node.level), node)
    def visit_alias(self, node):
        return ast.copy_location(ast.alias(name=node.name, asname=node.asname), node)
    def visit_Exec(self, node):
        return ast.copy_location(ast.Exec(body=self.visit(node.body), globals=self.visit(node.globals), locals=self.visit(node.locals)), node)
    def visit_Global(self, node):
        return ast.copy_location(ast.Global(names=[self.visit(x) for x in node.names]), node)
    def visit_Nonlocal(self, node):
        return ast.copy_location(ast.Nonlocal(names=[self.visit(x) for x in node.names]), node)
    def visit_Pass(self, node):
        return ast.copy_location(ast.Pass(), node)
    def visit_Break(self, node):
        return ast.copy_location(ast.Break(), node)
    def visit_Continue(self, node):
        return ast.copy_location(ast.Continue(), node)
    def visit_Try(self, node):
        return ast.copy_location(ast.Try(body=[self.visit(x) for x in node.body], handlers=[self.visit(x) for x in node.handlers], orelse=[self.visit(x) for x in node.orelse], finalbody=[self.visit(x) for x in node.finalbody]), node)
    def visit_ExceptHandler(self, node):
        return ast.copy_location(ast.ExceptHandler(type=self.visit(node.type), name=node.name, body=[self.visit(x) for x in node.body]), node)
    def visit_ClassDef(self, node):
        return ast.copy_location(ast.ClassDef(name=node.name, bases=[self.visit(x) for x in node.bases], keywords=[self.visit(x) for x in node.keywords], body=[self.visit(x) for x in node.body], decorator_list=[self.visit(x) for x in node.decorator_list]), node)
    def visit_keyword(self, node):
        return ast.copy_location(ast.keyword(arg=node.arg, value=self.visit(node.value)), node)
    
    def visit_BitAnd(self, node: ast.BitAnd):
        return ast.copy_location(ast.BitAnd(), node)
    
    def visit_BitOr(self, node: ast.BitOr):
        return ast.copy_location(ast.BitOr(), node)
    
    def visit_BitXor(self, node: ast.BitXor):
        return ast.copy_location(ast.BitXor(), node)
    
    def visit_Invert(self, node: ast.Invert):
        return ast.copy_location(ast.Invert(), node)
    
    def visit_LShift(self, node: ast.LShift):
        return ast.copy_location(ast.LShift(), node)
    
    def visit_RShift(self, node: ast.RShift):
        return ast.copy_location(ast.RShift(), node)
    
    def visit_UAdd(self, node: ast.UAdd):
        return ast.copy_location(ast.UAdd(), node)