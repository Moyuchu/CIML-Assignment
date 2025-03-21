import math
import sys, parse
import time, os, copy
import random
from collections import deque

# Pacman play against up to 4 random Ghost
def better_play_multiple_ghosts(problem):
    #Your p4 code here
    EAT_FOOD_SCORE = 10
    PACMAN_EATEN_SCORE = -500
    PACMAN_WIN_SCORE = 500
    PACMAN_MOVING_SCORE = -1
    seed = problem['seed']
    if seed != -1:
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
    beansPos = []
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
                beansPos.append((i, j))
                pacNum += 1
    # all possible moves for pacman and ghost in each point
    possibleMoves = {}
    for i, row in enumerate(layout):
        for j, item in enumerate(row):
            if item != '%':  # Assuming '%' represents walls
                everyPos = (i, j)
                possibleMove = all_possible_move(everyPos, layout)
                possibleMoves[everyPos] = possibleMove
    count = 0
    # the state before moving first step
    results.append(f'{count}')
    results.append('\n'.join([''.join(row) for row in layout]))

    while True:
        if count % (ghostNum + 1) == 0:
            # !!MAIN CODE for pacman
            count += 1
            bestMove = evalution_function(possibleMoves, pacmanPos,pacNum, ghostPos, beansPos, layout)
            moveP = bestMove
            # pacmanPos = move
            results.append(f"{count}: P moving {moveP}")
            score += PACMAN_MOVING_SCORE
            x, y = pacmanPos
            pacmanPos = direction_To_position(moveP, pacmanPos)
            if pacmanPos in ghostPos.values():
                score += PACMAN_EATEN_SCORE
                for ghost, pos in ghostPos.items():
                    if pos == pacmanPos:
                        # Whether P goes to ghost or ghost goes to P, the final display is ghost
                        layout[pacmanPos[0]][pacmanPos[1]] = ghost
                        break
            else:
                # eat bean
                if layout[pacmanPos[0]][pacmanPos[1]] == '.':
                    # print('eat')
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
            for ghost in sorted(ghostPos.keys()):
                # if this problem not have this ghost, then continue
                if ghostPos[ghost] == None:
                    continue
                # check which positions could be moved to
                count += 1
                moveG = possible_ghost_position(ghostPos[ghost], layout)
                # moveG = random.choice(possibleMoves[ghostPos[ghost]])
                results.append(f"{count}: {ghost} moving {moveG}")
                # record the old position to recover the last position in next step
                oldI, oldJ = ghostPos[ghost]
                # stuck by '%WXYZ'
                if moveG == None:
                    results.append(f"{count}: {ghost} moving ")
                    results.append('\n'.join([''.join(row) for row in layout]))
                    results.append(f"score: {score}")
                    continue
                # set newPos for readable, make sure the next position caused by this move
                newPos = direction_To_position(moveG, ghostPos[ghost])
                ghostPos[ghost] = newPos
                # whether ghost will eat Pacman
                if pacmanPos == ghostPos[ghost]:
                    score += PACMAN_EATEN_SCORE
                # with or without pac, the coordinates that w passes through are reverted
                layout[oldI][oldJ] = original[ghost]
                # record the new position's value to recover the last position in next step
                original[ghost] = layout[newPos[0]][newPos[1]]
                # change ghost to next
                layout[newPos[0]][newPos[1]] = ghost
                # output layout and score
                results.append('\n'.join([''.join(row) for row in layout]))
                results.append(f"score: {score}")
                # pacman already was eaten by ghost
                if pacmanPos in ghostPos.values():
                    break
                if not beansPos:
                    break
        if not beansPos:
            winner = 'Pacman'
            break
        elif pacmanPos in ghostPos.values():
            winner = 'Ghost'
            break
    # standard output
    solution += '\n'.join(results)
    # print('solution', solution)
    return solution, winner
