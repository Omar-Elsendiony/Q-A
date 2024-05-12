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
from SearchBasedBugFixing.identifier.identifierVisitor import IdentifierVisitor
import InsertVisitor
import SwapVisitor

def editFreq(cand):
    ## TODO ##
    pass

def compare_input_output(res, output):
    outputMod = output
    if (type(output) is list):
        if len(output) == 1:
            outputMod = output[0]
        else:
            outputMod = tuple(output)

    if (res == outputMod):
        return True
    return False


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
                res, isError = runCode(editedProgram, globals())
                if (isError):
                    return -9
                res = res.strip()
                if (compare_input_output(eval(res), outputs[i])):
                    passedTests += 1
            else:
                editedProgram = program + f'\n\ntestcase = {testcase}\nres = {program_name}(*testcase)\n\nprint(res)'
            
                res, isError = runCode(editedProgram, globals())
                res = res.strip()
                # this mutation is of no avail and caused error
                if (isError):
                    passedTests -= 9
                    return passedTests
                if (compare_input_output(eval(res), outputs[i])):
                    passedTests += 1
        except Exception as e:
            # print(e)
            return -9
    # print(eval(res))
    if (eval(res) is None and passedTests == 0):
        passedTests -= 9
    return passedTests



    
# @profile
def passesNegTests(program:str, program_name:str, inputs:List, outputs:List) -> bool:
    """
    Inputs:
    program : str :  program to be tested
    inputs : List :  inputs to the program
    outputs : List :  outputs of the program
    """
    # let's try by capturing the name of the function in regex and the list of names is compared with the name of the function
    editedProgram = ""
    res = None

    for i in range(len(inputs)):
        try:
            testcase = inputs[i]
            if (len(testcase) == 1):
                testcase = testcase[0]
                if (testcase.lower() == 'void'):
                    editedProgram = program + f'\n\nres = {program_name}()\n\nprint(res)'
                else:
                    editedProgram = program + f'\n\ntestcase = {testcase}\nres = {program_name}(testcase)\n\nprint(res)'
                res, isError = runCode(editedProgram, globals())
                if (isError):
                    return False
                res = res.strip()

                if (not compare_input_output(eval(res), outputs[i])):
                    return False
            else:
                inputStrings = ""
                outputStrings = ""
                for argIndex, arg in enumerate(testcase):
                    input_inp = f'input_{argIndex} = {arg}\n'
                    inputStrings += input_inp
                for argIndex in range(len(testcase)):
                    output_out = f'input_{argIndex},'
                    outputStrings += output_out
                editedProgram = program + inputStrings + f'\nres = {program_name}({outputStrings})\n\nprint(res)'
            
                res, isError = runCode(editedProgram, globals())
                if (isError):
                    return False
                res = res.strip()
                # if outputs[i] is not list:
                #     outputs[i] = outputs[i][0]
                if (not compare_input_output(eval(res), outputs[i])):
                # if (eval(res) != outputs[i]):
                    return False
        except Exception as e:
            return False
    # print(eval(res))
    return True


# import subprocess
# def passesNegTests_2(program:str, program_name:str, inputs:List, outputs:List):
#     test_path = f'testcases/GeneratedTests/test.py'
#     src_path = f'testcases/GeneratedTests/source_code.py'
#     res = subprocess.run(["python3", "-m", "pytest", f"{test_path}"], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
#     # print(str(res).split()[-1])
#     res = res.stdout.decode('utf-8')
#     splitted = res.split()
#     passed = None; Failed = None
#     passOrFailedNum = splitted[-5]
#     passOrFailedString = splitted[-4]
#     if (passOrFailedString == "passed"):
#         passed = passOrFailedNum
#     else:
#         Failed = passOrFailedNum
#         passed = 0
#     if passed == len(inputs):
#         return True
#     else:
#         return False

# def passesNegTests_3(program:str, program_name:str, inputs:List, outputs:List):
#     test_path = f'testcases/GeneratedTests/test.py'
#     src_path = f'testcases/GeneratedTests/source_code.py'
#     res = subprocess.run(["python3", "-m", "pytest", f"{test_path}"], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
#     # print(str(res).split()[-1])
#     res = res.stdout.decode('utf-8')
#     splitted = res.split()
#     passed = None; Failed = None
#     passOrFailedNum = splitted[-5]
#     passOrFailedString = splitted[-4]
#     if (passOrFailedString == "passed"):
#         passed = passOrFailedNum
#     else:
#         Failed = passOrFailedNum
#         passed = 0
#     return passed


