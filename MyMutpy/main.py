"""
Module : main
The main pipeline resides here

"""

import ast
import re
from operators import *
import operators
import utils
import random
from typing import List, Set, Callable
from runCode import runCode


copier = copyMutation()
def getNameToOperatorMap(self):
    name_to_operator = utils.build_name_to_operator_map()
    return name_to_operator


def editFreq(cand):
    ## TODO ##
    pass

def fitness_testCasesPassed(program:str, program_name:str, inputs:List, outputs:List) -> int:
    """
    Inputs:
    program : str :  program to be tested
    inputs : List :  inputs to the program
    outputs : List :  outputs of the program
    """
    # let's try by capturing the name of the function in regex and the list of names is compared with the name of the function
    editedProgram = None
    passedTests = 0
    res = None

    for i in range(len(inputs)):
        try:
            testcase = inputs[i]
            program = re.sub(f'\nres = {program_name}', f'\n\ntestcase = {testcase}\nres = {program_name}', program)
            editedProgram = re.sub(f'\nres = {program_name}', f'\nres = {program_name}()', program)
            if (globals().get('res') is not None):
                del globals()['res']
            exec(editedProgram, globals())
            if res == outputs[i]:
                passedTests += 1
        except Exception as e:
            print(e)
            # return False
    return passedTests

def passesNegTests(program:str, program_name:str, inputs:List, outputs:List) -> bool:
    """
    Inputs:
    program : str :  program to be tested
    inputs : List :  inputs to the program
    outputs : List :  outputs of the program
    """
    # let's try by capturing the name of the function in regex and the list of names is compared with the name of the function
    editedProgram = None
    res = None

    for i in range(len(inputs)):
        try:
            testcase = inputs[i]
            if (type(testcase) is not list and eval(testcase) is None):
                # program = re.sub(r'$', f'\n\ntestcase = {testcase}\nres = {program_name}()\n\nprint(res)', program)
                # if (i == 0): # add in the first iteration only
                #     program += f'\n\ntestcase = {testcase}\nres = {program_name}()\n\nprint(res)'
                # editedProgram = re.sub(f'\nres = {program_name}', f'\nres = {program_name}()\n\nprint(res)', program)
                editedProgram = program + f'\n\ntestcase = {testcase}\nres = {program_name}()\n\nprint(res)'
                res = runCode(editedProgram, globals())
                res = res.strip()
                # if len(outputs[i]) == 1:
                #     outputs[i] = outputs[i][0]
                if (eval(res) != outputs[i]):
                    return False
            else:
                # if (i == 0): # add in the first iteration only
                #     program += f'\n\ntestcase = {testcase}\nres = {program_name}(*testcase)\n\nprint(res)'
                editedProgram = program + f'\n\ntestcase = {testcase}\nres = {program_name}(*testcase)\n\nprint(res)'
            
                res = runCode(editedProgram, globals())
                res = res.strip()
                # if outputs[i] is not list:
                #     outputs[i] = outputs[i][0]
                if (eval(res) != outputs[i]):
                    return False
        except Exception as e:
            print(e)
            return False
    return True


def selectPool(candidates:List, inputs:List, outputs:List) -> Set:
    """Select pool determined by the number of testcases passed by the candidates"""
    scores = [] # list of scores that will be used to choose the candidate to be selected
    for cand in candidates:
        scores.append(fitness_testCasesPassed(ast.unparse(cand), methodUnderTestName, inputs, outputs) + 1) # why +1, just to make it non-zero and also relatively, it stays the same.
    choice = random.choices(candidates, weights = scores, k=1)[0]
    return ast.unparse(choice)


# def selectPool(candidates:Set) -> Set:
#     pass

