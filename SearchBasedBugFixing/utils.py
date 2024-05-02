import ast
import copy
import re
from operators import standard_operators, experimental_operators
import random

def build_name_to_operator_map():
    result = {}
    for operator in standard_operators | experimental_operators:
        result[operator.name()] = operator
        # result[operator.long_name()] = operator
    return result

def getNameToOperatorMap():
    name_to_operator = build_name_to_operator_map()
    return name_to_operator

# def checkIsSlice(tokens: list, i: int):
#     """
#     Check if the current token is a slice operator or not
#     Args:
#         tokens: list of tokens in the faulty location
#         i: index of the current token
#     Returns:
#         True if the current token is a slice operator, False otherwise
#     """
#     if tokens[i] == ":":
#         if i - 1 >= 0 and (tokens[i - 1] == "[" or type(tokens[i - 1]) == int):
#             return True
#         if i + 1 < len(tokens) and (tokens[i - 1] == "[" or type(tokens[i + 1]) == int):
#             return True
#     return False

def checkPreviousNotDigit(tokens: list, i: int):
    """
    Check if the previous token is not a digit
    Args:
        tokens: list of tokens in the faulty location
        i: index of the current token
    Returns:
        True if the previous token is not a digit, False otherwise
    """
    # it is not plausible that we will reach the beginning of line without any token (int or none)
    while (i - 1 >= 0 and (tokens[i - 1]) != ' '):
        i -= 1
    if not (type(tokens[i]) == int):
        return True
    return False



def checkIsSlice(listTokens, currentIndex):
    def checkRight(tokens, i):
        while i + 1 < len(tokens) and tokens[i + 1] != ']':
            val = tokens[i + 1] # value may be a space, digit or negative, else, this can not be a slice
            if not (val.lstrip("-").lstrip('+').lstrip('0').isdigit() or val == '-' or val == ' '):
                return False
            i += 1
        else: # if break, will not go to else
            if (i + 1 < len(tokens) and tokens[i + 1] == ']'):
                return True
        return False
    
    def checkLeft(tokens, i):
        while i - 1 >= 0 and tokens[i - 1] != '[':
            val = tokens[i - 1] # value may be a space, digit or negative, else, this can not be a slice
            if not (val.lstrip("-").lstrip('+').lstrip('0').isdigit() or val == '-' or val == ' '):
                return False
            i -= 1
        else: # if break, will not go to else
            if (tokens[i - 1] == '['):
                return True
        return False
    
    if (checkRight(listTokens, currentIndex) and checkLeft(listTokens, currentIndex)):
        return True
    else:
        return False

def addColumnOffset(offsetsDict: dict, token: str, lineno: int):
    if (offsetsDict.get(token)):
        offsetsDict[token].append(lineno)
    else:
        offsetsDict[token] = [lineno]

def checkSavedSequence(temp: str, lst: list, st: set, unit_ColOffset: dict, col_offsets: list):
    if (temp != ""):
        lst.append(temp)
        st.add(temp)
        addColumnOffset(unit_ColOffset, temp, col_offsets[-1])
        temp = ""
    return temp