# @profile
# def selectPool(candidates:List, inputs:List, outputs:List):
#     """Select pool determined by the number of testcases passed by the candidates"""
#     # scores = [] # list of scores that will be used to choose the candidate to be selected
#     # # # print(str(len(candidates))+'---------------------------------------')
#     # for cand in candidates:
#     #     scores.append(passesNegTests_3(ast.unparse(cand), methodUnderTestName, inputs, outputs) + 10) # why +10, just to make it non-zero and also relatively, it stays the same.
#     # choice = random.choices(range(len(candidates)), weights = scores, k=1)[0]

#     return ast.unparse(candidates[0])
#     # return (ast.unparse(candidates[0]))


# def selectPool(candidates:Set) -> Set:
#     pass


# @profile
def update(cand, faultyLineLocations, weightsFaultyLineLocations, ops, name_to_operator, pool, limitLocations = 2):
    # instance of the copy class to be used for copying ASTs
    copier = copyMutation()
    # split the candidate into lines to be able to segment them into tokens and we are working line-wise fault location
    splitted_cand = cand.split('\n')

    # the maximum possible length of faulty locations are the length of the code itself
    limitKPossible = len(faultyLineLocations)
    locationsExtracted = limitKPossible  if (limitKPossible < limitLocations) else limitLocations
    # choose from the locations based on a parameter sent by the user which sould not exceed max length, that is why a limit cap is present
    locs = random.choices(faultyLineLocations, weights = weightsFaultyLineLocations, k=locationsExtracted)

    # candidate that will be mutated
    cand_dash = None
    # parse the candidate
    cand_ast = ast.parse(cand)
    # add this line as type ignores gets missed in the mutations and it is needed in ast.unparse
    cand_ast.type_ignores = []

    # parentify the candidate so it will be used by functions like mutate_DIV, mutate_ADD, etc.
    utils.parentify(cand_ast)
    # get the list of identifiers of an ast using IdentifierVisitor
    idVistitor =  IdentifierVisitor()
    idVistitor.visit(cand_ast)
    # add the list of identifiers to the baseOperator class where it is seen by all its descendants
    # baseOperator.set_identifiers((idVistitor.get_identifiers))

    for f in locs:
        # import time
        # parentify the candidate so it will be used by functions like mutate_DIV, mutate_ADD, etc.
        utils.parentify(cand_ast)
        # start = time.time()
        try:
            # segment line into presumably tokens
            tokenSet, units_ColOffset = utils.segmentLine(splitted_cand[f - 1])
        except:
            # because the line may be removed by mutations
            continue
        # print(time.time() - start)

        # getting the mutations that can be applied, original tokens and weight of each mutation
        op_f_list, op_f_weights, original_op = ops(tokenSet)
        # op_f_list may be empty as the lines are removed and added, etc. However, running the fault localization again will solve the issue
        if (op_f_list == []):
            continue
        # start = time.time()
        # Choose the index with the higher probability
        choice_index = random.choices(range(len(op_f_list)), weights = op_f_weights, k=1)[0]
        # Get the operation neumonic from operation list
        op_f = op_f_list[choice_index]
        # print(op_f)
        # get the colum offset occurances of such an operation
        colOffsets = units_ColOffset[original_op[choice_index]]
        # get an index of the operation that you want to apply on
        col_index = random.randint(0, len(colOffsets) - 1)
        # get the operator class that holds all the logic from the 3 letters neumonic
        operator = name_to_operator[op_f]

        # copy the candidate as not to make the mutation affect the original candidate
        copied_cand = copier.visit(cand_ast)
        copied_cand.type_ignores = []

        col_index = col_index if op_f != "ARD" else choice_index // 2
        # apply the mutation and acquire a new candidate
        cand_dash = operator(target_node_lineno = f, code_ast = cand_ast, indexMutation= col_index, specifiedOperator=original_op[choice_index]).visitC() # f + 1 because the line number starts from 1
        # adds/corrects the line number as well as column offset
        ast.fix_missing_locations(cand_dash)
        cand_dash.type_ignores = []
        # add the candidate to the pool that you will select from
        pool.append(cand_dash)
        # return cand to its original ast (despite different location in memory)
        cand = copied_cand
        # print(time.time() - start)
    # exit(0)


