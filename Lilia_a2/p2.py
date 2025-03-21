import sys, parse
import time, os, copy
import random
from collections import deque


# Pacman play against a single random Ghost
def better_play_single_ghosts(problem):
    #Your p2 code here
    solution = ''
    winner = 'Ghost'

    EAT_FOOD_SCORE = 10
    PACMAN_EATEN_SCORE = -500
    PACMAN_WIN_SCORE = 500
    PACMAN_MOVING_SCORE = -1
    solution = ''
    # Import the graph and random seed of the problem
    seed = problem['seed']
    if seed != -1:
        random.seed(seed, version=1)
    layout = problem['layout']
    results = []
    # first row
    results.append(f'seed: {seed}')
    # position pf pacman & ghost
    pacmanPos = None
    ghostPos = None
    beansPos = []
    pacNum = 0
    score = 0

    # single list's index and cell
    for i, row in enumerate(layout):
        # single list's inside
        for j, item in enumerate(row):
            if item == 'P':
                pacmanPos = (i, j)
            elif item == 'W':
                ghostPos = (i, j)
            elif item == '.':
                beansPos.append((i, j))
                pacNum += 1
                # print(f'{pacNum}: {item}')
    # all possible moves for pacman and ghost in each point
    possibleMoves = {}
    for i, row in enumerate(layout):
        for j, item in enumerate(row):
            if item != '%':  # Assuming '%' represents walls
                everyPos = (i, j)
                possibleMove = all_possible_move(everyPos, layout)
                possibleMoves[everyPos] = possibleMove
    # every state for pacman and ghost
    count = 0
    # used by ghost(W) to record the original point and restore after next step
    original = ' '
    # the state before moving first step
    results.append(f'{count}')
    results.append('\n'.join([''.join(row) for row in layout]))
    # start to record time

    while True:
        # if overtime, break
        # if end - start > 300:
        #     print("overtime")
        #     winner = 'Nobody, overtime'
        #     break
        # first step moved by pacman
        # !!MAIN CODE for pacman
        if count % 2 == 0:
            # pacman direction calculate
            bestMove = None
            bestScore = float('-inf')
            beansTonew = float('inf')
            # infinitely
            moveOffset = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
            moveBeansTonew = {}
            countP = 0
            for move in possibleMoves[pacmanPos]:
                # record the next direction of pacman
                x, y = pacmanPos
                # print('pacmanPos', pacmanPos)
                dx, dy = moveOffset[move]
                newPos = (x + dx, y+dy)
                # calculate straight-line distance of ghost and pacman or bean and pacman
                closeBean = None
                # beansTonew = abs(newPos[0] - beansPos[0]) + abs(newPos[1] - beansPos[1])
                beansTonew = float('inf')
                for bean in beansPos:
                    distance = abs(newPos[0] - bean[0]) + abs(newPos[1] - bean[1])
                    # distance = bfs(bean, newPos, layout)
                    if distance < beansTonew:
                        beansTonew = distance
                        # beansTonew = bfs(bean, newPos, layout)
                        closeBean = bean
                        # print('beansTonew', beansTonew)
                # beansTonew = bfs(closeBean, newPos, layout)
                ghostTonew = abs(newPos[0] - ghostPos[0]) + abs(newPos[1] - ghostPos[1])
                # ghostTonew = bfs(ghostPos, newPos, layout)
                scoreBFS = ghostTonew - beansTonew

                if ghostTonew < 2:
                    # continue
                    countP += 1
                    if countP != len(possibleMoves[pacmanPos]):
                        continue
                    else:
                        bestMove = move
                        break
                elif beansTonew == 0 and ghostTonew != 0:
                    bestMove = move
                    break
                else:
                    bestMoveS = move
                    moveBeansTonew[bestMoveS] = beansTonew
                    # choose the most far beansTonew's move
                    bestMove = min(moveBeansTonew, key=moveBeansTonew.get)
                if scoreBFS > bestScore:
                    bestScore = scoreBFS
                    bestMove = move
            moveP = bestMove
            # pacmanPos = move
            results.append(f"{count + 1}: P moving {moveP}")
            score += PACMAN_MOVING_SCORE
            x, y = pacmanPos
            pacmanPos = direction_To_position(moveP, pacmanPos)

            if pacmanPos == ghostPos:
                score += PACMAN_EATEN_SCORE
                # Whether P goes to W or W goes to P, the final display is W
                layout[pacmanPos[0]][pacmanPos[1]] = 'W'
            else:
                # eat bean
                if layout[pacmanPos[0]][pacmanPos[1]] == '.':
                    # score -1
                    pacNum -= 1
                    score += EAT_FOOD_SCORE
                    beansPos.remove(pacmanPos)
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
            moveG = random.choice(possibleMoves[ghostPos])
            results.append(f"{count + 1}: W moving {moveG}")
            # record the next direction of ghost
            i, j = ghostPos
            ghostPos = direction_To_position(moveG, ghostPos)
            # whether W will eat Pacman
            if pacmanPos == ghostPos:
                score += PACMAN_EATEN_SCORE
            # with or without pac, the coordinates that w passes through are reverted
            layout[i][j] = original
            # recorded next one
            original = layout[ghostPos[0]][ghostPos[1]]
            # ghost move
            layout[ghostPos[0]][ghostPos[1]] = 'W'
            # output layout and score
            results.append('\n'.join([''.join(row) for row in layout]))
            results.append(f"score: {score}")
        # next step
        count += 1
        # Even though the break game is over, the flow is still complete, so break is placed last, along with WIN
        if pacNum == 0:
            winner = 'Pacman'
            break
        elif pacmanPos == ghostPos:
            winner = 'Ghost'
            break
    # standard output
    solution += '\n'.join(results)

    return solution, winner

# def evalutionF():


def bfs(start, targets, layout):
    moveOffset = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
    queue = deque([(start, 0)])
    visited = set()
    visited.add(start)
    while queue:
        current, distance = queue.popleft()
        if current in targets:
            return distance
        for move in all_possible_move(current, layout):
            dx, dy = moveOffset[move]
            newPos = (current[0] + dx, current[1] + dy)
            if newPos not in visited:
                visited.add(newPos)
                queue.append((newPos, distance + 1))
    return float('inf')  # If no path found

def all_possible_move(anyPos, layout):
    possibleMoves = []
    moveOffset = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
    for move, (x, y) in moveOffset.items():
        newPos = (anyPos[0]+x, anyPos[1]+y)
        # print('pacmanPos newPos', newPos)
        if layout[newPos[0]][newPos[1]] not in '%':
            possibleMoves.append(move)
    # print('possibleMoves', possibleMoves)
    return sorted(possibleMoves) if possibleMoves else None

def direction_To_position(move, position):
    x, y = position
    moveOffset = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
    dx, dy = moveOffset[move]
    return (x + dx, y + dy)

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])    
    problem_id = 2
    file_name_problem = str(test_case_id)+'.prob' 
    file_name_sol = str(test_case_id)+'.sol'
    path = os.path.join('test_cases','p'+str(problem_id)) 
    problem = parse.read_layout_problem(os.path.join(path,file_name_problem))
    num_trials = int(sys.argv[2])
    verbose = bool(int(sys.argv[3]))
    print('test_case_id:',test_case_id)
    print('num_trials:',num_trials)
    print('verbose:',verbose)
    start = time.time()
    win_count = 0
    for i in range(num_trials):
        solution, winner = better_play_single_ghosts(copy.deepcopy(problem))
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count/num_trials * 100
    end = time.time()
    print('time: ',end - start)
    print('win %',win_p)