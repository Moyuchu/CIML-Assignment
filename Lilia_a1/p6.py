import sys, parse, grader
# 8皇后局部搜索-攻击次数
def number_of_attacks(problem):
    #Your p6 code here

    solution = ""
    n = len(problem)
    attackCheck = [[0] * n for _ in range(n)]
    chessmen = problem[:]
    # print('chessmen', chessmen)

    for col in range(n):
        # print('col', col)
        # 防止变化
        original_value = chessmen[col]
        # for a in chess[n]:
        for row in range(n):
            # print('row', row , 'col', col)
            chessmen[col] = row
            # attacks = 0
            attacks = [0] * n
            # 到此，col和row确定了一个新位置
            # check棋子，chessNow是当前棋子与不同位置棋子检查attack；col是变化后的新棋子位置；i是不同的棋子
            for nextChess in range(n):
                # if k != i and k != col:
                # print('nextChess', nextChess)
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
    # for row in attackCheck:
    #     print(' '.join(map(str, row)))

    solution = '\n'.join([' '.join(f'{item:>2}' for item in row) for row in attackCheck])
    # solution = attackCheck
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 6
    grader.grade(problem_id, test_case_id, number_of_attacks, parse.read_8queens_search_problem)