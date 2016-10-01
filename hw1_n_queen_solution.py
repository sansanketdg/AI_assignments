import queue as Q
import sys
import csv
import datetime
# moves = UP, RIGHT, DOWN, LEFT
moves = [[-1, 0], [0, 1], [1, 0], [0, -1]]
goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
_3_or_4 = 0
_algo_to_use = 0

steps_IDA = ""

class Node:
    def __init__(self, state, parent, action, gn):
        self.parent = parent
        self.state = state
        self.action = action
        self.gn = gn
        #self.heuristic = heuristic

#def heuristic(state):
#    counter = 1
#    heu = 0
#    for i in range(3):
#        for j in range(3):
#            if(state[i][j] != counter):
#                heu+=1
#            counter+=1
#    return heu

def actualPos(counter1):
    counter = counter1 - 1
    x = counter / 3
    y = (counter % 3)
    return [int(x), int(y)]

#def heu_manhanttan(state):
def heuristic(state):
    #printBoard(state)
    heu = 0
    #counter = 1
    for i in range(3):
        for j in range(3):
            if(state[i][j] != 0):
                x, y = actualPos(state[i][j])
                #print(x, y)
            else:
                x = 2
                y = 2
            #print(abs(x - i) + abs(y - j))
            heu = heu + (abs(x - i) + abs(y - j))
            #counter+=1
    #print(heu)
    return heu

# def heuristic(board):
#     distance = 0
#     l = len(board)
#     for i in range(l):
#         for j in range(l):
#             if board[i][j] != 0 and board[i][j] != (_3_or_4 * i + j + 1):
#                 # Mapping to actual positions to find Manhattan distance - xA,yA are the actual positions
#                 rem = board[i][j] % l
#                 quotient = int(board[i][j] / l)
#                 if rem == 0:
#                     xA = quotient - 1
#                     yA = l - 1
#
#                 else:
#                     xA = quotient
#                     yA = rem - 1
#                     # print(str(xA)+"  "+str(yA))
#                 distance += abs(xA - i) + abs(yA - j)
#                 # print(str(board[i][j])+"  "+str(xA)+"  "+str(yA)+"  "+str(i)+"  "+str(j))
#     return distance

def possibleMoves(board):

    global moves
    x, y = findGap(board)

    res = []
    for mv in moves:
        x2, y2 = nextPos(x, y, mv)
        if isPositionLegal(board, x2, y2):
            res.append(mv)

    return res

def moveGap(board1, move):

    board = createBoardCopy(board1)
    x, y = findGap(board)
    x2, y2 = nextPos(x, y, move)
    tmp = board[x][y]
    board[x][y] = board[x2][y2]
    board[x2][y2] = tmp
    return board

