import ast
import copy
import re
import sys
import time
import types


def segmentLine(line):
    segmentors = {' ', '(', ')', '[', ']', '{', '}', ':', ',', '='}
    i = 0
    ln = len(line)
    lst = []
    st = set()
    temp = ""
    while(i < ln):
        if (line[i] == " "): # I do not need spaces
            if (i - 1 != 0 and line[i - 1] != " "):
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
            while (line[i] != "\n"):
                i += 1
        elif (line[i] in segmentors):
            if (temp != ""):
                lst.append(temp)
                st.add(temp)
                temp = ""
            lst.append(line[i])
            st.add(temp)
        elif (line[i] == "-"): # Check if it is a unary sub
            if (i + 1 < ln and line[i + 1].isdigit()):
                temp += line[i]
            else:
                if (temp != ""):
                    lst.append(temp) #add the previous accumulated
                    st.add(temp)
                lst.append(line[i]) # add the current
                st.add(line[i])
                temp = ""

        else:
            temp += line[i]
        i += 1
    else:
        if (temp != ""):
            lst.append(temp)
            st.add(temp)
    return lst, st



def mutationsCanBeApplied(setTokens: set):
    """
    Iterate over the set of segmented parts in the faulty location and insert the mutations that can be applied
    Args: 
        setTokens: set of tokens in the faulty location
    Returns:
        list of mutations that can be applied
    """
    lstMutations = [] # list of mutations that can be applied
    if '+' in setTokens: lstMutations.append(('AR', 'ADD')) # the only mutations coupled with other binary operators that are encompassed in a list to accomodate the operation name
    # if '-' in setTokens: lstMutations.append('AR')
    # if '*' in setTokens: lstMutations.append('AR')
    # if '/' in setTokens: lstMutations.append('AR')
    # if '%' in setTokens: lstMutations.append('AR')
    # if '**' in setTokens: lstMutations.append('AR')
    # if '//' in setTokens: lstMutations.append('AR')
    # if '==' in setTokens: lstMutations.append('CR')
    # if '!=' in setTokens: lstMutations.append('CR')
    # if '<' in setTokens: lstMutations.append('CR')
    # if '>' in setTokens: lstMutations.append('CR')
    # if '<=' in setTokens: lstMutations.append('CR')
    # if '>=' in setTokens: lstMutations.append('CR')
    # if 'and' in setTokens: lstMutations.append('CR')
    # if 'or' in setTokens: lstMutations.append('CR')
    # if 'not' in setTokens: lstMutations.append('CR')
    # if 'is' in setTokens: lstMutations.append('CR')
    # if 'in' in setTokens: lstMutations.append('CR')
    # if 'not in' in setTokens: lstMutations.append('CR')
    # if 'is not' in setTokens: lstMutations.append('CR')
    # if '()' in setTokens: lstMutations.append('MR')
    # if '[]' in setTokens: lstMutations.append('MR')
    # if '{}' in setTokens: lstMutations.append('MR')
    weights = [1] * len(lstMutations) # the weights are all equal for now

    return lstMutations, weights







def notmutate(sth):
    return sth




def is_docstring(node):
    def_node = node.parent.parent
    return (isinstance(def_node, (ast.FunctionDef, ast.ClassDef, ast.Module)) and def_node.body and
            isinstance(def_node.body[0], ast.Expr) and isinstance(def_node.body[0].value, ast.Str) and
            def_node.body[0].value == node)




def sort_operators(operators):
    return sorted(operators, key=lambda cls: cls.name())


