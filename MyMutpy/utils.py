import ast
import copy
import re
import sys
import time
import types

from numpy import extract
from sklearn.tree import export_graphviz
from operators import standard_operators, experimental_operators

def build_name_to_operator_map():
    result = {}
    for operator in standard_operators | experimental_operators:
        result[operator.name()] = operator
        # result[operator.long_name()] = operator
    return result



def segmentLine(line):
    segmentors = {' ', '(', ')', '[', ']', '{', '}', ':', ','}
    i = 0  # iterator to parse the line character by character
    ln = len(line)  # length of the line
    lst = []  #list of tokens
    col_offsets = []  # column offsets of the tokens
    st = set() # set of tokens
    temp = ""

    while(i < ln):
        if (line[i] == " "): # I do not need spaces
            if (i - 1 >= 0 and line[i - 1] != " "): # means that the previous character was not a space
                if (temp != ""):
                    lst.append(temp)
                    st.add(temp)
                    temp = ""
            i += 1
            continue
        elif (line[i] == "\n"): # break loop has to be added in the scope as we are considering only one line and remove the outer else, however, Ignore for now
            if (temp != ""):
                lst.append(temp)
                st.add(temp)
                temp = ""
        elif (line[i] == "\t"): # Ignore tabs
            i += 1
            continue
        elif (line[i] == "#"): # Ignore comments
            while ( i < ln and line[i] != "\n"):
                i += 1
        elif (line[i] in segmentors):
            if (temp != ""):
                lst.append(temp)
                st.add(temp)
                temp = ""
            lst.append(line[i])
            col_offsets.append(i + 1)
            st.add(temp)
        elif (line[i] == "-"): # Check if it is a unary sub
            if (i + 1 < ln and line[i + 1].isdigit()):
                if (temp == ""):
                    col_offsets.append(i + 1)
                temp += line[i]
            else:
                if (temp != ""):
                    lst.append(temp) #add the previous accumulated
                    st.add(temp)
                lst.append(line[i]) # add the current
                col_offsets.append(i + 1)
                st.add(line[i])
                temp = ""

        else:
            if (temp == ""):
                col_offsets.append(i + 1)
            temp += line[i]
        i += 1
    else:  # else for the while loop
        if (temp != ""):
            lst.append(temp)
            st.add(temp)
    return lst, st, col_offsets



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
    if '+' in setTokens: lstMutations.append('ADD') # the only mutations coupled with other binary operators that are encompassed in a list to accomodate the operation name
    if '-' in setTokens: lstMutations.append('SUB')
    if '*' in setTokens: lstMutations.append('MUL')
    if '/' in setTokens: lstMutations.append('DIV')
    if '%' in setTokens: lstMutations.append('MOD')
    if '**' in setTokens: lstMutations.append('POW')
    if '//' in setTokens: lstMutations.append('FLOORDIV')

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
    if 'in' in setTokens: lstMutations.append('CR'); print("in"); print(setTokens)
    if 'not in' in setTokens: lstMutations.append('CR');  print("not in")
    if 'is not' in setTokens: lstMutations.append('CR'); print("is not")

    ############### LOOPS OPERATORS ################
    if 'for' in setTokens: lstMutations.extend(['OIL', 'RIL', 'ZIL', 'STD']) # one iteration loop, reverse iteration loop, zero iteration loop
    if 'while' in setTokens: lstMutations.extend(['OIL', 'RIL', 'ZIL', 'STD']) # added statement deletion
    if 'range' in setTokens: lstMutations.append('OIL')
    if 'enumerate' in setTokens: lstMutations.append('OIL')
    if 'zip' in setTokens: lstMutations.append('OIL')

    ################ CONDITIONAL OPERATORS ################
    if 'if' in setTokens: lstMutations.extend(['COI', 'STD'])

    ################ SLICE OPERATORS ################
    if ':' in setTokens: lstMutations.append('SIR')

    ################ BREAK AND CONTINUE ################
    if 'break' in setTokens: lstMutations.append('BCR')
    if 'continue' in setTokens: lstMutations.append('BCR')


    # if '()' in setTokens: lstMutations.append('MR')
    # if '[]' in setTokens: lstMutations.append('MR')
    # if '{}' in setTokens: lstMutations.append('MR')
    weights = [1] * len(lstMutations) # the weights are all equal for now

    return lstMutations, weights


def checkTypeInput(val):
    if val.startswith("\"") and val.endswith("\""): # I know that it is string explicitly
        val = re.sub(r"\"", "\\\"", val)
        val = re.sub(r"_", " ", val)
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








