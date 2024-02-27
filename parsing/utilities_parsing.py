from queue import PriorityQueue
import ast
import re

""" iterate over the entire ast and make the height mapping function"""
def addHeightAttribute(node):
    max = 1
    # print("lll")
    for n in ast.iter_child_nodes(node):
        retHeight = 1 + addHeightAttribute(n)
        max = retHeight if retHeight > max else max
    node.height = max 
    return max


def is_leaf_node(node):
    """
    Yield all direct child nodes of *node*, that is, all fields that are nodes
    and all items of fields that are lists of nodes.
    """
    for name, field in ast.iter_fields(node):
        if isinstance(field, ast.AST):
            return True
        elif isinstance(field, list):
            for item in field:
                if isinstance(item, ast.AST):
                    return True
    return False


# addHeightAttribute(tree)

def parentify(tree):
    tree.parent = None
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node

# parentify(tree)



def ast_visit(node, level=0):
    # print(node.height)
    for field, value in ast.iter_fields(node):
        if isinstance(value, list):
            for item in value:
                if isinstance(item, ast.AST):
                    ast_visit(item, level=level+1)
        elif isinstance(value, ast.AST):
            ast_visit(value, level=level+1)

# ast_visit(tree)

def getHeight(node):
    return node.height

def descendants(node):
    return [n for n in ast.walk(node)][1:]

"""dice function to calculate the dice similarity between
 two trees based on the equation 2*|A ∩ B| / |A| + |B|"""
def dice(node1, node2, M):
    # print(node1.height)
    # print(node2.height)
    # yield the list of descendants of the node exlude the node itself
    def descendants(node):
        return [n for n in ast.walk(node)][1:]
    set1 = set(descendants(node1))
    set2 = set(descendants(node2))
    Interesection = len(set1.intersection(set2))
    return 2*Interesection / (len(set1) + len(set2))



setIgnore = set(['lineno', 'col_offset', 'ctx', 'end_col_offset', 'height', 'parent'])
def compare_ast(node1, node2):
    if type(node1) is not type(node2):
        return False
    if isinstance(node1, ast.AST):
        for k, v in vars(node1).items():
            if k in setIgnore:
                continue
            if not compare_ast(v, getattr(node2, k)):
                return False
        return True
    elif isinstance(node1, list):
        return (all(compare_ast(n1, n2) for n1, n2 in zip(node1, node2)))
    else:
        return node1 == node2


def peekMax(listPriority: PriorityQueue):
    if (not listPriority.empty()):
        item = listPriority.get()
        height = item[0]
        listPriority.put(item)
        return height
    return 0

def popUtility(listPriority: PriorityQueue):
    try:
        listPopped = []
        firstItem = listPriority.get()
        heightMax = firstItem[0]
        listPopped.append(firstItem[2])
        # start of getting the items
        if (listPriority.empty()): return listPopped
        otherItem = listPriority.get()
        while (otherItem[0] == heightMax):
            listPopped.append(otherItem[2])
            if (not listPriority.empty()):
                otherItem = listPriority.get()
            else:
                break
        else:
            listPriority.put(otherItem)
        return listPopped
    except Exception as e:
        print(e)



def checkOtherT(t1, t2, T):
    """check if there is other occurance of t1 in tree T that is not T2"""
    # traverse the tree
    isIsomorphic = False
    if (T != t2):
        compare_ast(t1, T)
    for tx in ast.iter_child_nodes(T):
        if (tx != t2): isIsomorphic = compare_ast(t1, tx)
        if (isIsomorphic): return True
    for tx in ast.iter_child_nodes(T):
        isIsomorphic = checkOtherT(t1, t2, tx)
        if (isIsomorphic): return True
    return isIsomorphic


def descendants(node):
    """return the list of descendants of the node and if there is no descendants return None"""
    return [n for n in ast.walk(node)][1:] if is_leaf_node(node) else None

def postordertraversal(node, listNodes):
    for child in ast.iter_child_nodes(node):
        postordertraversal(child, listNodes)
    listNodes.append(node)