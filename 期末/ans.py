from math import degrees
import sys
import time
from typing import Container

#  棋盤物件
class Board:
    def __init__(self, rMax, cMax):
        self.m = [None] * rMax
        self.rMax = rMax
        self.cMax = cMax
        for r in range(rMax):
            self.m[r] = [None] * cMax
            for c in range(cMax):
                self.m[r][c] = '-'

    #  將棋盤格式化成字串
    def __str__(self):
        b = []
        b.append('  0 1 2 3 4 5 6 7 8 9 a b c d e f')
        for r in range(self.rMax):
            b.append('{:x} {:s} {:x}'.format(r, ' '.join(self.m[r]), r))
            # r.toString(16) + ' ' + self.m[r].join(' ') + ' ' + r.toString(16) + '\n'

        b.append('  0 1 2 3 4 5 6 7 8 9 a b c d e f')
        return '\n'.join(b)

    #  顯示棋盤
    def show(self):
        print(str(self))

#Weight
shape_score = [(50, (0, 1, 1, 0, 0)),
               (50, (0, 0, 1, 1, 0)),
               (200, (1, 1, 0, 1, 0)),
               (500, (0, 0, 1, 1, 1)),
               (500, (1, 1, 1, 0, 0)),
               (5000, (0, 1, 1, 1, 0)),
               (5000, (0, 1, 0, 1, 1, 0)),
               (5000, (0, 1, 1, 0, 1, 0)),
               (5000, (1, 1, 1, 0, 1)),
               (5000, (1, 1, 0, 1, 1)),
               (5000, (1, 0, 1, 1, 1)),
               (5000, (1, 1, 1, 1, 0)),
               (5000, (0, 1, 1, 1, 1)),
               (50000, (0, 1, 1, 1, 1, 0)),
               (99999999, (1, 1, 1, 1, 1))]


listAI = [] #AI走過的路徑
listHuman = [] #玩家走過的路徑
listAllStep = [] #Save all path

#棋盤上所有可以走的點
listBoard = [] 

#AI 下一步棋
nextPoint = [0, 0] 

ratio = 2
DEEPTH = 3
for i in range(16):
    for j in range(16):
        listBoard.append((i, j))


def ai():
    global cutCount   #剪枝次數
    global searchCount #搜索次數
    cutCount, searchCount = 0, 0 
    print("Starting")
    minAB(True, DEEPTH, -99999999, 99999999)
    print("本次共剪枝次数：" + str(cutCount))
    print("本次共搜索次数：" + str(searchCount))
    return nextPoint[0], nextPoint[1]

#min max & alpha beta
def minAB(isAI, depth, alpha, beta):
    global valueStore
    if depth == 0:
        return evalution(isAI)
        
    #利用 set 剔除走過的位置
    blankList = list(set(listBoard).difference(set(listAllStep)))

    order(blankList)

    #去判斷所有可能性
    for nextStep in blankList:

        global searchCount
        searchCount+=1

        #nextStep附近沒有棋(9宮格)，就不去評估
        if not hasNeightnor(nextStep):
            continue

        #紀錄 AI & Player 可能的路徑
        if isAI:
            listAI.append(nextStep)
        else:
            listHuman.append(nextStep)

        listAllStep.append(nextStep)

        value = -minAB(not isAI, depth - 1, -beta, -alpha)
        if isAI:
            listAI.remove(nextStep)
        else:
            listHuman.remove(nextStep)

        listAllStep.remove(nextStep)

        if value > alpha:
            print(f"alpha : {alpha} , beta {beta}")

            if depth == DEEPTH:
                nextPoint[0], nextPoint[1] = nextStep[0], nextStep[1]
            if value >= beta:
                global cutCount
                cutCount+=1
                return beta
            alpha = value
    return alpha

#排序，先從對手下的那步棋附近開始判斷，降低計算量
def order(blankList):
    #紀錄當前下的那步棋
    lastPt = listAllStep[-1]
    for item in blankList:
        for i in range(-1, 2):
                for j in range(-1, 2):
                    if i==0 and j==0:
                        continue
                    
                    #找到lastPt附近的位置，並insert到最前面
                    if (lastPt[0]+i, lastPt[1]+j) in blankList:
                        blankList.remove((lastPt[0]+i, lastPt[1]+j))
                        blankList.insert(0, (lastPt[0]+i, lastPt[1]+j))

#判斷鄰近位置有沒有棋
def hasNeightnor(pt):
    for i in range(-1, 2):
        for j in range(-1,2 ):

            #忽略自己的位置
            if i==0 and j==0:
                continue

            #附近有下過子
            if (pt[0]+i, pt[1]+j) in listAllStep:
                return True
    return False

def evalution(isAI):
    totalScore = 0
    if isAI:
        myList, enemyList = listAI, listHuman
    else:
        myList, enemyList = listHuman, listAI

    #自己得分
    scoreAllArr = []
    myScore = 0
    for pt in myList:
        m = pt[0]
        n = pt[1]
        myScore += calScore(m, n, 0, 1, enemyList, myList, scoreAllArr)
        myScore += calScore(m, n, 1, 0, enemyList, myList, scoreAllArr)
        myScore += calScore(m, n, 1, 1, enemyList, myList, scoreAllArr)
        myScore += calScore(m, n, -1, 1, enemyList, myList, scoreAllArr)

    #  算敌人的得分， 并减去
    scoreAllArrEnemy = []
    enemyScore = 0
    for pt in enemyList:
        m = pt[0]
        n = pt[1]
        enemyScore += calScore(m, n, 0, 1, myList, enemyList, scoreAllArrEnemy)
        enemyScore += calScore(m, n, 1, 0, myList, enemyList, scoreAllArrEnemy)
        enemyScore += calScore(m, n, 1, 1, myList, enemyList, scoreAllArrEnemy)
        enemyScore += calScore(m, n, -1, 1, myList, enemyList, scoreAllArrEnemy)

    totalSscore = myScore - enemyScore*ratio*0.1

    return totalScore

