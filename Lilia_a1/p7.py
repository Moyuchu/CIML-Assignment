import sys, parse, grader
# 8皇后局部搜索-得到一个更好的board
def better_board(problem):
    #Your p7 code here
    n = len(problem)
    attackCheck = [[0] * n for _ in range(n)]
    chessmen = problem[:]

    for col in range(n):
        # print('col', col)
        # 防止变化
        original_value = chessmen[col]
        # for a in chess[n]:
        for row in range(n):
            # print('row', row , 'col', col)
            chessmen[col] = row
            # attacks = [0] * n
            # 到此，col和row确定了一个新位置
            # check棋子，chessNow是当前棋子与不同位置棋子检查attack；col是变化后的新棋子位置；i是不同的棋子
            for nextChess in range(n):
                for chessAttack in range(nextChess, n):
                    # print('chessAttack', chessAttack)
                    if nextChess != chessAttack:
                        # 同一行
                        if chessmen[chessAttack] == chessmen[nextChess]:
                            attackCheck[row][col] += 1
                        # 对角线
                        if abs(chessmen[chessAttack] - chessmen[nextChess]) == abs(chessAttack - nextChess):
                            attackCheck[row][col] += 1

        chessmen[col] = original_value

    # 寻找最小攻击数
    minAttack = 65
    bestPos = (0, 0)
    for col in range(n):
        for row in range(n):
            if attackCheck[row][col] < minAttack:
                minAttack = attackCheck[row][col]
                bestPos = (row, col)
    chessmen[bestPos[1]] = bestPos[0]
    # print('chessmen', chessmen)

    # chessmen[col] = row
    # return chessmen

    boardBest = [['.'] * n for _ in range(n)]
    for col in range(n):
        boardBest[chessmen[col]][col] = 'q'
    # print('boardBest', boardBest)
    solution = '\n'.join([' '.join(row) for row in boardBest])

# solution = """
# . q . . . . . .
# . . . . . . . .
# . . . . . . . .
# . . . q . . . .
# q . . . q . . .
# . . . . . q . q
# . . q . . . q .
# . . . . . . . ."""
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 7
    grader.grade(problem_id, test_case_id, better_board, parse.read_8queens_search_problem)