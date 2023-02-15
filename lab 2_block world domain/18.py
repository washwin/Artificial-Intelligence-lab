import time
startState = [['A', 'B', 'C','GROUND'], ['GROUND'], ['D','GROUND']]
goalState = [['C','GROUND'], ['A', 'GROUND'], ['B','D','GROUND']]
stateDict = {}
goalDict = {}

def inputTerminal():
    print("Welcome to Block World Domain")
    print("Here you have to enter a start state and a goal state")
    print("There are 3 stacks in each state")
    print("Enter unique characters for each block")
    print("Enter ! to change a stack")
    print("Start State:")
    block = []
    startState.clear()
    goalState.clear()
    for i in range(1,4):
        print("Stack ",i)
        j = 1
        while True:
            x = input()
            if x=="!":
                break
            block.append(x)
            j = j+1
        block.append("GROUND")
        startState.append(list(block))
        block.clear()

    print(startState)
    print("Goal State:")
    for i in range(1,4):
        print("Stack ",i)
        j = 1
        block.append("#")
        while True:
            x = input()
            if x=="!":
                break
            block.append(x)
            j = j+1
        startState.append(list(block))
        block.clear()
        
        
def makeDict(currentState):
    stateDict.clear()
    for i in range(3):
        for j in range(len(currentState[i])-1):
            stateDict[currentState[i][j]]=currentState[i][j+1]
            
    for i in range(3):
        for j in range(len(goalState[i])-1):
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

def moveGen(currentState):
    moves = []
    tempState = []
    if len(currentState[0])!=1:
        tempState = currentState.copy()
        l1 = list(tempState[0])
        top = l1.pop(0)
        tempState[0] = l1
        l2 = list(tempState[1])
        l2.insert(0, top)
        tempState[1] = l2
        moves.append(tempState)
        
        tempState = currentState.copy()
        l1 = list(tempState[0])
        top = l1.pop(0)
        tempState[0] = l1
        l2 = list(tempState[2])
        l2.insert(0, top)
        tempState[2] = l2
        moves.append(tempState)
        
    if len(currentState[1])!=1:
        tempState = currentState.copy()
        l1 = list(tempState[1])
        top = l1.pop(0)
        tempState[1] = l1
        l2 = list(tempState[0])
        l2.insert(0, top)
        tempState[0] = l2
        moves.append(tempState)
        
        tempState = currentState.copy()
        l1 = list(tempState[1])
        top = l1.pop(0)
        tempState[1] = l1
        l2 = list(tempState[2])
        l2.insert(0, top)
        tempState[2] = l2
        moves.append(tempState)

    if len(currentState[2])!=1:
        tempState = currentState.copy()
        l1 = list(tempState[2])
        top = l1.pop(0)
        tempState[2] = l1
        l2 = list(tempState[0])
        l2.insert(0, top)
        tempState[0] = l2
        moves.append(tempState)
        
        tempState = currentState.copy()
        l1 = list(tempState[2])
        top = l1.pop(0)
        tempState[2] = l1
        l2 = list(tempState[1])
        l2.insert(0, top)
        tempState[1] = l2
        moves.append(tempState)
    return moves

def goalTest(currentState):
    if currentState[0]==goalState[0] or currentState[0]==goalState[1] or currentState[0]==goalState[2]:
        if currentState[1]==goalState[0] or currentState[1]==goalState[1] or currentState[1]==goalState[2]:
            if currentState[2]==goalState[0] or currentState[2]==goalState[1] or currentState[2]==goalState[2]:
                    return True
    return False      
    
def hillClimbing(currentState):
    if goalTest(currentState):
        print("GOAL REACHED!!!")
        exit()

    hValues = []
    path = []
    path.append(currentState)
    state = currentState
    while True:
        hValues.clear()
        for move in moveGen(state):
            hValues.append(heuristic2(move))
        if max(hValues)==heuristic2(goalState):
            if goalTest(moveGen(state)[hValues.index(max(hValues))]):
                path.append(moveGen(state)[hValues.index(max(hValues))])
                print("GOAL REACHED!!!")
                print("Path taken: ",path)
                print("States explored: ",len(path))
                break       
        if max(hValues)<=heuristic2(currentState):
            print("LOCAL MAXIMA REACHED")
            print("Path taken: ",path)
            print("Number of states explored",len(path))
            break
        state = moveGen(state)[hValues.index(max(hValues))]
        path.append(state)
        
initialTime = time.time()
# inputTerminal()
hillClimbing(startState)
finalTime = time.time()
print("Time taken:",finalTime-initialTime)