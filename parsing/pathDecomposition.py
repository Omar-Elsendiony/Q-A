parentChild = {"A": ["B", "C"], "B":[], "C": ["D", "E","G"], "D": [], "E": ["F"], "F": [], "G": []}

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
print(tree)


def printTree(tree):
    for level in tree:
        for node in level:
            print(node, sep="", end=" ")
        print("\n")

printTree(tree)

def getLeftPath(parentChild):
    # dedfine subtree and subforest
    leftPath = {"A", "B"}
    for parent in parentChild:
        for child in parentChild[parent]:
            leftPath.add(child)
    return leftPath


def leftPathDecomposition(parentChild):
    # dedfine subtree and subforest
    leftPath = {"A", "B"}
    for parent in parentChild:
        for child in parentChild[parent]:
            leftPath[child] = parent
    return leftPath