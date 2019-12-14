import csv
from collections import Counter
import itertools as it
from _functools import reduce

with open('fp_data.txt', "rt", encoding='utf8') as f:
    reader = csv.reader(f)
    data = list(reader)


class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode  # needs to be updated
        self.children = {}
# increments the count variable with a given amount

    def inc(self, numOccur):
        self.count += numOccur
# display tree in text. Useful for debugging

    def disp(self, ind=1):
        print('     '*ind, self.name, '...', self.count)
        for child in self.children.values():
            child.disp(ind+1)


# rootNode = treeNode('pyramid', 9, None)
# rootNode.children['eye'] = treeNode('eye', 13, None)
# rootNode.disp()


def updateHeader(nodeToTest, targetNode):  # this version does not use recursion
    while (nodeToTest.nodeLink != None):  # Do not use recursion to traverse a linked list!
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode


def updateTree(items, inTree, headerTable, count):
    if items[0] in inTree.children:  # check if orderedItems[0] in retTree.children
        inTree.children[items[0]].inc(count)  # incrament count
    else:  # add items[0] to inTree.children
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        if headerTable[items[0]][1] == None:  # update header table
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
    if len(items) > 1:  # call updateTree() with remaining ordered items
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)


def createTree(dataSet, minSup=1):  # create FP-tree from dataset but don't mine
    headerTable = {}
    # go over dataSet twice
    for trans in dataSet:  # first pass counts frequency of occurance
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
    for k in list(headerTable):  # remove items not meeting minSup
        # print(f'{k} {headerTable[k]}')
        if headerTable[k] < minSup:
            del(headerTable[k])
    freqItemSet = set(headerTable.keys())
    # print 'freqItemSet: ',freqItemSet
    if len(freqItemSet) == 0:
        return None, None  # if no items meet min support -->get out
    for k in headerTable:
        # reformat headerTable to use Node link
        headerTable[k] = [headerTable[k], None]
    # print 'headerTable: ',headerTable
    retTree = treeNode('Root', 'Tree', None)  # create tree
    for tranSet, count in dataSet.items():  # go through dataset 2nd time
        localD = {}
        for item in tranSet:  # put transaction items in order
            if item in freqItemSet:
                localD[item] = headerTable[item][0]
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(
                localD.items(), key=lambda p: p[1], reverse=True)]
            # populate tree with ordered freq itemset
            updateTree(orderedItems, retTree, headerTable, count)
    return retTree, headerTable  # return tree and header table


def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[tuple(sorted(trans))] = 1
    return retDict


simpDat = data
# simpDat = loadSimpDat()
# print(simpDat)
initSet = createInitSet(simpDat)
# print(initSet)

support = 3
myFPtree, myHeaderTab = createTree(initSet, support)
print('FP-Tree:\n')
myFPtree.disp()


def ascendTree(leafNode, prefixPath):  # ascends from leaf node to root
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)


def findPrefixPath(basePat, treeNode):  # treeNode comes from header table
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1:
            condPats[tuple(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats


# def contains(w, t):
#     return any(w == e[0] for e in t)

# # print(data)
# # temp = {k[0]: k[1:] for k in data}
# # unique_data = list(dict.fromkeys(temp))
# print(myHeaderTab.keys())


for k in list(myHeaderTab.keys()):
    print(f'-----{k}-----')
    if findPrefixPath(k, myHeaderTab[k][1]):
        print(f'Conditional Patterns of {k}:')
        cp = findPrefixPath(k, myHeaderTab[k][1])
        print(f'{k} {cp}')
        # flat_cp = [element for tupl in cp for element in tupl]
        # counts = dict(Counter(flat_cp))

        sets = []
        for m, n in cp.items():
            count = m*n
            sets.append(count)

        flat_cp = [element for tupl in sets for element in tupl]
        counts = dict(Counter(flat_cp))
        
        print(f'{k}\'s condtional FP-Tree:')
        pats = {}
        for m, n in counts.items():
            if n >= support:
                pats.update({m: n})
        if pats:
            print(f'({pats}) | {k}')
        else:
            print('None found')
        
        k_perms = {}
        for q, r in myHeaderTab.items():
            if q == k:
                pats.update({k: r[0]})
                k_perms.update({k: r[0]})

        perms = []
        for i in range(2, len(pats.keys()) + 1):
            perms.append(tuple(it.combinations(pats.keys(), i)))
            flat_perms = [element for tupl in perms for element in tupl]

        
        for j in flat_perms:
            if k in j:
                k_perms.update({j: None})
                k_perms.update({k: None})

        # print(f'pats: {pats}')
        # print(f'k_perms: {k_perms}')
        for s, t in pats.items():
            for j, w in k_perms.items():
                if s in j and (w == None or t <= w):
                    k_perms[j] = t

        # print(k_perms)
        print(f'Frequent Patterns of {k}:')
        for x, z in k_perms.items():
            print(f'({x}:{z})')

    else:
        print('None found')
