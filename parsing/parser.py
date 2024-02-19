import ast
string = "s = 5"
x = compile(source = string, filename ="test", mode="exec", flags= ast.PyCF_ONLY_AST)
print(ast.dump(x, indent=4))  # either this 
print("+++++++++++++++++++++++++++++++++++++++")
print(ast.dump(ast.parse(string), indent = 4)) # or this