def mutate(cand:str, ops:Callable, name_to_operator):  # helper function to mutate the code
    splitted_cand = cand.split('\n')
    faultyLineLocations = list(range(len(splitted_cand)))

    ## for the future ##
    ## we check if the line still exists or not, so that we can mutate it
    ## we will send the column offset but after making sure that the line exists
    locs = random.choices(faultyLineLocations, k=1) # we select from fault line locations arbitrarily for now
    # locs = [4]

    pool = set()
    cand_dash = None
    cand_ast = ast.parse(cand)
    cand_ast.type_ignores = []
    # op_f = None
    for f in locs:
        tokenList, tokenSet, offsets = utils.segmentLine(splitted_cand[f])
        op_f_list, op_f_weights = ops(tokenSet)
        if (op_f_list == []):
            continue
        op_f = (random.choices(op_f_list, k=1)[0])
        copied_cand = copier.visit(cand_ast)
        copied_cand.type_ignores = []
        operator = name_to_operator[op_f]
        cand_dash = operator(target_node_lineno = f + 1, code_ast = cand_ast).visitC() # f + 1 because the line number starts from 1
        pool.add(cand_dash)
        # print(ast.dump(cand_dash, indent=4))
        cand_dash.type_ignores = []
        # print("**********************************")
        # print(ast.unparse(cand_dash))
        cand = copied_cand
        # print(ast.unparse(cand))
        # print("**********************************")
    if (len(pool) == 0):
        return cand
    return selectPool(list(pool), inputs, outputs)

# def mutate_2(cand:str, ops:Callable, inputs: List, outputs:List):  # helper function to mutate the code
#     splitted_cand = cand.split('\n')
#     faultyLineLocations = range(1, len(splitted_cand) + 1)

#     ## for the future ##
#     ## we check if the line still exists or not, so that we can mutate it
#     ## we will send the column offset but after making sure that the line exists
#     locs = random.choices(faultyLineLocations, k=1)
#     pool = set()
#     cand_dash = None
#     for f in locs:
#         op_f = ops(f)
#         op_f = (random.choices(op_f, k=1)[0])
#         copied_cand = copier.visit(cand)
#         cand_dash = op_f(target_node_lineno = f, code_ast = copied_cand).visitC()
#         pool.add(cand_dash)
#         cand = copied_cand
#     selectPool(pool, inputs, outputs)



def main(BugProgram:str, MethodUnderTestName:str, FaultLocations:List, inputs:List, outputs:List, FixPar:Callable, ops:Callable,
         popSize = 6, M = 4, E:int = 5, L:int = 5):
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
    
    name_to_operator = getNameToOperatorMap(operators)
    # while len(Pop) < popSize:
    #     Pop.append(mutate([], ops))  # mutate the population
    
    number_of_iterations = 0
    while len(Solutions) < M and number_of_iterations < 10:
        for p in Pop:
            if p not in Solutions:
                if passesNegTests(p, MethodUnderTestName, inputs, outputs):
                    Solutions.add(p)
                else:
                    Pop[Pop.index(p)] = mutate(p, ops, name_to_operator)
                    # Pop.remove(p) # remove p from the population to be inserted again after mutation
                    # Pop.append(mutate(ops))
        number_of_iterations += 1
    print(Pop)
    return Solutions

if __name__ == '__main__':
    ops = utils.mutationsCanBeApplied # ALIAS to operations that can be applied 
    inputs = []
    outputs = []
    methodUnderTestName = None

    with open('O:/DriveFiles/GP_Projects/Bug-Repair/Q-A/MyMutpy/testcases/BuggyPrograms/2.txt', 'r') as file:
        buggyProgram = file.read()
    with open('O:/DriveFiles/GP_Projects/Bug-Repair/Q-A/MyMutpy/testcases/MetaData/2.txt', 'r') as file:
        methodUnderTestName = file.read().strip()
        foundName = False
        function_names = re.findall(r'def\s+(\w+)', buggyProgram)
        for name in function_names:
            if name == methodUnderTestName:
                foundName = True
                break
        if not foundName:
            print("Function name not found")
            exit(-1)
    with open('O:\DriveFiles\GP_Projects\Bug-Repair\Q-A\MyMutpy/testcases/Inputs/2.txt', 'r') as file:
        lines = file.readlines()
        i = 0
        for line in lines:
            utils.processLine(line, i, inputs)
            i += 1

    with open('O:\DriveFiles\GP_Projects\Bug-Repair\Q-A\MyMutpy/testcases/Outputs/2.txt', 'r') as file:
        lines = file.readlines()
        i = 0
        for line in lines:
            utils.processLine(line, i , outputs)
            i += 1

    faultLocations = range(len(buggyProgram.split('\n'))) # it is there for now
    # print(inputs)
    # print(outputs)
    solutions = main(buggyProgram, methodUnderTestName, faultLocations, inputs, outputs, None, ops)
    print(solutions)
    # print(methodUnderTestName)
    # print(buggyProgram)















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




