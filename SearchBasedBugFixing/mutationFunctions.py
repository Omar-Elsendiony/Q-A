import ast
import utils
import operators
import random
import InsertVisitor
from operators.copyAST import *

def update(cand, faultyLineLocations, weightsFaultyLineLocations, ops, name_to_operator, pool):
    copier = copyMutation()
    splitted_cand = cand.split('\n')
    # faultyLineLocations = list(range(len(splitted_cand)))

    ## for the future ##
    ## we check if the line still exists or not, so that we can mutate it
    ## we will send the column offset but after making sure that the line exists
    locs = random.choices(faultyLineLocations, weights = weightsFaultyLineLocations, k=3)

    cand_dash = None
    cand_ast = ast.parse(cand)
    cand_ast.type_ignores = []
    # op_f = None
    for f in locs:
        try:
            tokenList, tokenSet, offsets = utils.segmentLine(splitted_cand[f])
        except:
            continue
        op_f_list, op_f_weights = ops(tokenSet)
        if (op_f_list == []):
            continue
        op_f = random.choices(op_f_list,weights=op_f_weights, k=1)[0]
        copied_cand = copier.visit(cand_ast)
        copied_cand.type_ignores = []
        operator = name_to_operator[op_f]
        cand_dash = operator(target_node_lineno = f + 1, code_ast = cand_ast).visitC() # f + 1 because the line number starts from 1
        ast.fix_missing_locations(cand_dash)
        pool.add(cand_dash)
        # print(ast.dump(cand_dash, indent=4))
        cand_dash.type_ignores = []
        # print("**********************************")
        # print(op_f)
        # print(ast.unparse(cand_dash))
        cand = copied_cand
        # print(ast.unparse(cand))
        # print("**********************************")

def insert(cand:str, pool:set):  # helper function to mutate the code
    # insert will be updated once more to add in certain locations
    cand_ast = ast.parse(cand)
    cand_ast.type_ignores = []
    InsertVisitor.insertNode(cand_ast)
    # print(ast.unparse(cand_ast))
    pool.add(cand_ast)
    cand_ast.type_ignores = []
    return
