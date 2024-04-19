"""
Module : main
The main pipeline resides here

"""

import ast
import re
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

def editFreq(cand):
    pass

def testCasesPassed(candidate:str, inputs:List, outputs:List) -> int:
    """
    based on the number of test cases passed, we can determine the fitness of the candidate
    """
    pass

def passesNegTests(program:str, program_name:str, inputs:List, outputs:List) -> bool:
    """
    Inputs:
    program : str :  program to be tested
    inputs : List :  inputs to the program
    outputs : List :  outputs of the program
    """
    # let's try by capturing the name of the function in regex and the list of names is compared with the name of the function
    function_names = re.findall(r'def\s+(\w+)', program)
    for name in function_names:
        if name == program_name:
            editedProgram = re.sub(r'$', f'\nres = {program_name}', program)
            print(editedProgram)
            break
    
    # this loop is wrong as the return of exec is binary not the expected output of the program
    for i in range(len(inputs)):
        if exec(program, globals(), locals()) != outputs[i]:
            return False
    return True


def selectPool(candidates:Set, inputs:List, outputs:List) -> Set:
    pass

def selectPool(candidates:Set) -> Set:
    pass

def mutate(cand:str, ops:Callable):  # helper function to mutate the code
    splitted_cand = cand.split('\n')
    faultyLineLocations = range(1, len(splitted_cand) + 1)

    ## for the future ##
    ## we check if the line still exists or not, so that we can mutate it
    ## we will send the column offset but after making sure that the line exists
    locs = random.choices(faultyLineLocations, k=1)
    pool = set()
    cand_dash = None
    for f in locs:
        op_f = ops(f)
        op_f = (random.choices(op_f, k=1)[0])
        copied_cand = copier.visit(cand)
        cand_dash = op_f(target_node_lineno = f, code_ast = copied_cand).visitC()
        pool.add(cand_dash)
        cand = copied_cand
    selectPool(pool)

def mutate_2(cand:str, ops:Callable, inputs: List, outputs:List):  # helper function to mutate the code
    splitted_cand = cand.split('\n')
    faultyLineLocations = range(1, len(splitted_cand) + 1)

    ## for the future ##
    ## we check if the line still exists or not, so that we can mutate it
    ## we will send the column offset but after making sure that the line exists
    locs = random.choices(faultyLineLocations, k=1)
    pool = set()
    cand_dash = None
    for f in locs:
        op_f = ops(f)
        op_f = (random.choices(op_f, k=1)[0])
        copied_cand = copier.visit(cand)
        cand_dash = op_f(target_node_lineno = f, code_ast = copied_cand).visitC()
        pool.add(cand_dash)
        cand = copied_cand
    selectPool(pool, inputs, outputs)



def main(BugProgram:str, MethodUnderTestName:str, FaultLocations:List, inputs:List, outputs:List, FixPar:Callable, ops:Callable,
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
    while len(Solutions) < M and number_of_iterations < 10:
        for p in Pop:
            if p not in Solutions:
                if passesNegTests(p, inputs, outputs):
                    Solutions.append(p)
                else:
                    Pop.remove(p) # remove p from the population to be inserted again after mutation
                    Pop.append(mutate(ops))


if __name__ == '__main__':
    ops = utils.mutationsCanBeApplied
    with open('BuggyProgram.txt', 'r') as file:
        buggyProgram = file.read()
    with open('MethodUnderTestName.txt', 'r') as file:
        methodUnderTestName = file.read()
    with open('inputs.txt', 'r') as file:
        while (inputs := file.readline()):
            inputs = file.readline()
        # inputs = file.readline()

# codeLines = code.split('\n')
# codeLineslst = [] # temporary list to store the code lines
# codeLinesset = set() # temporary set to store the code lines
# print(codeLines) # print the code lines which are a list lines after being split by '\n'
# for line in codeLines:
#     codeLineslstX , codeLinessetX, offsets = utils.segmentLine(line) # any variable appended by X is temporary
#     # assume know we are going to mutate the code line by line
#     print(len(codeLineslstX), len(codeLinessetX), len(offsets))
#     print(codeLineslstX)
#     print(offsets)
#     lstMutations, weights = utils.mutationsCanBeApplied(codeLinessetX)
#     if not lstMutations: # check list is empty or not
#         continue
#     choice = random.choices(lstMutations, weights = weights, k=1)[0] # random.choice returns a list, its size determined by k
#     i = 1
#     line_ast = ast.parse(line)
#     if (type(choice) is tuple):
#         opCode = choice[0]
#         operator = choice[1]
#         op = name_to_operator[opCode]
#         lineParsedOriginal = copier.visit(line_ast)
#         mutant = op(target_node_lineno = i, code_ast = line_ast, operator = operator).visitC()
#         mutant = ast.fix_missing_locations(mutant) # after mutation, we need to fix the missing locations
#         print("**********************************")
#         print(unparseAST.to_source(mutant))
#         print("**********************************")
#     else:
#         op = name_to_operator[choice]
#         lineParsedOriginal = copier.visit(line_ast)
#         line_ast = ast.parse(line)
#         mutant = op(target_node_lineno = i, code_ast = line_ast).visitC()
#         mutant = ast.fix_missing_locations(mutant) # after mutation, we need to fix the missing locations
#         print("**********************************")
#         print(unparseAST.to_source(mutant))
#         print("**********************************")
    # i+=1




