#!/usr/bin/env python
# coding: utf-8

# In[1]:


#variables:
#name of the node, a count
#nodelink used to link similar items
#parent vaiable used to refer to the parent of the node in the tree
#node contains an empty dictionary for the children in the node
#from itertools import combinations
import time
class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode      #needs to be updated
        self.children = {} 
#increments the count variable with a given amount    
    def inc(self, numOccur):
        self.count += numOccur
#display tree in text. Useful for debugging        
    def disp(self, ind=1):
        print ('  '*ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.disp(ind+1)

def createTree(dataSet, minSup=1):#create FP-tree from dataset but don't mine
    headerTable = {}
    #go over dataSet twice
    for trans in dataSet:#first pass counts frequency of occurance
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
    for k in list(headerTable):  #remove items not meeting minSup
        if headerTable[k] < minSup: 
            del(headerTable[k])
    #print(type(headerTable))
    freqItemSet = set(headerTable.keys())
    #print ('freqItemSet: ',freqItemSet)
    if len(freqItemSet) == 0: return None, None  #if no items meet min support -->get out
    for k in headerTable:
        headerTable[k] = [headerTable[k], None] #reformat headerTable to use Node link 
    #print ('headerTable: ',headerTable)
    retTree = treeNode('Null Set', 1, None) #create tree
    for tranSet, count in dataSet.items():  #go through dataset 2nd time
        localD = {}
        for item in tranSet:  #put transaction items in order
            if item in freqItemSet:
                localD[item] = headerTable[item][0]
        #print(localD)
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[0], reverse=True)]
            updateTree(orderedItems, retTree, headerTable, count)#populate tree with ordered freq itemset
    return retTree, headerTable #return tree and header table


def updateTree(items, inTree, headerTable, count):
    if items[0] in inTree.children:#check if orderedItems[0] in retTree.children
        inTree.children[items[0]].inc(count) #incrament count
    else:   #add items[0] to inTree.children
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        if headerTable[items[0]][1] == None: #update header table 
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
    if len(items) > 1:#call updateTree() with remaining ordered items
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)


def updateHeader(nodeToTest, targetNode):   #this version does not use recursion
    while (nodeToTest.nodeLink != None):    #Do not use recursion to traverse a linked list!
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode
    
def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = 1
    return retDict

def ascendTree(leafNode, prefixPath): #ascends from leaf node to root
    #if leafNode.parent != None:
        #prefixPath.append(leafNode.name)
        #ascendTree(leafNode.parent, prefixPath)
    while leafNode.parent !=None:
        prefixPath.append(leafNode.name)
        leafNode=leafNode.parent


def findPrefixPath(basePat, treeNode): #treeNode comes from header table
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1: 
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats


def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
    #print("minetree:",headerTable,minSup,preFix,freqItemList)
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[0])]
    #print(bigL)
    for basePat in bigL:
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        if len(newFreqSet)>5:
            return
        freqItemList.append(newFreqSet)
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        #Not this one then next one
        #print(condPattBases," ",newFreqSet)
        myCondTree, myHead = createTree(condPattBases, minSup)
        if myHead != None: # 用於測試 
            #print('conditional tree for:', newFreqSet)
            #myCondTree.disp()
            mineTree(myCondTree, myHead, minSup, newFreqSet,freqItemList)
            
def fpGrowth(dataSet, minSup=30):
    initSet = createInitSet(dataSet)
    #print(initSet)
    myFPtree, myHeaderTab = createTree(initSet, minSup)
    freqItems = []
    #asociationlist=[]
    mineTree(myFPtree, myHeaderTab, minSup, set([]), freqItems)
    return freqItems
def loadFileDat():
    fileDat = []
    with open('tags2.dat','r',encoding="utf-8") as fp:
        for line in fp :
            lineDat = line.split(' ')
            fileDat.append(lineDat[:-1])
    return fileDat
a=time.time()
freqItems = []
dataSet = loadFileDat()
freqItems = fpGrowth(dataSet)
b=time.time()
print('處理程序耗時: {} 秒'.format(b-a))
print("total freqItemSet that item<5: ",len(freqItems))
sum=[0,0,0,0,0]
for i in freqItems:
    sum[len(i)-1]+=1
    print (i)
print("1~5items freqItemSet count: ",sum)


# In[ ]:





# In[ ]:





# In[ ]:




