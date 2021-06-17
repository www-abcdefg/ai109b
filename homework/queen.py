def queen(n): # 主函數
	q = [] # q 代表已經排下去的皇后，一開始為空的
	return queenNext(n, q) # 呼叫 queenNext 遞迴下去排出所有可能

def queenNext(n, q): # 已經排好 q[0..y2-1], 繼續排下去 [y2...n-1]
	y2 = qlen = len(q)
	if qlen == n: # 全部排好了
		print(q)  # 印出盤面
		return# 未排滿則繼續排下去
	for x2 in range(n): # 對本列的每一個 x2 去嘗試
		isConflict = False
		for y in range(qlen): # 前面已經排下去的舊皇后，座標為 (x,y)
			x = q[y]
			if conflict(x,y,x2,y2): # 檢查排的皇后(x2,y2)，前後有無衝突
				isConflict = True
		if not isConflict:  # 若無衝突，則繼續排下去
			q.append(x2)    # 把 (x2,y2) 放進盤面
			queenNext(n, q) # 繼續遞迴尋找下一個皇后位置
			q.pop()         # 把 (x2,y2) 移出盤面
		
def conflict(x1,y1,x2,y2): # 判斷 (x1,y1), (x2,y2) 位置有沒有衝突
	if x1==x2: return True
	if y1==y2: return True
	if x1+y1==x2+y2: return True
	if x1-y1==x2-y2: return True
	return False

queen(4) # 列出四皇后的解答
queen(8) # 列出八皇后的解答
