# 人工智慧期末專案 五子棋 加alpha + beta剪枝 對局搜尋
## 此專案參考老師的五子棋 以及別人github結合alpha + beta剪枝和對局搜尋
## 內容
- [對局搜尋](#Min-Max對局搜尋法)
- [剪枝搜尋](#alpha-beta剪枝搜尋)
- [程式碼](#CODE)
- [參考資料](#參考資料)
- [授權聲明](#授權聲明)
## Min-Max對局搜尋法

![pic](https://github.com/www-abcdefg/ai109b/blob/main/pic/%E7%AC%AC%E5%85%AB%E9%80%B1pic/%E7%AC%AC%E5%85%AB%E9%80%B1pic.png)

## alpha-beta剪枝搜尋
* 「Min-Max 對局搜尋法」的一個修改版，主要是在 Min-Max 當中加入了 α 與 β 兩個紀錄值，來做為是否要修剪的參考標準

![pic](https://github.com/www-abcdefg/ai109b/blob/main/%E6%9C%9F%E6%9C%AB/pic.jpg)

## code
* 對局搜尋五子棋.py
    * 參考老師的code 以及別人github code 加以修改寫出的
    * [老師的code](https://gitlab.com/ccc109/ai/-/blob/master/11-chess/01-gomoku/gomoku.py)
    * [自己修改後的code](https://github.com/www-abcdefg/ai109b/blob/main/%E6%9C%9F%E6%9C%AB/%E5%B0%8D%E5%B1%80%E6%90%9C%E5%B0%8B%E4%BA%94%E5%AD%90%E6%A3%8B.py)
```
import sys
import time


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

#Weight(棋型評估分數)
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

listAI = []  # AI
listHuman = []  # human
listAllStep = []  # all

listBoard=[]

#AI 下一步棋
next_point = [0, 0] 

ratio = 1 # 進攻係數 大於1進攻反之則防守
DEPTH = 3 # 探索深度
for i in range(16):
    for j in range(16):
        listBoard.append((i, j))


def ai():
    global cut_count   # 統計剪枝次數
    cut_count = 0
    global search_count   # 統計搜索次數
    search_count = 0
    #如果電腦下第一步，則從 First Step 開始
    firstPoint = (8, 8)
    
    if not listAllStep: 
        listAllStep.append(firstPoint)
        listAI.append(firstPoint)

        return firstPoint[0],firstPoint[1]
    else:
        negamax(True, DEPTH, -99999999, 99999999)
        # print("本次共剪枝次數：" + str(cut_count))
        # print("本次共搜索次數：" + str(search_count))

        return next_point[0], next_point[1]


# 負值極大算法搜索 alpha + beta剪枝
def negamax(is_ai, depth, alpha, beta):
    if depth == 0:
        return evaluation(is_ai)
    #用 set 剔除走過的位置
    blank_list = list(set(listBoard).difference(set(listAllStep)))

    order(blank_list)   # 搜索顺序排序  提高剪枝效率
    # 遍歷每一個後選步
    for next_step in blank_list:

        global search_count
        search_count += 1

        # 如果要評估的位置沒有相鄰的子， 則不去評估  減少計算
        if not has_neightnor(next_step):
            continue

        if is_ai:
            listAI.append(next_step)
        else:
            listHuman.append(next_step)
        listAllStep.append(next_step)

        value = -negamax(not is_ai, depth - 1, -beta, -alpha)
        if is_ai:
            listAI.remove(next_step)
        else:
            listHuman.remove(next_step)
        listAllStep.remove(next_step)

        if value > alpha:

            #print(str(value) + "alpha:" + str(alpha) + "beta:" + str(beta))
            #print(listAllStep)
            if depth == DEPTH:
                next_point[0] = next_step[0]
                next_point[1] = next_step[1]
            # alpha + beta剪枝點
            if value >= beta:
                global cut_count
                cut_count += 1
                return beta
            alpha = value
    return alpha


def order(blank_list):
    #紀錄當前下的那步棋
    last_pt = listAllStep[-1]
    # print(last_pt)
    for item in blank_list:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                
                #找到lastPt附近的位置，並insert到最前面
                if (last_pt[0] + i, last_pt[1] + j) in blank_list:
                    blank_list.remove((last_pt[0] + i, last_pt[1] + j))
                    blank_list.insert(0, (last_pt[0] + i, last_pt[1] + j))

#判斷鄰近位置有沒有棋
def has_neightnor(pt):
    for i in range(-1, 2):
        for j in range(-1, 2):
            #忽略自己的位置
            if i == 0 and j == 0:
                continue
            #附近9宮格有下過子
            if (pt[0] + i, pt[1]+j) in listAllStep:
                return True
    return False

def evaluation(is_ai):
    total_score = 0

    if is_ai:
        my_list = listAI
        enemy_list = listHuman
    else:
        my_list = listHuman
        enemy_list = listAI

    # 算自己的得分
    score_all_arr = []  # 得分形狀的位置 用於計算如果有相交 得分翻倍
    my_score = 0
    for pt in my_list:
        m = pt[0]
        n = pt[1]
        my_score += cal_score(m, n, 0, 1, enemy_list, my_list, score_all_arr)
        my_score += cal_score(m, n, 1, 0, enemy_list, my_list, score_all_arr)
        my_score += cal_score(m, n, 1, 1, enemy_list, my_list, score_all_arr)
        my_score += cal_score(m, n, -1, 1, enemy_list, my_list, score_all_arr)

    #  算敵人的得分， 並扣掉
    score_all_arr_enemy = []
    enemy_score = 0
    for pt in enemy_list:
        m = pt[0]
        n = pt[1]
        enemy_score += cal_score(m, n, 0, 1, my_list, enemy_list, score_all_arr_enemy)
        enemy_score += cal_score(m, n, 1, 0, my_list, enemy_list, score_all_arr_enemy)
        enemy_score += cal_score(m, n, 1, 1, my_list, enemy_list, score_all_arr_enemy)
        enemy_score += cal_score(m, n, -1, 1, my_list, enemy_list, score_all_arr_enemy)

    total_score = my_score - enemy_score*ratio*0.1

    return total_score   

def cal_score(m, n, x_decrict, y_derice, enemy_list, my_list, score_all_arr):
    add_score = 0  # 加分項目
    # 在一个方向上， 只取最大的得分項目
    max_score_shape = (0, None)

    # 如果此方向上，該點已經有得分形狀，則不重復計算
    for item in score_all_arr:
        for pt in item[1]:
            if m == pt[0] and n == pt[1] and x_decrict == item[2][0] and y_derice == item[2][1]:
                return 0

    # 在落子點 左右方向上循環查找得分形狀
    for offset in range(-5, 1):
        # offset = -2
        pos = []
        for i in range(0, 6):
            if (m + (i + offset) * x_decrict, n + (i + offset) * y_derice) in enemy_list:
                pos.append(2)
            elif (m + (i + offset) * x_decrict, n + (i + offset) * y_derice) in my_list:
                pos.append(1)
            else:
                pos.append(0)
        tmp_shap5 = (pos[0], pos[1], pos[2], pos[3], pos[4])
        tmp_shap6 = (pos[0], pos[1], pos[2], pos[3], pos[4], pos[5])

        for (score, shape) in shape_score:
            if tmp_shap5 == shape or tmp_shap6 == shape:
                if score > max_score_shape[0]:
                    max_score_shape = (score, ((m + (0+offset) * x_decrict, n + (0+offset) * y_derice),
                                               (m + (1+offset) * x_decrict, n + (1+offset) * y_derice),
                                               (m + (2+offset) * x_decrict, n + (2+offset) * y_derice),
                                               (m + (3+offset) * x_decrict, n + (3+offset) * y_derice),
                                               (m + (4+offset) * x_decrict, n + (4+offset) * y_derice)), (x_decrict, y_derice))

    # 計算兩個形狀相交， 如兩個3活 相交， 得分增加 一個子的除外
    if max_score_shape[1] is not None:
        for item in score_all_arr:
            for pt1 in item[1]:
                for pt2 in max_score_shape[1]:
                    if pt1 == pt2 and max_score_shape[0] > 10 and item[0] > 10:
                        add_score += item[0] + max_score_shape[0]

        score_all_arr.append(max_score_shape)

    return add_score + max_score_shape[0]

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
        listHuman.append((r, c))
        listAllStep.append((r, c))
    except Exception as e:
        print("!!!!!!!!!!!!!! Attention !!!!!!!!!!!!!!\n")
        print(f"Got Error {e}")
        print("\n!!!!!!!!!!!!!! Attention !!!!!!!!!!!!!!")
        humanTurn(board, turn)

def computerTurn(board, turn):
    print("Computer Turn")
    #計算最佳位置
    aiStep = ai()
    board.m[aiStep[0]][aiStep[1]] = turn

    #紀錄路徑
    listAllStep.append(aiStep)
    listAI.append(aiStep)

z9 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
i9 = [-4, -3, -2, -1, 0, 1, 2, 3, 4]
d9 = [4, 3, 2, 1, 0, -1, -2, -3, -4]
z5 = [0, 0, 0, 0, 0]
i2 = i9[2:-2]
d2 = d9[2:-2]


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

def chess(o, x):
    b = Board(16, 16) #  建立棋盤
    b.show()            #  顯示棋盤
    while 1:
        print(o)
        if o=='p':
            humanTurn(b, 'o')
        else:
            computerTurn(b, 'o')
        b.show()
        winCheck(b, 'o')
        #winCheck
        if x=='p':
            humanTurn(b, 'x')
        else:
            computerTurn(b, 'x')
        b.show()
        winCheck(b, 'x')

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

user1 = input("User1 : c/p ").lower()
user2 = input("User2 : c/p ").lower()
o, x = user1, user2
user1 = "Computer" if user1=="c" else "Human"
user2 = "Computer" if user2=="c" else "Human"
print(f"User1 : {user1}, User2 : {user2}")

chess(o, x)

```
* 執行結果
```
PS C:\Users\柯泓吉\Desktop\課程\人工智慧\ai109b\期末> python 對局搜尋五子棋.py pc
User1 : c/p p
User2 : c/p c
User1 : Human, User2 : Computer
  0 1 2 3 4 5 6 7 8 9 a b c d e f
0 - - - - - - - - - - - - - - - - 0
1 - - - - - - - - - - - - - - - - 1
2 - - - - - - - - - - - - - - - - 2
3 - - - - - - - - - - - - - - - - 3
4 - - - - - - - - - - - - - - - - 4
5 - - - - - - - - - - - - - - - - 5
6 - - - - - - - - - - - - - - - - 6
7 - - - - - - - - - - - - - - - - 7
8 - - - - - - - - - - - - - - - - 8
9 - - - - - - - - - - - - - - - - 9
a - - - - - - - - - - - - - - - - a
b - - - - - - - - - - - - - - - - b
c - - - - - - - - - - - - - - - - c
d - - - - - - - - - - - - - - - - d
e - - - - - - - - - - - - - - - - e
f - - - - - - - - - - - - - - - - f
  0 1 2 3 4 5 6 7 8 9 a b c d e f
p
Input e.g.: 11、22、13......
將o下在?88
  0 1 2 3 4 5 6 7 8 9 a b c d e f  
0 - - - - - - - - - - - - - - - - 0
1 - - - - - - - - - - - - - - - - 1
2 - - - - - - - - - - - - - - - - 2
3 - - - - - - - - - - - - - - - - 3
4 - - - - - - - - - - - - - - - - 4
5 - - - - - - - - - - - - - - - - 5
6 - - - - - - - - - - - - - - - - 6
7 - - - - - - - - - - - - - - - - 7
8 - - - - - - - - o - - - - - - - 8
9 - - - - - - - - - - - - - - - - 9
a - - - - - - - - - - - - - - - - a
b - - - - - - - - - - - - - - - - b
c - - - - - - - - - - - - - - - - c
d - - - - - - - - - - - - - - - - d
e - - - - - - - - - - - - - - - - e
f - - - - - - - - - - - - - - - - f
  0 1 2 3 4 5 6 7 8 9 a b c d e f  
Computer Turn
  0 1 2 3 4 5 6 7 8 9 a b c d e f  
0 - - - - - - - - - - - - - - - - 0
1 - - - - - - - - - - - - - - - - 1
2 - - - - - - - - - - - - - - - - 2
3 - - - - - - - - - - - - - - - - 3
4 - - - - - - - - - - - - - - - - 4
5 - - - - - - - - - - - - - - - - 5
6 - - - - - - - - - - - - - - - - 6
7 - - - - - - - - - - - - - - - - 7
8 - - - - - - - - o - - - - - - - 8
9 - - - - - - - - - x - - - - - - 9
a - - - - - - - - - - - - - - - - a
b - - - - - - - - - - - - - - - - b
c - - - - - - - - - - - - - - - - c
d - - - - - - - - - - - - - - - - d
e - - - - - - - - - - - - - - - - e
f - - - - - - - - - - - - - - - - f
  0 1 2 3 4 5 6 7 8 9 a b c d e f
p
Input e.g.: 11、22、13......
將o下在?
```
## 參考資料
* [博弈树alpha-beta剪枝搜索的五子棋AI](https://www.jianshu.com/p/8376efe0782d)
* [五子棋code參考](https://github.com/colingogogo/gobang_AI#gobang_ai)
* [min max](https://gitlab.com/ccc109/ai/-/blob/master/11-chess/02-Min-Max%E5%B0%8D%E5%B1%80%E6%90%9C%E5%B0%8B%E6%B3%95.md)
* [陳鍾誠老師code ai/11-chess/01-gomoku/gomoku.py](https://gitlab.com/ccc109/ai/-/blob/master/11-chess/01-gomoku/gomoku.py)

# 授權聲明
* [授權聲明](https://github.com/www-abcdefg/ai109b/blob/main/%E6%9C%9F%E6%9C%AB/LICENSE.md)