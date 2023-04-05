import sys
import copy
import math

text=open(sys.argv[1],'r').read().split('\n')
for i in range(0,len(text)):
    text[i]=text[i].split('\t')
if [''] in text:
    text.remove([''])

temlist=[]
for i in range(1,len(text)):
    dict=copy.deepcopy({})
    for j in range(0,len(text[0])):
        dict[text[0][j]]=text[i][j]
    temlist.append(copy.deepcopy(dict))

nn=text[0][-1]
attributeList=copy.deepcopy(text[0])
attributeList.remove(nn)

def calcEntropy(passedList1):
    temset=copy.deepcopy(set([]))
    for i in passedList1:
        temset.add(i[nn])
    temset=copy.deepcopy(list(temset))
    temsetcount=copy.deepcopy({})
    for i in temset:
        temsetcount[i]=0
    for i in passedList1:
        temsetcount[i[nn]]+=1
    entropy=0
    for i in temsetcount.keys():
        entropy-=(temsetcount[i]/len(passedList1))*math.log2(temsetcount[i]/len(passedList1))
    return entropy

def inforGain(passedList2,attribute):
    temset = copy.deepcopy(set([]))
    for i in passedList2:
        temset.add(i[attribute])
    temset = copy.deepcopy(list(temset))
    temsetcount = copy.deepcopy({})
    for i in temset:
        temsetcount[i] = 0
    for i in passedList2:
        temsetcount[i[attribute]] += 1
    infoGain=calcEntropy(passedList2)
    for i in temsetcount.keys():
        temlist1=copy.deepcopy([])
        for j in passedList2:
            if j[attribute]==i:
                temlist1.append(j)
        infoGain-=(temsetcount[i]/len(passedList2))*calcEntropy(temlist1)
    return infoGain

answerdict={}

def id3(passedList,attributeList1):
    if calcEntropy(passedList)==0:
        returndict=copy.deepcopy({})
        returndict[nn]=passedList[0][nn]
        return returndict
    if len(attributeList1)==0:
        temset1=copy.deepcopy([])
        for i in passedList:
            temset1.append(i[nn])
        temset1=copy.deepcopy(set(temset1))
        temset1=copy.deepcopy(list(temset1))
        temsetcount=copy.deepcopy({})
        for i in temset1:
            temsetcount[i]=0
        for i in passedList:
            temsetcount[i[nn]]+=1
        temvarcount=-1
        for i in temsetcount.keys():
            if temsetcount[i]>temvarcount:
                temvarcount=temsetcount[i]
                outputanswer=i
        returndict=copy.deepcopy({})
        returndict[nn]=outputanswer
        return returndict

    temValue=0
    temAttribute=attributeList1[0]
    for i in attributeList1:
        if inforGain(passedList,i)>temValue:
            temValue=inforGain(passedList,i)
            temAttribute=i
    temAttributeList=copy.deepcopy(attributeList1)
    temAttributeList.remove(temAttribute)
    # print(attributeList1)
    temset = copy.deepcopy(set([]))
    for i in passedList:
        temset.add(i[temAttribute])
    temset = copy.deepcopy(list(temset))
    returndict=copy.deepcopy({})
    for i in temset:
        temlist2=copy.deepcopy([])
        for j in passedList:
            if j[temAttribute]==i:
                temlist2.append(j)
        returndict[(temAttribute,i)]=id3(temlist2,temAttributeList)
    return returndict

answerdict=id3(temlist,attributeList)
tabval=0
sampledict={
    'samplekey':'samplevalue'
}


def printAnswer(dictPrint,tabval):
    for i in dictPrint.keys():
        for k in range(0,tabval):
            print('\t',end='')
        if type(sampledict) == type(dictPrint[i]):
            print(i[0],"=",i[1],":")
        else:
            print(i,"=",dictPrint[i])
        if type(sampledict) == type(dictPrint[i]):
            printAnswer(dictPrint[i],tabval+1)

printAnswer(answerdict,0)