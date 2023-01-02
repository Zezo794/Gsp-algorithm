import itertools
dataSet = [['A', 'B', 'FG', 'C', 'D'],
           ['B', 'G', 'D'],
           ['B', 'F', 'G', 'AB'],
           ['F', 'AB', 'C', 'D'],
           ['A', 'BC', 'G', 'F', 'DE']]
    
minSprt = 40
def cnt_min_sprt(itemList):
    minSupport = minSprt/100 * len(dataSet)
    # initialize counter dictionary
    dicCnt = {}
    for i in itemList :
        dicCnt[i] = 0
    
    # count support of each element
    for item in itemList :
        for data in dataSet :
            pos = 0
            checkLength = 0
            if type(item) is tuple :
                for i in range(len(item)) :
                    while pos < len(data) :
                        if data[pos].find(item[i]) != -1 :
                            pos += 1
                            checkLength +=1
                            break
                        pos +=1
                    if checkLength == len(item):
                        dicCnt[item] +=1
                        break
                    elif checkLength == 0:
                        break
            else:
                while pos < len(data):
                    if data[pos].find(item) != -1:
                        dicCnt[item] +=1
                        break
                    else :
                        pos +=1

    # filter item that < min_support
    itemSet2 = {}
    itemList2 = []
    for value,cntr in dicCnt.items() :#items
        if cntr >= minSupport :
            itemSet2[value] = cntr
    
    for k in itemSet2.keys():
        itemList2.append(k)
    
    # return final list
    return itemList2,itemSet2 

def separate_items():
    chars=""
    for dat in dataSet:
        for element in dat:
            chars+=element
    list1=list(chars)
    list1=set(list1)
    l1 = list(list1)
    l1.sort()
    return(l1)  
    

def join_tow_items(itemList):
    # build matrix 1
    fMatrix = [i for i in itertools.product(itemList, repeat=2)]
    # matrix1 = [tuple(i) for i in matrix1]
    # build matrix 2
    resOfCom = itertools.combinations(itemList, 2)
    sMatrix = list(resOfCom)
    sMatrix = [f"{i[0]}{i[1]}" for i in sMatrix]
    tMatrix = fMatrix + sMatrix
    return tMatrix

def join_threeoOrMore_items(itemList):
    #print("----------------------test 1----------------------")
    #print(itemList)
    itemList3 = []
    for firstItem in itemList :
        for secItem in itemList:
            if type(secItem) is tuple and type(firstItem) is tuple :
                #first case
                if len(firstItem[0]) == 1 and len(secItem[-1]) == 1 :
                    if firstItem[1:] == secItem[:len(secItem)-1]:
                        listn = [i for i in firstItem]
                        itemList3.append(tuple(listn+list(secItem[-1])))
                # second case
                elif len(firstItem[0]) == 1 and len(secItem[-1]) != 1:
                    tmp = list(secItem)
                    #print("----------------------test 2----------------------")
                    #print(tmp)
                    #print(tmp[-1])
                    tmp[-1] = tmp[-1][:len(tmp)-1]
                    #print("----------------------test 3----------------------")
                    #print(tmp[-1])
                    tmp = tuple(tmp)
                    #print("----------------------test 4----------------------")
                    #print(tmp)
                    if firstItem[1:] == tmp[0:]:
                        listn = [i for i in firstItem[len(firstItem)-1]]
                        itemList3.append(tuple(listn+list(secItem[-1])))

                #third case
                elif len(firstItem[0]) != 1 and len(secItem[-1]) == 1:
                    tmp = list(firstItem)
                    tmp[0]= tmp[0][1:]
                    tmp = tuple(tmp)
                    if tmp[0:] == secItem[:len(secItem)-1]:
                        listn = [i for i in firstItem]
                        itemList3.append(tuple(listn+list(secItem[-1])))

                # forth case
                else : #(BC,A) + (C,AB)
                    tempItem = list(firstItem)
                    tempItem[0] = tempItem[0][1:]
                    tempItem = tuple(firstItem)
                    tempItem2 = list(secItem)
                    tempItem2[-1] = tempItem2[-1][:len(tempItem2) - 1]
                    tempItem2 = tuple(secItem)
                    if tempItem[0:] == tempItem2[0:]:
                        itemList3.append(tuple([firstItem[0], secItem[1:]]))

            elif type(secItem) is not tuple and type(firstItem) is tuple: # (A , B) + (AB)
                # first case
                if len(firstItem[0]) == 1 :
                    #print("----------------------test 4----------------------")
                    #print(firstItem[1:])
                    if firstItem[1:][0] == secItem[:len(secItem)-1] :
                        itemList3.append(tuple([firstItem[0], secItem]))
                # second case
                elif len(firstItem[0]) != 1 :
                    tmp = list(firstItem)
                    tmp[0]= tmp[0][1:]
                    tmp = tuple(tmp)
                    if tmp[0:][0] == secItem[:len(secItem)-1] :
                        itemList3.append(tuple([firstItem[0], secItem]))

            elif type(secItem) is  tuple and type(firstItem) is not tuple:
                #first case
                if  len(secItem[-1])==1 :
                    if firstItem[1:] == secItem[:len(secItem)-1][0] :
                        itemList3.append(tuple([firstItem , secItem[-1]]))
                # second case
                elif  len(secItem[-1]) != 1:
                    tmp = list(secItem)
                    tmp[-1] = tmp[-1][:len(tmp)-1]
                    tmp = tuple(tmp)
                    if firstItem[1:] == tmp[0:][0] :
                        itemList3.append(tuple([firstItem, secItem[-1]]))

    itemSet3 = set(itemList3)
    itemList3 = list(itemSet3)
    itemList3.sort()
    return itemList3

def finalRes():
    cnt = 3
    # print first sequences
    L1 = separate_items()
    oneSeqList, oneSeqDic = cnt_min_sprt(L1)
    print("1-sequences")
    print(oneSeqDic)

    # print second sequences
    L2 = join_tow_items(oneSeqList)
    twoSeqList, twoSeqDic = cnt_min_sprt(L2)
    print("2-sequences")
    print(twoSeqDic)

    # print third or more sequences
    L3 = join_threeoOrMore_items(twoSeqList)
    threeOrMoreSeqList, threeOrMoreSeqDic = cnt_min_sprt(L3)
    print("3-sequences")
    print(threeOrMoreSeqDic)
    while len(threeOrMoreSeqList) != 0:
        L_More = join_threeoOrMore_items(threeOrMoreSeqList)
        threeOrMoreSeqList, threeOrMoreSeqDic = cnt_min_sprt(L_More)
        if(len(threeOrMoreSeqList) != 0):
            cnt += 1
            print(f"{cnt}""-sequences")
            print(threeOrMoreSeqDic)

finalRes()