def insert(cand:str, pool:set):  # helper function to mutate the code
    # insert will be updated once more to add in certain locations
    # parse the candidate
    cand_ast = ast.parse(cand)
    # add type ignores
    cand_ast.type_ignores = []
    # call the function that will insert the node and this function is present in the library insert visitor
    InsertVisitor.insertNode(cand_ast)
    # add to the possible candidates
    pool.append(cand_ast)
    cand_ast.type_ignores = []
    # add the line numbers
    ast.fix_missing_locations(cand_ast)
    return

def swap(cand:str, pool:set):  # helper function to mutate the code
    cand_ast = ast.parse(cand)
    cand_ast.type_ignores = []
    SwapVisitor.swapNodes(cand_ast)
    pool.append(cand_ast)
    cand_ast.type_ignores = []
    ast.fix_missing_locations(cand_ast)
    return


def mutate(cand:str, ops:Callable, name_to_operator:Dict, 
           faultyLineLocations: List, weightsFaultyLineLocations:List, L:int ):  # helper function to mutate the code
    # try:
    pool = list()
    # pool_list = []
    availableChoices = {"1": "Insertion", "2": "Swap", "3": "Update"}
    weightsMutation = [0.01, 0.01, 0.98]
    choiceMutation = random.choices(list(availableChoices.keys()), weights=weightsMutation, k=1)[0]
    if availableChoices[choiceMutation] == "Update" or availableChoices[choiceMutation] == "Insertion":
        update(
            cand=cand,
            faultyLineLocations=faultyLineLocations,
            weightsFaultyLineLocations=weightsFaultyLineLocations,
            ops=ops,
            name_to_operator=name_to_operator,
            pool=pool,
            limitLocations=L
        )
        # insert(cand=cand, pool=pool)
    elif availableChoices[choiceMutation] == "Insertion":
        insert(cand=cand, pool=pool)
    elif availableChoices[choiceMutation] == "Swap":
        swap(cand=cand, pool=pool)
    if (len(pool) == 0):
        return cand, False

    scores = [] # list of scores that will be used to choose the candidate to be selected
    for cand in pool:
        scores.append(fitness_testCasesPassed(ast.unparse(cand), methodUnderTestName, inputs, outputs) + 10) # why +10, just to make it non-zero and also relatively, it stays the same.
    choice = random.choices(range(len(pool)), weights = scores, k=1)[0]
    return ast.unparse(pool[choice]), False



