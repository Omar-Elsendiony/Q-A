import ast
import copy
import re
import sys
import time
import types
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
    if 'and' in setTokens: lstMutations.append('ROR')
    if 'or' in setTokens: lstMutations.append('ROR')
    if 'not' in setTokens: lstMutations.append('ROR')

    ################ ASSIGNMENT OPERATORS ################
    if '==' in setTokens: lstMutations.append('ROR')
    if '!=' in setTokens: lstMutations.append('ROR')

    ################ LOGICAL OPERATORS ################
    if 'and' in setTokens: lstMutations.append('LOR')
    if 'or' in setTokens: lstMutations.append('LOR')
    if 'not' in setTokens: lstMutations.append('LOR')


    # if 'is' in setTokens: lstMutations.append('CR')
    # if 'in' in setTokens: lstMutations.append('CR')
    # if 'not in' in setTokens: lstMutations.append('CR')
    # if 'is not' in setTokens: lstMutations.append('CR')
    # if '()' in setTokens: lstMutations.append('MR')
    # if '[]' in setTokens: lstMutations.append('MR')
    # if '{}' in setTokens: lstMutations.append('MR')
    weights = [1] * len(lstMutations) # the weights are all equal for now

    return lstMutations, weights









