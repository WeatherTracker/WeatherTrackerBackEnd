from pymongo import MongoClient
import time
import collections
import datetime
import math
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
        retDict[frozenset(trans)] = 0
    for trans in dataSet:
        retDict[frozenset(trans)] +=1
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
            
def fpGrowth(dataSet, minSup=10):
    initSet = createInitSet(dataSet)

    myFPtree, myHeaderTab = createTree(initSet, minSup)
    freqItems = []
    #asociationlist=[]
    mineTree(myFPtree, myHeaderTab, minSup, set([]), freqItems)
    return freqItems
def loadFileDat():
    fileDat = []
    client = MongoClient("localhost", 27017)
    availableEvent=client.event.pastEvent.find()
    for i in availableEvent:
        FPnode=[]
        FPnode.append(i.get('staticHobbyTag'))
        tags=i.get('dynamicTags')
        FPnode=FPnode+tags
        #FPnode.append(tags)
        fileDat.append(FPnode)
    return fileDat
def fp_recommend(dynamicTagList):
    a=time.time()
    freqItems = []
    dataSet = loadFileDat()
    freqItems = fpGrowth(dataSet)
    b=time.time()
    print('處理程序耗時: {} 秒'.format(b-a))
    print("total freqItemSet that item<5: ",len(freqItems))
    sum=[0,0,0,0,0]
    hobbyList=["健行","賞鳥","散步","旅遊","賽車","開車兜風","騎單車",'網球','羽球','博弈','桌球',"聚餐","釣魚",
    "游泳","水上活動","拖曳傘","撞球","保齡球","棒球","籃球","高爾夫球","排球","打拳","靜坐","有氧","健身","瑜珈","登山"
    ,"健行","慢跑","跑步","彈奏樂器","舞蹈","攝影","書法","藝文展覽","表演欣賞","手工藝","閱讀","園藝","上網","電競","桌遊"
    "益智遊戲","密室逃脫","博弈","電視","錄影帶","電影","KTV","聽音樂","泡湯","SPA","按摩","遊樂園","娛樂中心","逛街購物",
    "下午茶","禮拜","團康","親子活動","打掃","睡覺","做家事"]
    freqItems.reverse()
    freqItems=sorted(freqItems, reverse=True,key= len)
    recommendlist=[]
    for i in freqItems:
        s2=set(hobbyList)
        s1=set(i)
        if(s1&s2 and len(i)>=1):
            sum[len(i)-1]+=1
            s1copy=s1.copy()
            staticTag=""
            for j in s1:
                if (j in s2):
                    s1copy.remove(j)
                    staticTag=j
            if(collections.Counter(s1copy)==collections.Counter(dynamicTagList)):
                recommendlist.append(staticTag)
    return recommendlist
                
def fp_recommendList(lat,lon):
    recommendEventList7day=[]
    recommendEventList=[]
    client = MongoClient("localhost", 27017)
    #locationData=client.station.CWB_3Days.find_one({'city':city})
    #every3hourData=locationData.get('locations').get(location).get('times_3HR_point')
    currentEventList=client.event.currentEvent.find()
    #for i in every3hourData:
    #    tags=[]
    #    data=i.get('data')
    #    for j in data:
    #        if(j.get('tag')):
    #            tags.append(j.get('tag'))
    #    if(len(tags)>0):
    #        recommendTypes=fp_recommend(tags)
    #        print(recommendTypes)
    #    dataTime=i.get('dataTime')

    for i in currentEventList:
        startTimeLeft=(i.get('startTime')-datetime.datetime.today()).total_seconds()
        if(startTimeLeft<604800 and len(i.get('dynamicTags'))>0):
            tags=i.get('dynamicTags')
            recommendTypeList=fp_recommend(tags)
            print(recommendTypeList)
            if(i.get('staticHobbyTag')in recommendTypeList):
                i['recommendLevel']=recommendTypeList.index(i.get('staticHobbyTag'))+1
                recommendEventList.append(i)
    recommendEventList.sort(key=lambda x: abs(float(lat)-x.get("latitude"))**(2)+abs(float(lon)-x.get("longitude"))**(2))
    recommendEventList.sort(key=lambda x: x.get('recommendLevel'))
    for i in recommendEventList:
        i.pop('recommendLevel')
        i.pop("_id")
    
    return recommendEventList