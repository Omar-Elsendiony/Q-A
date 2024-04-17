"""
Module : main
The main pipeline resides here

"""


import ast

from numpy import number
from sqlalchemy import func
from operators import *
import operators
import unparseAST
import utils
import time
import random
from typing import List, Set, Callable


copier = copyMutation()
def getNameToOperatorMap(self):
    name_to_operator = utils.build_name_to_operator_map()
    return name_to_operator

name_to_operator = getNameToOperatorMap(operators)


import time
start = time.time()
code = """
i = 1 == 2"""

def mutate():  # helper function to mutate the code
    pass

def passesNegTests(program:str, inputs:List, outputs:List) -> bool:
    """
    Inputs:
    program : str :  program to be tested
    inputs : List :  inputs to the program
    outputs : List :  outputs of the program
    """
    # for i in range(len(inputs)):
    #     if eval(program
    return True

def main(BugProgram:str, FaultLocations:List, inputs:List, outputs:List, FixPar:Callable, ops:Callable,
         popSize = 4, M = 4, E:int = 5, L:int = 5):
    """
    Inputs:
    BugProgram : str :  buggy program
    FaultLocations : List : the locations of the fault
    inputs : List :  inputs to the program
    outputs : List :  outputs of the program
    FixPar : Callable : distribution sampled from when comparing with history fix
    ops : Callable : operations that can be applied for the given fault location
    popSize : int :  population size
    M : int :  number of desired solutions that serves as the upper limit
    E : int :  number of seeded candidates to the initial population
    L: int: number of locations considered in the mutation step
    """
    Solutions = set() # set of solutions
    Pop = []  # population
    for i in range(E):  # E number must be less than or equal to the population size
        Pop.append(BugProgram)  # seeding the population with candidates that were not exposed to mutation
    
    while len(Pop) < popSize:
        Pop.append(mutate())  # mutate the population
    
    number_of_iterations = 0
    while len(Solutions) < M and number_of_iterations < 1000:
        for p in Pop:
            if p not in Solutions:
                if passesNegTests(p, inputs, outputs):
                    Solutions.append(p)
                else:
                    Pop.remove(p) # remove p from the population to be inserted again after mutation
                    Pop.append(mutate())


if __name__ == '__main__':
    ops = utils.mutationsCanBeApplied


codeLines = code.split('\n')
codeLineslst = [] # temporary list to store the code lines
codeLinesset = set() # temporary set to store the code lines
print(codeLines) # print the code lines which are a list lines after being split by '\n'
for line in codeLines:
    codeLineslstX , codeLinessetX, offsets = utils.segmentLine(line) # any variable appended by X is temporary
    # assume know we are going to mutate the code line by line
    print(len(codeLineslstX), len(codeLinessetX), len(offsets))
    print(codeLineslstX)
    print(offsets)
    lstMutations, weights = utils.mutationsCanBeApplied(codeLinessetX)
    if not lstMutations: # check list is empty or not
        continue
    choice = random.choices(lstMutations, weights = weights, k=1)[0] # random.choice returns a list, its size determined by k
    i = 1
    line_ast = ast.parse(line)
    if (type(choice) is tuple):
        opCode = choice[0]
        operator = choice[1]
        op = name_to_operator[opCode]
        lineParsedOriginal = copier.visit(line_ast)
        mutant = op(target_node_lineno = i, code_ast = line_ast, operator = operator).visitC()
        mutant = ast.fix_missing_locations(mutant) # after mutation, we need to fix the missing locations
        print("**********************************")
        print(unparseAST.to_source(mutant))
        print("**********************************")
    else:
        op = name_to_operator[choice]
        lineParsedOriginal = copier.visit(line_ast)
        line_ast = ast.parse(line)
        mutant = op(target_node_lineno = i, code_ast = line_ast).visitC()
        mutant = ast.fix_missing_locations(mutant) # after mutation, we need to fix the missing locations
        print("**********************************")
        print(unparseAST.to_source(mutant))
        print("**********************************")
    # i+=1



faultyLineLocations = [1]
# for l in faultyLineLocations:
    # print(l)


lstMutations, weights = utils.mutationsCanBeApplied(codeLinesset)
# print(lstMutations)


ast_node = ast.parse(code)
# print(unparseAST.to_source(ast_node))
copied = copyMutation().visit(ast_node)
# copy.deepcopy(ast_node)
mutant = (AdditionOperatorReplacement(target_node_lineno = 1, code_ast = ast_node)).visitC()
mutant = ast.fix_missing_locations(mutant) # after mutation, we need to fix the missing locations
# mutant = (BinaryOperatorReplacement(target_node_lineno= 1, code = mutant, operator='SUB')).visitC()
# print(ast.dump(mutant, indent=4))
# ast_node = copyMutation().visit(copied)
span = time.time() - start
print(span)
# print(ast_node is copied)
# print(unparseAST.to_source(copied))
# print(unparseAST.to_source(line_ast))


# again = ArithmeticOperatorReplacement.printMutatedSet()