def segmentLine(line):
    unit_ColOffset = dict() # dictionary that holds unit and the places that it is in 
    segmentors = {' ', '(', ')', '[', ']', '{', '}', ',', '.', ';'}
    operators_1 = {'+', '-', '*', '/', '%', '>', '<', '^'} # one character string
    operators_2 = {'**', '//', '<<', '>>'}  # two characters string
    i = 0  # iterator to parse the line character by character
    ln = len(line)  # length of the line
    lst = []  #list of tokens
    col_offsets = []  # column offsets of the tokens
    st = set() # set of tokens
    temp = ""

    while(i < ln):
        if (line[i] == " "): # I do not need spaces
            if (i - 1 >= 0 and line[i - 1] != " "): # means that the previous character was not a space
                temp = checkSavedSequence(temp, lst, st, unit_ColOffset=unit_ColOffset, col_offsets=col_offsets)

            i += 1
            continue
        elif (line[i] == "\n"): # break loop has to be added in the scope as we are considering only one line and remove the outer else, however, Ignore for now
            temp = checkSavedSequence(temp, lst, st, unit_ColOffset=unit_ColOffset, col_offsets=col_offsets)

        elif (line[i] == "\t"): # Ignore tabs
            i += 1
            continue
        elif (line[i] == "#"): # Ignore comments
            while (i < ln and line[i] != "\n"):
                i += 1
        elif (line[i] in segmentors):
            temp = checkSavedSequence(temp, lst, st, unit_ColOffset=unit_ColOffset, col_offsets=col_offsets)
            lst.append(line[i])
            st.add(temp)
            col_offsets.append(i + 1)
            addColumnOffset(unit_ColOffset, line[i], i + 1)
        elif (line[i] in operators_1 and ((line[i + 1] in operators_1 and line[i + 2] == '=') or line[i + 1] == '=')):
            # this is augmented Assignment
            col_offsets.append(i + 1)
            addColumnOffset(unit_ColOffset, line[i], i + 1)

            temp = checkSavedSequence(temp, lst, st, unit_ColOffset=unit_ColOffset, col_offsets=col_offsets)
            if ((line[i + 1] in operators_1 and line[i + 2] == '=')):
                lst.append("AugAssign")
                st.add("AugAssign")
                i += 2
            else:
                lst.append("AugAssign")
                st.add("AugAssign")
                i += 1
        elif (line[i] == "="):
            col_offsets.append(i + 1)
            
            temp = checkSavedSequence(temp, lst, st, unit_ColOffset=unit_ColOffset, col_offsets=col_offsets)
            if (line[i + 1] == "="):
                lst.append("==")
                st.add("==")
                addColumnOffset(unit_ColOffset, "==", i + 1)
                i += 1
            else:
                lst.append("=")
                st.add("=")
                addColumnOffset(unit_ColOffset, "=", i + 1)
        
        elif (line[i] in operators_1 and (temp != "" or line[i+1] != " ")): # this means that the operators and the operands are adherent
            lst.append(temp)
            st.add(temp)
            temp = ""
            col_offsets.append(i + 1)

            if (line[i] + line[i + 1] in operators_2):
                lst.append(line[i] + line[i + 1])
                st.add(line[i] + line[i + 1])
                addColumnOffset(unit_ColOffset, line[i] + line[i + 1], i + 1)
                i += 1
            else:
                lst.append(line[i])
                st.add(line[i])
                addColumnOffset(unit_ColOffset, line[i], i + 1)

        elif (line[i] == "-"): # Check if it is a unary subtraction (-x)
            if (i + 1 < ln and line[i + 1].isdigit() and checkPreviousNotDigit(line, i)):
                if (temp == ""):
                    col_offsets.append(i + 1)
                    addColumnOffset(unit_ColOffset, line[i], i + 1)

                temp += line[i]
            else:
                if (temp != ""):
                    lst.append(temp) #add the previous accumulated
                    st.add(temp)
                    temp = ""
                lst.append(line[i]) # add the current
                col_offsets.append(i + 1)
                addColumnOffset(unit_ColOffset, line[i], i + 1)

                st.add(line[i])
                temp = ""
        elif (line[i] == "\"" or line[i] == "'"): # Check if it is a string
            temp = checkSavedSequence(temp, lst, st, unit_ColOffset=unit_ColOffset, col_offsets=col_offsets)
            lst.append("STR") # add the current
            col_offsets.append(i + 1)
            addColumnOffset(unit_ColOffset, "STR", i + 1)

            st.add(line[i])
            temp = ""
            if (line[i] == "\""):
                i += 1
                while(i < ln and line[i] != '"'):
                    i += 1
            else:
                i += 1
                while(i < ln and line[i] != "'"):
                    i += 1
            i += 1
        elif (line[i] == ":"):
            if (checkIsSlice(line, i)): # ensure it is a slice and not function definition
                temp = checkSavedSequence(temp, lst, st, unit_ColOffset=unit_ColOffset, col_offsets=col_offsets)
                lst.append(":")
                col_offsets.append(i + 1)
                addColumnOffset(unit_ColOffset, line[i], i + 1)

                st.add(":")
                temp = ""
        else:
            if (line[i].isdigit()): # check digit
                savedI = i
                while(i < ln and line[i].isdigit()):
                    i += 1
                lst.append("NUM")
                st.add("NUM")
                col_offsets.append(savedI + 1)
                addColumnOffset(unit_ColOffset, "NUM", savedI + 1)
                continue

            if (temp == ""): # this means it is the first in the sequence
                col_offsets.append(i + 1)
                # addColumnOffset(unit_ColOffset, line[i], i + 1)
            temp += line[i]
        i += 1
    else:  # else for the while loop
        if (temp != ""):
            lst.append(temp)
            st.add(temp)
    # checkIsSlice = False
    return lst, st, col_offsets, unit_ColOffset