def bfs(start, targets, layout):
    moveOffset = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
    distances = {}
    frontier = deque([(start, 0)])
    exploredSet = set()
    while frontier:
        current, distance = frontier.popleft()
        distances[current] = distance
        if current == targets:
            return distance
        for move, (dx, dy) in moveOffset.items():
            newPos = (current[0] + dx, current[1] + dy)
            if newPos not in exploredSet and layout[newPos[0]][newPos[1]] != '%':  # Assuming '%' is a wall
                exploredSet.add(newPos)
                frontier.append((newPos, distance + 1))
    return float('inf')  # If no path found
def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
def move_closed(possibleMoves, pacmanPos, beansToPAbsMinPos, ghostToPMinPos, layout):
    min_distance = float('inf')
    best_ghost_distance = float('-inf')
    bestMoveB = None
    for move in possibleMoves[pacmanPos]:
        newPos = direction_To_position(move, pacmanPos)
        bean_distance = bfs(newPos, beansToPAbsMinPos, layout)
        ghost_distance = bfs(newPos, ghostToPMinPos, layout)
        if bean_distance < min_distance or (bean_distance == min_distance and ghost_distance > best_ghost_distance):
            min_distance = bean_distance
            best_ghost_distance = ghost_distance
            bestMoveB = move
    return bestMoveB
def evalution_function(possibleMoves, pacmanPos, pacNum, ghostPos, beansPos, layout):
    bestMove = None
    bestScore = float('-inf')
    # moveOffset = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
    equalScoreMoves = {}
    ghostToPMinPos = min((pos for pos in ghostPos.values() if pos), key=lambda pos: manhattan_distance(pacmanPos, pos))
    ghostToPAbs = min(manhattan_distance(pacmanPos, pos) for pos in ghostPos.values() if pos)
    beansToPAbsMinPos = min((bean for bean in beansPos), key=lambda bean: manhattan_distance(pacmanPos, bean))
    for move in possibleMoves[pacmanPos]:
        scoreBFS = 0
        newPos = direction_To_position(move, pacmanPos)
        ghostTonewAbs = min(manhattan_distance(newPos, pos) for pos in ghostPos.values() if pos)
        beansTonewAbs = min(manhattan_distance(newPos, bean) for bean in beansPos)
        if (ghostTonewAbs > 2 or pacNum == 1) and beansTonewAbs == 0:
            bestMove = move
            break
        elif ghostTonewAbs >= 3 and ghostToPAbs >= 3:
            bestMove = move_closed(possibleMoves, pacmanPos, beansToPAbsMinPos, ghostToPMinPos, layout)
            break
        elif ghostTonewAbs < 2:
            continue
        ghostTonew = min(bfs(newPos, pos, layout) for pos in ghostPos.values() if pos)
        beansTonew = min(bfs(newPos, bean, layout) for bean in beansPos)
        if ghostTonewAbs == 1:
            scoreBFS -= 3
        scoreBFS = ((math.log(ghostTonew + 1)) * 2 - beansTonew / 10)
        if scoreBFS > bestScore:
            bestScore = scoreBFS
            bestMove = move
        elif scoreBFS == bestScore:
            equalScoreMoves = {}
            equalScoreMoves[move] = beansTonew
        if len(equalScoreMoves) > 1:
            bestMove = min(equalScoreMoves, key=equalScoreMoves.get)
    if not bestMove:
        bestMove = random.choice(possibleMoves[pacmanPos])
    return bestMove
def all_possible_move(anyPos, layout):
    possibleMoves = []
    moveOffset = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
    for move, (x, y) in moveOffset.items():
        newPos = (anyPos[0]+x, anyPos[1]+y)
        if layout[newPos[0]][newPos[1]] not in '%':
            possibleMoves.append(move)
    # print('possibleMoves', possibleMoves)
    return sorted(possibleMoves) if possibleMoves else None
def possible_ghost_position(ghostPos, layout):
    possibleMoves = []
    moveOffset = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
    for move, (x, y) in moveOffset.items():
        newPos = (ghostPos[0] + x, ghostPos[1] + y)
        # print('ghost newPos', newPos)
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
    problem_id = 4
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
        solution, winner = better_play_multiple_ghosts(copy.deepcopy(problem))
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count/num_trials * 100
    end = time.time()
    print('time: ',end - start)
    print('win %',win_p)