def calScore(m, n, xDirect, yDirect, enemyList, myList, scoreAllArr):
    addScore = 0
    maxScoreShape = (0, None)
    for item in scoreAllArr:
        for pt in item[1]:
            if m == pt[0] and n == pt[1] and xDirect == item[2][0] and yDirect == item[2][1]:
                return 0
    for offset in range(-5, 1):
        # offset = -2
        pos = []
        for i in range(0, 6):
            if (m + (i + offset) * xDirect, n + (i + offset) * yDirect) in enemyList:
                pos.append(2)
            elif (m + (i + offset) * xDirect, n + (i + offset) * yDirect) in myList:
                pos.append(1)
            else:
                pos.append(0)
        tmp_shap5 = (pos[0], pos[1], pos[2], pos[3], pos[4])
        tmp_shap6 = (pos[0], pos[1], pos[2], pos[3], pos[4], pos[5])

        for (score, shape) in shape_score:
            if tmp_shap5 == shape or tmp_shap6 == shape:
                if tmp_shap5 == (1,1,1,1,1):
                    print('wwwwwwwwwwwwwwwwwwwwwwwwwww')
                if score > maxScoreShape[0]:
                    maxScoreShape = (score, ((m + (0+offset) * xDirect, n + (0+offset) * yDirect),
                                               (m + (1+offset) * xDirect, n + (1+offset) * yDirect),
                                               (m + (2+offset) * xDirect, n + (2+offset) * yDirect),
                                               (m + (3+offset) * xDirect, n + (3+offset) * yDirect),
                                               (m + (4+offset) * xDirect, n + (4+offset) * yDirect)), (xDirect, yDirect))

    # 计算两个形状相交， 如两个3活 相交， 得分增加 一个子的除外
    if maxScoreShape[1] is not None:
        for item in scoreAllArr:
            for pt1 in item[1]:
                for pt2 in maxScoreShape[1]:
                    if pt1 == pt2 and maxScoreShape[0] > 10 and item[0] > 10:
                        addScore += item[0] + maxScoreShape[0]

        scoreAllArr.append(maxScoreShape)

    return addScore + maxScoreShape[0]

def humanTurn(board, turn):
    global listAllStep
    try:
        print("Input e.g.: 11、22、13......")
        xy = input(f"將{turn}下在?")
        r = int(xy[0], 16) # Turn into Hex
        c = int(xy[1], 16)
        # Out of border
        if r < 0 or r > board.rMax or c < 0 or c > board.cMax:
            raise Exception (f"{r}, {c} is out of border")
        # Not empty
        if board.m[r][c] != "-":
            raise Exception (f"{r}, {c} is occupied.")
        board.m[r][c] = turn
        listAllStep.append((r, c))
        listHuman.append((r, c))
        print(listAllStep)
    except Exception as e:
        print("!!!!!!!!!!!!!! Attention !!!!!!!!!!!!!!\n")
        print(f"Got Error {e}")
        print("\n!!!!!!!!!!!!!! Attention !!!!!!!!!!!!!!")
        humanTurn(board, turn)


def patternCheck(board, turn, r, c, dr, dc):
    for i in range(len(dr)):
        tr = round(r + dr[i])
        tc = round(c + dc[i])
        if tr < 0 or tr >= board.rMax or tc < 0 or tc >= board.cMax:
            return False
        v = board.m[tr][tc]
        if (v != turn):
            return False
    
    return True

def winCheck(board, turn):
    win = False
    tie = True
    for r in range(board.rMax):
        for c in range(board.cMax):
            tie = False if board.m[r][c] == '-' else tie
            win = True if patternCheck(board, turn, r, c, z5, i2) else win #  水平 -
            win = True if patternCheck(board, turn, r, c, i2, z5) else win #  垂直 |
            win = True if patternCheck(board, turn, r, c, i2, i2) else win #  下斜 \
            win = True if patternCheck(board, turn, r, c, i2, d2) else win #  上斜 /
    if (win):
        print('{} 贏了！'.format(turn))  #  如果贏了就印出贏了
        sys.exit() #  然後離開。

    if (tie):
        print('平手')
        sys.exit(0) #  然後離開。

    return win


def computerTurn(board, turn):
    print("Computer Turn")
    aiStep = ai()
    board.m[aiStep[0]][aiStep[1]] = turn
    listAllStep.append(aiStep)
    listAI.append(aiStep)
    print(f"All {listAllStep}")
    print(f"Step {aiStep}")


def chess(o, x):
    b = Board(16, 16) #  建立棋盤
    b.show()            #  顯示棋盤
    while 1:
        print(o)
        if o=='p':
            humanTurn(b, 'o')
        else:
            computerTurn(b, 'o')
        #winCheck
        if x=='p':
            humanTurn(b, 'x')
        else:
            computerTurn(b, 'x')
        b.show()# Current state

user1 = input("User1 : c/p ").lower()
user2 = input("User2 : c/p ").lower()
o, x = user1, user2
user1 = "Computer" if user1=="c" else "Human"
user2 = "Computer" if user2=="c" else "Human"
print(f"User1 : {user1}, User2 : {user2}")

chess(o, x)