# make a dictionary that contains offsets of the tokens

def mutationsCanBeApplied(setTokens: set):
    """
    Iterate over the set of segmented parts in the faulty location and insert the mutations that can be applied
    Args: 
        setTokens: set of tokens in the faulty location
    Returns:
        list of mutations that can be applied
    """
    lstMutations = [] # list of mutations that can be applied
    
    # Note: the follwing will be converted to  a loop over the list to get the column offset
    ################ ARITHMETIC OPERATORS ################
    if '+' in setTokens: lstMutations.append('ADD');# lstMutations.append('ARD') # the only mutations coupled with other binary operators that are encompassed in a list to accomodate the operation name
    if '-' in setTokens: lstMutations.append('SUB');# lstMutations.append('ARD')
    if '*' in setTokens: lstMutations.append('MUL');# lstMutations.append('ARD')
    if '/' in setTokens: lstMutations.append('DIV');# lstMutations.append('ARD')
    if '%' in setTokens: lstMutations.append('MOD');# lstMutations.append('ARD')
    if '**' in setTokens: lstMutations.append('POW');# lstMutations.append('ARD')
    if '//' in setTokens: lstMutations.append('FLOORDIV');# lstMutations.append('ARD')


    ################## Augmented Assign #####################
    if 'AugAssign' in setTokens: lstMutations.append('AUG')

    ################ RELATIONAL OPERATORS ################
    if '<' in setTokens: lstMutations.append('ROR') # relational operator replacement
    if '>' in setTokens: lstMutations.append('ROR')
    if '<=' in setTokens: lstMutations.append('ROR')
    if '>=' in setTokens: lstMutations.append('ROR')

    ################ ASSIGNMENT OPERATORS ################
    if '==' in setTokens: lstMutations.append('ROR')
    if '!=' in setTokens: lstMutations.append('ROR')

    ################ LOGICAL OPERATORS ################
    if 'and' in setTokens: lstMutations.append('LOR')
    if 'or' in setTokens: lstMutations.append('LOR')
    # if 'not' in setTokens: lstMutations.append('LOR')

    ################ BITWISE OPERATORS ################
    if '&' in setTokens: lstMutations.append('BOR')
    if '|' in setTokens: lstMutations.append('BOR')
    if '~' in setTokens: lstMutations.append('BOR')
    if '^' in setTokens: lstMutations.append('BOR')
    if '<<' in setTokens: lstMutations.append('BOR')
    if '>>' in setTokens: lstMutations.append('BOR')

    ################ UNARY OPERATORS ################
    # if '-' in setTokens: lstMutations.append('UOR')
    # if '+' in setTokens: lstMutations.append('UOR')
    if 'not' in setTokens: lstMutations.append('UOR')
    if '~' in setTokens: lstMutations.append('UOR')

    ################ MEMBERSHIP OPERATORS ################
    if 'in' in setTokens: lstMutations.append('MER')
    if 'not in' in setTokens: lstMutations.append('MER')
    if 'is not' in setTokens: lstMutations.append('MER')
    if 'is' in setTokens: lstMutations.append('MER')

    ############### LOOPS OPERATORS ################
    if 'for' in setTokens: lstMutations.extend(['OIL', 'RIL', 'ZIL', 'LOD']) # one iteration loop, reverse iteration loop, zero iteration loop
    if 'while' in setTokens: lstMutations.extend(['OIL', 'RIL', 'ZIL', 'LOD']) # added statement deletion
    if 'range' in setTokens: lstMutations.append('OIL')
    if 'enumerate' in setTokens: lstMutations.append('OIL')
    if 'zip' in setTokens: lstMutations.append('OIL')

    ################ CONDITIONAL OPERATORS ################
    if 'if' in setTokens: lstMutations.extend(['COI', 'COD'])

    ################ SLICE OPERATORS ################
    if ':' in setTokens: lstMutations.append('SIR') # make sure it is encompassed between square brackets

    ################ BREAK AND CONTINUE ################
    if 'break' in setTokens: lstMutations.append('BCR')
    if 'continue' in setTokens: lstMutations.append('BCR')

    ################ STATEMENT DELETION ################
    # these are very special, I will add with very low probability
    maxRand = 100
    prob = random.randint(1, maxRand) / maxRand
    if (prob > 0.95):  # Do not forget weights
        if 'NUM' in setTokens: lstMutations.append('CNR') # constant replacement
        if 'STR' in setTokens: lstMutations.append('CNR') # constant replacement
        if 'return' in setTokens: lstMutations.append('STD')
    
    ############### STRING MUTATIONS ################
    if '"' in setTokens or '\'' in setTokens: lstMutations.append('CSR')

    # if '()' in setTokens: lstMutations.append('MR')
    # if '[]' in setTokens: lstMutations.append('MR')
    # if '{}' in setTokens: lstMutations.append('MR')
    weights = [1] * len(lstMutations) # the weights are all equal for now

    return lstMutations, weights


