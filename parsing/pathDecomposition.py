parentChild = {"A": ["B", "C"], "B":[], "C": ["D", "E","G"],
                "D": [], "E": ["F"], "F": [], "G": []}

root = "A" # you have to know the root of the tree
tree = [[root]]
tempTree = []

def subtree(parent, parentChild):
    tempTree = []
    for child in parentChild.get(parent):
        tempTree.append(child)
    return tempTree

def drawTree(levels, parentChild):
    # dedfine subtree and subforest
    level = []
    children = []
    for parent in levels[-1]:
        for child in parentChild.get(parent):
            children.append(child)
            level += subtree(child, parentChild)
    levels.append(children)
    levels.append(level)
    drawTree(levels, parentChild) if level else None
    
drawTree(tree, parentChild)
# print(tree)


def printTree(tree):
    for level in tree:
        for node in level:
            print(node, sep="", end=" ")
        print("\n")

# printTree(tree)

setPath = set()
def getLeftPath(parentChild, root, setPath):
    node = root
    while node:
        setPath.add(node)
        nodeList = parentChild.get(node)
        node = nodeList[0] if nodeList else None
getLeftPath(parentChild, root, setPath) # setPath is changed in place
# print(setPath)


def leftPathDecomposition(parentChild):
    # dedfine subtree and subforest
    leftPath = {"A", "B"}
    for parent in parentChild:
        for child in parentChild[parent]:
            leftPath[child] = parent
    return leftPath




def getNumberDescendants(parentChild, root):
    """
    inputs: parentChild: dictionary, root: string
    outputs: int
    """
    if not parentChild.get(root):
        return 0
    else:
        return sum([getNumberDescendants(parentChild, child) for child in parentChild.get(root)]) + len(parentChild.get(root))

print(getNumberDescendants(parentChild, root))



""" number of relevant subforests equals to the number of relevant subtrees nodes summed"""
def relevantSubtrees():
    pass

