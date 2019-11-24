def loadDataSet():
    # data_set = [[1, 5], [1, 3, 4], [2, 3, 5], [1, 2, 3], [1, 3, 4], [2, 3, 4], [1, 4]]
    data_set = [{2, 3, 4}, {1, 3, 5, 6}, {1, 2, 3, 5}, {1, 3, 5}]
    return data_set


def getC1(dataSet):  # 创建1项集
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            # print(item)
            if {item} not in C1:
                C1.append({item})
    # C1.sort()
    # print(C1)
    ls = list(map(frozenset, C1))
    # print(ls)
    return ls


def selectProperDict(minSupport, Ck, dataSet):
    sel_dict = {}
    proper_list = []  # 频繁项集
    rest_list = []
    supported_dict = {}
    for trans in dataSet:
        for c in Ck:
            if c.issubset(trans):
                if c in sel_dict:
                    sel_dict[c] += 1
                else:
                    sel_dict[c] = 1
    # print(sel_dict)
    # 筛选支持度大于给定支持度的元素
    for key in sel_dict:
        support = sel_dict[key] / len(dataSet)
        # print(support)
        if support >= minSupport:
            proper_list.append(key)
            supported_dict[key] = support
        else:
            rest_list.append(key)

    return proper_list, supported_dict, rest_list


def getSupSet(Lk, k):
    SupSet = []
    for i in range(len(Lk)):
        for j in range(1, len(Lk)):
            if Lk[i] != Lk[j]:
                item = Lk[i].union(Lk[j])
                if (item not in SupSet) and (len(item) == k):
                    SupSet.append(item)
    # print(SupSet)
    return SupSet


def apriori(dataSet, minSupport):
    C1 = getC1(dataSet)
    k = 2
    L1, L1_sup, rest = selectProperDict(minSupport, C1, dataSet)
    Lk_sup = {}
    list_data = L1
    L = [L1]
    L_sup = L1_sup
    # print(len(list_data))
    # print(L1, L1_sup, rest)
    while len(list_data) > 1:
        Ck = getSupSet(list_data, k)
        Lk, Lk_sup, restk = selectProperDict(minSupport, Ck, dataSet)
        rest += restk
        # print(Lk, Lk_sup, rest)
        k += 1
        list_data = Lk
        L = L + [Lk]
        L_sup.update(Lk_sup)
    return L, L_sup


def generateRules(L, L_sup, minConf):
    ruleList = []
    for i in range(1, len(L)):
        # print(L[0])
        for freqSet in L[i]:
            # print(freqSet)
            newSet = []
            for item in freqSet:
                newSet.append(frozenset({item}))
            if i > 1:
                rulesMerge(freqSet, newSet, L_sup, ruleList, minConf)
            else:
                calcConf(freqSet, newSet, L_sup, ruleList, minConf)
            # print(newSet)
    return ruleList


# 获得满足最小可信度的关联规则
def calcConf(freqSet, newSet, L_sup, rl, minConf):
    prunedH = []
    for con in newSet:
        conf = L_sup[freqSet] / L_sup[freqSet - con]  # 计算置信度
        # print(con)
        if conf >= minConf:
            print(freqSet - con, '-->', con, 'conf:', conf)
            rl.append((freqSet - con, con, conf))
            prunedH.append(con)
    return prunedH


# 生成候选规则集合
def rulesMerge(freqSet, newSet, L_sup, rl, minConf):
    m = len(newSet[0])
    if len(freqSet) > (m + 1):  # 尝试进一步合并
        merged = getSupSet(newSet, m + 1)
        merged = calcConf(freqSet, merged, L_sup, rl, minConf)
        if len(merged) >= 2:
            rulesMerge(freqSet, merged, L_sup, rl, minConf)


if __name__ == "__main__":
    minSupport = 0.6
    minconf = 0.8
    dataSet = loadDataSet()
    # print(apriori(dataSet, minSupport))
    L, L_sup = apriori(dataSet, minSupport)
    print(L)
    print(L_sup)
    generateRules(L, L_sup, minconf)