# @profile
def main(BugProgram:str, 
        MethodUnderTestName:str, 
        FaultLocations:List,
        weightsFaultyLocations:List,
        inputs:List, 
        outputs:List, 
        FixPar:Callable,
        ops:Callable,
        popSize:int = 220, 
        M:int = 4, 
        E:int = 10, 
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
    
    name_to_operator = utils.getNameToOperatorMap()
    while len(Pop) < popSize:
        newMutation, errorOccured = mutate(BugProgram, ops, name_to_operator, FaultLocations, weightsFaultyLocations, L)
        if not errorOccured:
            Pop.append(newMutation)  # mutate the population

    # print(len(Pop))
    number_of_iterations = 0
    while len(Solutions) < M and number_of_iterations < 3:
        # print(number_of_iterations)
        for p_index, p in enumerate(Pop):
            if p not in Solutions:
                if passesNegTests(p, MethodUnderTestName, inputs, outputs):
                    Solutions.add(p)
                else:
                    mutationCandidate, errorOccured = mutate(p, ops, name_to_operator, FaultLocations, weightsFaultyLocations, L)
                    # if (errorOccured): 
                    #     Pop.pop(p_index)
                    # else:
                    #     Pop[p_index] = mutationCandidate
                    Pop[p_index] = mutationCandidate
                    # Pop.remove(p) # remove p from the population to be inserted again after mutation
                    # Pop.append(mutate(ops))
        number_of_iterations += 1
    # print(Pop)
    return Solutions, Pop




if __name__ == '__main__':
    ops = utils.mutationsCanBeApplied # ALIAS to operations that can be applied 
    inputs = []
    outputs = []
    inputProgramPath = 'SearchBasedBugFixing/testcases/BuggyPrograms'
    destinationLocalizationPath = 'SearchBasedBugFixing/testcases/GeneratedTests'
    inputCasesPath = 'SearchBasedBugFixing/testcases/Inputs'
    outputCasesPath = 'SearchBasedBugFixing/testcases/Outputs'
    metaDataPath = 'SearchBasedBugFixing/testcases/MetaData'
    file_id = 2
    file_name = f'{file_id}.txt'
    typeHintsInputs = []
    typeHintsOutputs = []
    methodUnderTestName = None

    try:
        with open(f'{inputProgramPath}/{file_name}', 'r') as file:
            buggyProgram = file.read()
            try:
                bp = ast.parse(buggyProgram)
            except:
                print("Problem in parsing the buggy program")
                exit(-1)
        with open(f'{metaDataPath}/{file_name}', 'r') as file:
            lines = file.readlines()
            methodUnderTestName = lines[0].strip()
            function_names = re.findall(r'def\s+(\w+)', buggyProgram)
            for name in function_names:
                if name == methodUnderTestName:
                    foundName = True
                    break
            if not foundName:
                print("Function name not found")
                exit(-1)   
            l = 1
            while(lines[l] != '\n'):
                typeHintsInputs.append(lines[l].strip())
                # utils.processLine(lines[l], l, inputs)
                l += 1
            l += 1
            while(l < len(lines) and lines[l] != '\n'):
                typeHintsOutputs.append(lines[l].strip())
                # utils.processLine(lines[l], l, inputs)
                l += 1
        with open(f'{inputCasesPath}/{file_name}', 'r') as file:
            lines = file.readlines()
            i = 0
            inputTestCase = []
            for line in lines:
                if (line == '\n'): 
                    if (inputTestCase != []) : inputs.append(inputTestCase); inputTestCase = []
                    else: continue
                else: utils.processLine(line, i, inputTestCase)
                i += 1
            if (inputTestCase != []):
                inputs.append(inputTestCase)

        with open(f'{outputCasesPath}/{file_name}', 'r') as file:
            lines = file.readlines()
            i = 0
            outputTestCase = []
            for line in lines:
                if (line == '\n'):
                    if (outputTestCase != []) : outputs.append(outputTestCase);outputTestCase = []
                    else: continue
                else: utils.processLine(line, i, outputTestCase)
                i += 1
            if (outputTestCase != []):
                outputs.append(outputTestCase)
    except Exception as e:
        print("Problem in reading files, insufficient data")
        print(e)
        exit(-1)
    print(inputs)
    print(outputs)


    faultLocalizationUtils.main(
        inputs = inputs, 
        outputs = outputs, 
        function_name= methodUnderTestName, 
        source_folder= inputProgramPath, 
        destination_folder= destinationLocalizationPath, 
        file_id= file_id,
        inputHints=typeHintsInputs,
        outputHints=typeHintsOutputs)
    
    faultLocations, weightsFaultyLocations = faultLocalizationUtils.getFaultyLines('..') # fauly locations are in the parent directory
    destination_folder = destinationLocalizationPath
    test_path = f'{destination_folder}/test.py'
    src_path = f'{destination_folder}/source_code.py'
    # s = faultLocalizationUtils.runFaultLocalization(test_path, src_path)
    faultLocations = list(map(int, faultLocations))
    weightsFaultyLocations = list(map(float, weightsFaultyLocations))

    solutions, population = main(BugProgram=buggyProgram, 
                    MethodUnderTestName=methodUnderTestName, 
                    FaultLocations=faultLocations, 
                    weightsFaultyLocations=weightsFaultyLocations, 
                    inputs=inputs,
                    outputs=outputs, 
                    FixPar=None, 
                    ops=ops)
    print("************************************************************")
    for solution in solutions:
        print(solution)
    print("************************************************************")
    # print(len(population))
    # i = 0
    # for p in population:
    #     print(population[i + 100])
    #     i += 1
    #     if (i == 10):
    #         break
    # print(methodUnderTestName)
    # print(buggyProgram)
