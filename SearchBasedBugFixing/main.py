"""
Module : main
The main pipeline resides here

"""

import ast
import re
from operators import *
import utils
import random
from typing import List, Set, Dict, Callable
from runCode import runCode
import faultLocalizationUtils
from mutationFunctions import *
import InsertVisitor

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
    res = None
    passedTests = 0

    for i in range(len(inputs)):
        try:
            testcase = inputs[i]
            if (type(testcase) is not list):
                if (testcase.lower() == 'void'):
                    editedProgram = program + f'\n\nres = {program_name}()\n\nprint(res)'
                else:
                    editedProgram = program + f'\n\ntestcase = {testcase}\nres = {program_name}({testcase})\n\nprint(res)'
                res = runCode(editedProgram, globals())
                res = res.strip()
                if (eval(res) != outputs[i]):
                    return False
            else:
                editedProgram = program + f'\n\ntestcase = {testcase}\nres = {program_name}(*testcase)\n\nprint(res)'
            
                res = runCode(editedProgram, globals())
                res = res.strip()
                # if outputs[i] is not list:
                #     outputs[i] = outputs[i][0]
                if (eval(res) == outputs[i]):
                    passedTests += 1
        except Exception as e:
            print(e)
            return 0

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
            if (type(testcase) is not list):
                if (testcase.lower() == 'void'):
                    editedProgram = program + f'\n\nres = {program_name}()\n\nprint(res)'
                else:
                    editedProgram = program + f'\n\ntestcase = {testcase}\nres = {program_name}({testcase})\n\nprint(res)'
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


def mutate(cand:str, ops:Callable, name_to_operator:Dict, 
           faultyLineLocations: List, weightsFaultyLineLocations:List ):  # helper function to mutate the code
    
    pool = set()
    availableChoices = {"1": "Insertion", "2": "Swap", "3": "Update"}
    weightsMutation = [0.1, 0.1, 0.8]
    choiceMutation = random.choices(list(availableChoices.keys()),weights=weightsMutation, k=1)[0]
    if availableChoices[choiceMutation] == "Update":
        update(
            cand=cand,
            faultyLineLocations=faultyLineLocations,
            weightsFaultyLineLocations=weightsFaultyLineLocations,
            ops=ops,
            name_to_operator=name_to_operator,
            pool=pool
        )
    elif availableChoices[choiceMutation] == "Insertion":
        insert(cand=cand, pool=pool)
    elif availableChoices[choiceMutation] == "Update":
        pass

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



def main(BugProgram:str, 
        MethodUnderTestName:str, 
        FaultLocations:List,
        weightsFaultyLocations:List,
        inputs:List, 
        outputs:List, 
        FixPar:Callable, 
        ops:Callable,
        popSize:int = 6, 
        M:int = 4, 
        E:int = 5, 
        L:int = 5):
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
    
    name_to_operator = utils.getNameToOperatorMap(operators)
    # while len(Pop) < popSize:
    #     Pop.append(mutate([], ops))  # mutate the population


    number_of_iterations = 0
    while len(Solutions) < M and number_of_iterations < 10:
        for p in Pop:
            if p not in Solutions:
                if passesNegTests(p, MethodUnderTestName, inputs, outputs):
                    Solutions.add(p)
                else:
                    Pop[Pop.index(p)] = mutate(p, ops, name_to_operator, FaultLocations, weightsFaultyLocations)
                    # Pop.remove(p) # remove p from the population to be inserted again after mutation
                    # Pop.append(mutate(ops))
        number_of_iterations += 1
    # print(Pop)
    return Solutions








if __name__ == '__main__':
    ops = utils.mutationsCanBeApplied # ALIAS to operations that can be applied 
    inputs = []
    outputs = []
    inputProgramPath = 'SearchBasedBugFixing/testcases/BuggyPrograms'
    destinationLocalizationPath = 'SearchBasedBugFixing/testcases/GeneratedTests'
    inputCasesPath = 'SearchBasedBugFixing/testcases/Inputs'
    outputCasesPath = 'SearchBasedBugFixing/testcases/Outputs'
    metaDataPath = 'SearchBasedBugFixing/testcases/MetaData'
    file_id = 1
    file_name = f'{file_id}.txt'
    
    methodUnderTestName = None

    with open(f'{inputProgramPath}/{file_name}', 'r') as file:
        buggyProgram = file.read()
    with open(f'{metaDataPath}/{file_name}', 'r') as file:
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
    with open(f'{inputCasesPath}/{file_name}', 'r') as file:
        lines = file.readlines()
        i = 0
        for line in lines:
            utils.processLine(line, i, inputs)
            i += 1

    with open(f'{outputCasesPath}/{file_name}', 'r') as file:
        lines = file.readlines()
        i = 0
        for line in lines:
            utils.processLine(line, i , outputs)
            i += 1

    # faultLocations = range(len(buggyProgram.split('\n'))) # it is there for now
    # copyFolder(inputProgramPath, destinationLocalizationPath, file_id)
    # create_py_test(inputs, outputs, methodUnderTestName, destinationLocalizationPath)

    faultLocalizationUtils.main(inputs, outputs, methodUnderTestName, inputProgramPath, destinationLocalizationPath, file_id)
    faultLocations, weightsFaultyLocations = faultLocalizationUtils.getFaultyLines('..') # fauly locations are in the parent directory
    # destination_folder = destinationLocalizationPath
    # test_path = f'{destination_folder}/test.py'
    # src_path = f'{destination_folder}/source_code.py'
    # s = faultLocalizationUtils.runFaultLocalization(test_path, src_path)

    # print(inputs)
    # print(outputs)
    faultLocations = list(map(int, faultLocations))
    weightsFaultyLocations = list(map(float, weightsFaultyLocations))
    
    print(faultLocations)
    print(weightsFaultyLocations)


    solutions = main(buggyProgram, methodUnderTestName, faultLocations, weightsFaultyLocations, inputs, outputs, None, ops)
    for solution in solutions:
        print(solution)
    # print(methodUnderTestName)
    # print(buggyProgram)