def findGap(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                return i,j
    return -1, -1

def printBoard(board):

    print("")
    for row in board:
        row_str = ""
        for cell in row:
            row_str += str(cell) + " "
        print(row_str)

def isPositionLegal(board, x, y):
    n = len(board)
    return ((x >= 0) and (x < n) and (y >= 0) and (y < n))

def nextPos(x,y, move):
    nextX = x + move[0]
    nextY = y + move[1]

    return nextX, nextY

def canMove(board, direction):

    mv = moves[direction]
    x, y = findGap(board)
    x2, y2 = nextPos(x, y, mv)

    return isPositionLegal(board, x2, y2)

def createBoardCopy(current):
    currentcpy = [[0,0,0],[0,0,0],[0,0,0]]
    for i in range(3):
        for j in range(3):
            currentcpy[i][j] = current[i][j]
    return currentcpy

def writeToFile(steps):
    f = open('output.txt', 'w')
    f.write(steps)
    f.close()

def IDA_star_solvePuzzle(state):
    beg = datetime.datetime.now()

    #global steps_IDA
    gn_till_now = 0
    actualBoard = createBoardCopy(state)
    #node1 = Node(state, None, None, gn_till_now)
    bound = heuristic(state)
    while(True):
        state = createBoardCopy(actualBoard)
        t = search(state, 0, bound, "")
        if(t == True):
            end = datetime.datetime.now()
            print("Time taken : ",end="")
            print(end-beg)
            #steps_IDA = steps_IDA[2:]
            #print(steps_IDA[:-1])
            #writeToFile(steps_IDA[:-1])
            return bound
        # if(t == 10000):         #infinity is represented by 10000 here
        #     return False;
        # bound = t
        else:
            bound = t

def search(state, g, bound, path):
    #printBoard(node.state)
    #global steps_IDA
    f = g + heuristic(state)
    if(f > bound):
        return f
    if(goal == state):
            # while(node.parent != None):
            #     path = getCharForAction(node.action) + path
            #     node = node.parent
            print(path)
            #printBoard(node.state)
            #print(getCharForAction(node.action))
            return True
    minim = 10000   #infinity is represented by 10000 here
    available_moves = possibleMoves(state)
    currentcpy = createBoardCopy(state)
    for action in available_moves:
        new__ = moveGap(state, action)
        #new_node = Node(new__, node, action, node.gn + 1)
        t = search(new__, g + 1, bound, path+ getCharForAction(action))
        if(t == True):
            #steps_IDA = getCharForAction(node.action) + steps_IDA
            #printBoard(node.state)
            #print(getCharForAction(node.action))
            return True
        if(t < minim):
            minim = t
        state = createBoardCopy(currentcpy)
    return minim

def getCharForAction(action):
    if (action == [-1, 0]):
        return "U,"
    elif (action == [1, 0]):
        return "D,"
    elif (action == [0, 1]):
        return "R,"
    else:
        return "L,"

def A_star_solvePuzzle(state):
    global moves
    global goal
    i = 0
    #state = [[1, 3, 0],[4, 2, 5], [7, 8, 6]]
    frontier = Q.PriorityQueue()
    gn_till_now = 0
    node1 = Node(state, None, None, gn_till_now)
    frontier.put((heuristic(state) + node1.gn, i, node1))
    i+=1
    visited_state = []
    steps = ""
    while(frontier.not_empty):
        current1 = frontier.get()
        current = current1[2];
        #printBoard(current.state)
        if(current.state == goal):
            while(current.parent != None):
                if(current.action == [-1, 0]):
                    steps = "U," + steps
                elif(current.action == [1, 0]):
                    steps = "D," + steps
                elif(current.action == [0, 1]):
                    steps = "R," + steps
                else:
                    steps = "L," + steps
                current = current.parent
            #print(current.state)
            print(steps[:-1])
            writeToFile(steps[:-1])
            return
        if(current.state not in visited_state):
            visited_state.append(current.state)
            available_moves = possibleMoves(current.state)
            currentcpy =createBoardCopy(current.state)
            for action in available_moves:
                new__ = moveGap(current.state, action)
                new_node = Node(new__, current, action, current.gn + 1)
                frontier.put((heuristic(new_node.state) + new_node.gn, i, new_node))
                i+=1
                current.state = createBoardCopy(currentcpy)
    #print(current)
if(sys.argv[1] == "1"):
    _algo_to_use = 1
elif(sys.argv[1] == "2"):
    _algo_to_use = 2
else:
    sys.exit("Invalid input for 8puzzle/15puzzle.\nProvide proper <#Algorithm> [1/2 : A*/IDA*] in following format\n'python puzzleSolver.py <#Algorithm> <N> <INPUT_FILE_PATH> <OUTPUT_FILE_PATH>'")

if(sys.argv[2] == "3"):
    #read file for 8 puzzle
    _3_or_4 = 3
    in_txt = csv.reader(open("8puzzle1.txt"))
elif(sys.argv[2] == "4"):
    _3_or_4 = 4
    #read file for 15 puzzle
    in_txt = csv.reader(open("15puzzle.txt", "r"))
else:
    sys.exit("Invalid input for 8puzzle/15puzzle.\nProvide proper <N> (3/4) in following format\n'python puzzleSolver.py <#Algorithm> <N> <INPUT_FILE_PATH> <OUTPUT_FILE_PATH>' ")

state = []
row = []
for line in in_txt:
    #print(line)
    for l in line:
        if(l == ''):
            row.append(0)
        else:
            row.append(int(l))
    state.append(row)
    row=[]
print("Initial input state is -")
print(state)

if(_algo_to_use == 1):
    A_star_solvePuzzle(state)
else:
    IDA_star_solvePuzzle(state)

