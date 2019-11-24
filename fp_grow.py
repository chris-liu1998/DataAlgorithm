class FPTreeNode:
    def __init__(self, name, parent, count):
        self.name = name  # 节点名
        self.parent = parent  # 父节点
        self.children = {}  # 子节点
        self.count = count  # 频率
        self.nextSamelink = None  # 节点间的链接

    def addCount(self, countChange):
        self.count += countChange

    def display(self, index):  # 文本显示
        print(' ' * index, self.name, ' ', self.count)
        for child in self.children.values():
            child.display(index + 1)


def loadData():
    data_set = [['A', 'B', 'D', 'E', 'C'],
                ['A', 'E', 'D', 'C'],
                ['A', 'B', 'D'],
                ['E', 'F', 'A', 'G'],
                ['A', 'C', 'B', 'E']]
    return data_set


def processDataSet(dataSet):
    newDataSet = {}
    for trans in dataSet:
        trans.sort()
        # print(trans)
        newDataSet[frozenset(trans)] = 1
    print(newDataSet)
    return newDataSet
    # for trans in dataSet:
    #     for item in trans:
    #         if item in deletedk:
    #             trans.remove(item)


def createHeaderTable(dataSet, minSup):  # 创建头指针表
    headerTable = {}
    deleted_key = []
    for trans in dataSet:
        for item in trans:
            if item in headerTable:
                headerTable[item] += 1
            else:
                headerTable[item] = 1
    for key in list(headerTable.keys()):
        if headerTable[key] < minSup:
            del headerTable[key]
            deleted_key.append(key)
    # print(headerTable)
    for key in headerTable:
        headerTable[key] = [headerTable[key], None]  # 初始状态，没有连接节点
    # print(dataSet.items())

    return headerTable


def createTree(headerT, dataSet):
    fpTree = FPTreeNode('NULL', None, 1)  # 创建根节点
    for trans, count in dataSet.items():
        freqItemC = {}
        orderItems = []
        for item in list(headerT.keys()):
            if item in trans:
                freqItemC[item] = headerT[item][0]
        if len(freqItemC) > 0:
            orderlist = sorted(freqItemC.items(), key=lambda p: (p[1], p[0]), reverse=True)
            for i in orderlist:
                orderItems.append(i[0])
            # print(orderItems)
            # print(count)
            addNodes(fpTree, headerT, orderItems, count)
    return fpTree


def addNodes(lastTreeNode, headerT, orderItems, count):  # 添加节点
    for item in orderItems:
        if item not in lastTreeNode.children:
            lastTreeNode.children[item] = FPTreeNode(item, lastTreeNode, count)
            if headerT[item][1] is not None:
                while headerT[item][1].nextSamelink is not None:
                    headerT[item][1] = headerT[item][1].nextSamelink
                headerT[item][1].nextSamelink = lastTreeNode.children[item]
            else:
                headerT[item][1] = lastTreeNode.children[item]
        else:
            lastTreeNode.children[item].addCount(count)
        lastTreeNode = lastTreeNode.children[item]


def ascendTree(node, prefixPath):
    if node.parent is not None:
        prefixPath.append(node.name)
        ascendTree(node.parent, prefixPath)


def mineTree(freqSet, fpTree, minSupport, header, prefix):
    sortedHeaderTable = sorted(header.items(), key=lambda p: p[1][0])  # 返回重新排序的列表
    freq = []
    for head in sortedHeaderTable:
        freq.append(head[0])  # 获取频繁项
    for basePat in freq:
        newFreqSet = prefix.copy()  # 新的频繁项集
        newFreqSet.add(basePat)
        freqSet.append(newFreqSet)  # 所有的频繁项集列表

        condPattBases = {}  # 存储条件模式基
        while header[basePat][1] is not None:
            prefixPath = []  # 用于存储前缀路径
            ascendTree(header[basePat][1], prefixPath)  # 生成前缀路径
            if len(prefixPath) > 1:
                condPattBases[frozenset(prefixPath[1:])] = header[basePat][1].count
            header[basePat][1] = header[basePat][1].nextSamelink  # 遍历下一个相同元素
            # print(condPattBases)
        newHeader = createHeaderTable(condPattBases, minSupport)
        # 创建条件FP树
        conditionTree = createTree(newHeader, condPattBases)

        if newHeader is not None:
            print('conditional tree for:', newFreqSet)
            conditionTree.display(1)
            mineTree(freqSet, conditionTree, minSupport, newHeader, newFreqSet)  # 递归直到不再有元素


if __name__ == "__main__":
    minSupport = 1
    freqSet = []
    prefix = set([])
    dataSet = processDataSet(loadData())
    header = createHeaderTable(dataSet, minSupport)
    fpTree = createTree(header, dataSet)
    fpTree.display(1)
    mineTree(freqSet, fpTree, minSupport, header, prefix)
    print(freqSet)
