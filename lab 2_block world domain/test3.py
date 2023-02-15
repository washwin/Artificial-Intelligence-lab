startState = [['A', 'B', 'GROUND'], ['C', 'GROUND'], ['GROUND']]
goalState = [['B', 'GROUND'], ['A','GROUND'], ['C', 'GROUND']]
stateDict = {}
goalDict = {}

def makeDict(currentState):
    stateDict.clear()
    for i in range(3):
        for j in range(len(currentState[i])-1):
            stateDict[currentState[i][j]]=currentState[i][j+1]
            
    for i in range(3):
        for j in range(len(currentState[i])-1):
            goalDict[goalState[i][j]]=goalState[i][j+1]
           

def heuristic1(currentState):
    value = 0
    makeDict(currentState)
    for x in currentState:
        for y in x:
            if y=="GROUND":
                continue
            if str(stateDict[y])==str(goalDict[y]):
                value = value+1
            else:
                value = value-1
    return value

def heuristic2(currentState):
    value = 0
    for i in range(3):
        for j in range(len(currentState[i])-1):
            if currentState[i][j:]==goalState[0][j:] or currentState[i][j:]==goalState[1][j:] or currentState[i][j:]==goalState[2][j:]:
                value = value + len(currentState[i]) - j - 2
            else:
                value = value - len(currentState[i]) + j + 2
    return value

print(heuristic1(startState))