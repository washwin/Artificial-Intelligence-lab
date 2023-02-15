

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

for i in range(3):
    j=0
    while j<len(startState[i])-1:
        stateDict[startState[i][j]]=startState[i][j+1]
        j=j+1

for i in range(3):
    j=0
    while j<len(goalState[i])-1:
        goalDict[goalState[i][j]]=goalState[i][j+1]
        j=j+1

def heuristic11(currentState):
    value = 0
    for x in currentState:
        for y in x:
            if y=="GROUND":
                continue
            if str(stateDict[y])==str(goalDict[y]):
                value = value+1
            else:
                value = value-1
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
    if currentState==goalState:
        return True
    return False


    
# def hillClimbing(currentState):
#     if goalTest(currentState):
#         print("GOAL REACHED!!!")
#         exit()

#     hValues = []
#     path = []
#     Hvalues = {}
#     path.append(currentState)
#     currentHvalue = heuristic1(currentState)
#     Hvalues[currentState] = currentHvalue
    # while True:
    #     hValues.clear()
    #     for move in moveGen(currentState):
    #         hValues.append(heuristic1(move))
        
    #     if max(hValues)<currentHvalue:
    #         if goalTest(currentState):
    #             print("GOAL REACHED!!!")
    #             exit()
    #         else:
    #             print("GOAL NOT REACHABLE!!!")
    #             exit()
                
    #     for x in hValues:
    #         if currentHvalue<x:
    #             currentHvalue=x
    # flag = 0
    # parentdict = {}
    # while flag == 0:
    #     temp = path[-1]
    #     if goalTest(currentState):
    #         way = []
    #         #back(way , temp)
    #     minimum = temp
    #     for move in moveGen(temp):
    #         hvalue = heuristic1(move)
    #         parentdict[move] = temp
    #         Hvalues[move] = hvalue
    #         if 


startState = [['A', 'B', 'C', 'GROUND'], ['E', 'GROUND'], ['GROUND']]
goalState = [['C', 'GROUND'], ['B', 'E', 'GROUND'], ['A', 'GROUND']]
        
def heuristic2(currentState):
    value = 0
    for i in range(3):
        for j in range(len(currentState[i])-1):
            if currentState[i][j:]==goalState[0][j:] or currentState[i][j:]==goalState[1][j:] or currentState[i][j:]==goalState[2][j:]:
                value = value + len(currentState[i]) - j - 2
            else:
                value = value - len(currentState[i]) + j + 2
    return value

# print(heuristic2(startState))

def heuristic1(currentState):
    value = 0
    for i in range(3):
        for j in range(len(currentState[i])-2):
            if currentState[i][j:j+2]==goalState[0][j:j+2] or currentState[i][j:j+2]==goalState[1][j:j+2] or currentState[i][j:j+2]==goalState[2][j:j+2]:
                value = value + 1
            else:
                value = value - 1
    return value

print(heuristic1(goalState))