import sys, grader, parse, math
import random
# Random Pacman play against up to 4 random Ghost
def random_play_multiple_ghosts(problem):
    #Your p3 code here
    # solution = ''
    EAT_FOOD_SCORE = 10
    PACMAN_EATEN_SCORE = -500
    PACMAN_WIN_SCORE = 500
    PACMAN_MOVING_SCORE = -1
    seed = problem['seed']
    # if seed != -1:
    random.seed(seed, version=1)
    solution = ''
    # Import the graph and random seed of the problem
    layout = problem['layout']
    results = []
    # first row
    results.append(f'seed: {seed}')
    # position pf pacman & ghost
    pacmanPos = None
    ghostPos = {'W': None, 'X': None, 'Y': None, 'Z': None}
    original = {'W': ' ', 'X': ' ', 'Y': ' ', 'Z': ' '}
    pacNum = 0
    ghostNum = 0
    score = 0

    # single list's index and cell
    for i, row in enumerate(layout):
        # single list's inside
        for j, item in enumerate(row):
            if item == 'P':
                pacmanPos = (i, j)
            elif item in ghostPos:
                ghostPos[item] = (i, j)
                ghostNum += 1
            elif item == '.':
                pacNum += 1
    # print('ghostPos', ghostPos)
    # every state for pacman and ghost
    count = 0
    # the state before moving first step
    results.append(f'{count}')
    results.append('\n'.join([''.join(row) for row in layout]))
    while True:
        # !!MAIN CODE for pacman
        if count % (ghostNum+1) == 0:
            # pacman random direction
            moveP = possible_pacman_position(pacmanPos, layout)
            count += 1
            results.append(f"{count}: P moving {moveP}")
            # print('这里是count', count, 'pacman', '确定往哪走了！', '走', moveP, '原位置', pacmanPos)

            score += PACMAN_MOVING_SCORE
            # record the next direction of pacman
            x, y = pacmanPos
            pacmanPos = direction_To_position(moveP, pacmanPos)
            # print('这里是count', count, 'pacman', '新位置', pacmanPos)

            if pacmanPos in ghostPos.values():
                score += PACMAN_EATEN_SCORE
                for ghost, pos in ghostPos.items():
                    # print('ghost', ghost, 'pos', pos)
                    if pos == pacmanPos:
                        # Whether P goes to W or W goes to P, the final display is W
                        layout[pacmanPos[0]][pacmanPos[1]] = ghost
                        break
            else:
                # eat bean
                if layout[pacmanPos[0]][pacmanPos[1]] == '.':
                    # print('eat')
                    # score -1
                    pacNum -= 1
                    score += EAT_FOOD_SCORE
                    # ate all beans and win the game
                    if pacNum == 0:
                        score += PACMAN_WIN_SCORE
                # 'P' move
                layout[pacmanPos[0]][pacmanPos[1]] = 'P'
            # passed through point will be ' '
            layout[x][y] = ' '
            results.append('\n'.join([''.join(row) for row in layout]))
            results.append(f"score: {score}")

        else:
            # !!MAIN CODE for ghost
            for ghost in sorted(ghostPos.keys()):
                # if this problem not have this ghost, then continue
                if ghostPos[ghost] == None:
                    continue
                # print('ghostPos[ghost]', ghostPos[ghost])
                # check which positions could be moved to
                moveG = possible_ghost_position(ghostPos[ghost], layout)
                # print('这是count', count + 1, 'ghost', ghost, '确定往哪走了！', '走', moveG)
                # record the old position to recover the last position in next step
                oldI, oldJ = ghostPos[ghost]
                count += 1
                # stuck by '%WXYZ'
                if moveG == None:
                    # print('ghost', ghost, '想走', moveG, '但已经有ghost了！', '标记位置', ghostPos[ghost])
                    results.append(f"{count}: {ghost} moving ")
                    results.append('\n'.join([''.join(row) for row in layout]))
                    results.append(f"score: {score}")
                    continue
                # set newPos for readable
                # make sure the next position caused by this move
                newPos = direction_To_position(moveG, ghostPos[ghost])

                ghostPos[ghost] = newPos
                results.append(f"{count}: {ghost} moving {moveG}")
                # whether ghost will eat Pacman
                if pacmanPos == newPos:
                    score += PACMAN_EATEN_SCORE
                # with or without pac, the coordinates that w passes through are reverted
                layout[oldI][oldJ] = original[ghost]
                # print('original[ghost]', original[ghost])
                # record the new position's value to recover the last position in next step
                original[ghost] = layout[newPos[0]][newPos[1]]
                # print('original', original)
                # change ghost to next
                layout[newPos[0]][newPos[1]] = ghost
                # output layout and score
                results.append('\n'.join([''.join(row) for row in layout]))
                results.append(f"score: {score}")
                # pacman already was eaten by ghost
                if pacmanPos in ghostPos.values():
                    break
        if pacNum == 0:
            results.append(f"WIN: Pacman")
            break
        elif pacmanPos in ghostPos.values():
            results.append(f"WIN: Ghost")
            break
    # standard output
    solution += '\n'.join(results)
    # solution = ''
    return solution

def possible_pacman_position(pacmanPos, layout):
    possibleMoves = []
    moveOffset = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
    for move, (x, y) in moveOffset.items():
        newPos = (pacmanPos[0]+x, pacmanPos[1]+y)
        # print('pacmanPos newPos', newPos)
        if layout[newPos[0]][newPos[1]] not in '%':
            possibleMoves.append(move)
    # print('possibleMoves', possibleMoves)
    return random.choice(sorted(possibleMoves)) if possibleMoves else None

def possible_ghost_position(ghostPos, layout):
    possibleMoves = []
    moveOffset = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
    for move, (x, y) in moveOffset.items():
        newPos = (ghostPos[0] + x, ghostPos[1] + y)
        # print('pacmanPos newPos', newPos)
        if layout[newPos[0]][newPos[1]] not in '%WXYZ':
            possibleMoves.append(move)
    # print('possibleMoves',possibleMoves)
    return random.choice(sorted(possibleMoves)) if possibleMoves else None

def direction_To_position(move, position):
    x, y = position
    moveOffset = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
    dx, dy = moveOffset[move]
    position = (x + dx, y + dy)

    return position

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 3
    grader.grade(problem_id, test_case_id, random_play_multiple_ghosts, parse.read_layout_problem)