def checkTypeInput(val):
    val = val.strip()
    if val.startswith("\"") and val.endswith("\""): # I know that it is string explicitly
        val = re.sub(r"\"", "\\\"", val)
        val = re.sub(r"_", " ", val)
    elif val.startswith("[") and val.endswith("]"):  # temporary for testing
        theList = val[1:-1].split(',')
        for i in range(len(theList)):
            theList[i] = checkTypeInput(theList[i])
        val = theList
    elif val.lstrip("-").lstrip('+').lstrip('0').isdigit():
        val = int(val)
    elif "." in val:
        units, decimal = val.split(".")
        if not (units.lstrip("-").lstrip('+').lstrip('0').isdigit() and decimal.isdigit()):
            print(units)
            print(decimal)
            return
        val = float(val)
    # if not within all of the previous conditions, val will return as it is
    return val

def processLine(line, i, testcaseList):
    """
    process the line of either the input txt file or output text file
    Args:
        line: line to be processed
        i: line number (zero indexed)
        testcaseList: list to store the testcases outputs or inputs
    """
    if line == '':
        print(f"Input is blank, please insert input at line {i + 1}")
        exit(-1)
    extractedLine = line.strip().split(',')
    if len(extractedLine) == 1:  # I think this condition is unnecessary , but later
        testcaseList.append(checkTypeInput(extractedLine[0]))
    else:
        for i in range(len(extractedLine)):
            extractedLine[i] = checkTypeInput(extractedLine[i])
        testcaseList.append(extractedLine)


def parentify(tree):
    tree.parent = None
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node


