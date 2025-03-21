import sys, parse
import time, os, copy
import random, math
from collections import deque
def expecti_max_multiple_ghosts(problem, k):
    #Your p6 code here
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
    ghostIndex = {ghost: (index + 1) for index, ghost in enumerate(sorted(ghostPos.keys()))}
    original = {'W': ' ', 'X': ' ', 'Y': ' ', 'Z': ' '}
    beansPos = []
    pacNum = 0
    ghostNum = 0
    possibleMoves = {}
    path = []
    # print('start;ghostIndex', ghostIndex)
    # single list's index and cell
    for i, row in enumerate(layout):
        # single list's inside
        for j, item in enumerate(row):
            if item != '%':  # Assuming '%' represents walls
                everyPos = (i, j)
                possibleMove = layout_possible_move(everyPos, layout)
                possibleMoves[everyPos] = possibleMove
                # print('possibleMove', possibleMove)
            if item == 'P':
                pacmanPos = (i, j)
            elif item in ghostPos:
                ghostPos[item] = (i, j)
                # print('ghostPos', ghostPos)
                ghostNum += 1
            elif item == '.':
                beansPos.append((i, j))
                pacNum += 1
    depth = k
    state = {
        'pacman': pacmanPos,
        'ghosts': ghostPos,
        'bean': beansPos,
        'layout': layout,
        'original': original
    }
    count = 0
    # the state before moving first step
    results.append(f'{count}')
    results.append('\n'.join([''.join(row) for row in layout]))
    # while True:
    # first step moved by pacman
    newState, bestMove= expectimax_decision(state, depth)
    # pathCreate(state, bestMove, depth)
    if not newState['bean']:
        # print('WINPacman')
        winner = 'Pacman'
    else:
        # print('LOSEGhost')
        winner = 'Ghost'
    solution += '\n'.join(results)
    return solution, winner
def showImage(state):
    layout = state['layout']
    check = []
    checkT = ''
    check.append('\n'.join([''.join(row) for row in layout]))
    checkT += '\n'.join(check)
    return checkT
def agentNum(state):
    count = 1
    for ghost in state['ghosts']:
        if state['ghosts'].get(ghost) is not None:
            count += 1
    return count
def pathNum(state, depthNow, agentIndex):
    return agentNum(state) * ((depthNow) // agentNum(state)) + agentIndex
def expectimax_decision(state, depth):

    # print('MINIMAX_decision!!showImage', showImage(state), 'agentIndex', agentIndex)
    maxScore = float('-inf')
    bestMove = None
    nextState = {}
    possibleMoves = all_possible_move(state, 0)
    for move in possibleMoves:
        path = [()] * (math.ceil(depth/2)+agentNum(state)*(depth//2))
        nextState = next_state(state, 0, move)
        bestMove, moveValue, nextState = value(nextState, 0, depth, 1, path)
        if moveValue > maxScore:
            maxScore = moveValue
            bestMove = move
        if not nextState['bean']:
            # path[pathNum(state, depth+1, agentIndex)] = (depth, agentIndex, bestMove, pathNum(state, depth + 1, agentIndex))
            return nextState, bestMove
    nextState['pacman'] = None
    return nextState, bestMove
def max_value(state, depthNow, depth, agentIndex, path):
    # print('MAX_value!!showImage', showImage(state))
    possibleMoves = all_possible_move(state, agentIndex)
    v = -float('inf')
    # print('possibleMoves', possibleMoves)
    bestMove = None
    for move in possibleMoves:
        nextState = next_state(state, agentIndex, move)
        m, moveValue, newState = value(nextState, depthNow+1, depth, 1, path)
        if moveValue > v:
            v = moveValue
            bestMove = move
            # path[pathNum(state, depthNow, agentIndex)] = (depthNow, agentIndex, bestMove, pathNum(state, depthNow, agentIndex))
        if isWin(newState):
            break
    return bestMove, v, newState
def exp_value(state, depthNow, depth, agentIndex, path):
    # print('EXP_value!!showImage', showImage(state))
    possibleMoves = all_possible_move(state, agentIndex)
    v = 0.0
    count = len(possibleMoves)
    bestMove = None
    if possibleMoves:
        for move in possibleMoves:
            nextState = next_state(state, agentIndex, move)
            if agentIndex + 1 == agentNum(state):
                # print('180行')
                m, moveValue, newState = value(nextState, depthNow+1, depth, 0, path)
                path[pathNum(state, depthNow, agentIndex)] = (depthNow,agentIndex, bestMove, all_possible_move(newState, agentIndex),pathNum(state, depthNow, agentIndex))
            else:
                # print('186行')
                m, moveValue, newState = value(nextState, depthNow, depth, agentIndex + 1, path)
                path[pathNum(state, depthNow, agentIndex)] = (depthNow,agentIndex, bestMove, all_possible_move(newState, agentIndex),pathNum(state, depthNow, agentIndex))
            v += moveValue
    else:
        move = None
        nextState = next_state(state, agentIndex, move)
        count = 1
        if agentIndex + 1 == agentNum(state):
            m, moveValue, newState = value(nextState, depthNow+1, depth, 0, path)
            path[pathNum(state, depthNow, agentIndex)] = (depthNow,agentIndex, bestMove, all_possible_move(newState, agentIndex),pathNum(state, depthNow, agentIndex))
        else:
            m, moveValue, newState = value(nextState, depthNow, depth, agentIndex + 1, path)
            path[pathNum(state, depthNow, agentIndex)] = (depthNow,agentIndex, bestMove, all_possible_move(newState, agentIndex), pathNum(state, depthNow, agentIndex))
        v += moveValue
        bestMove = move
    return bestMove, v/count, newState
def value(state, depthNow, depth, agentIndex, path):
    # if isWin(state):
    #     return None, float('inf'), state
    if depth == depthNow or isWin(state) or isLose(state):
        # print('MIN暂时结束', 'bestmove_evaluation(state)', bestmove_evaluation(state))
        return None, bestmove_evaluation(state), state
    if agentIndex == 0:
        return max_value(state, depthNow, depth, agentIndex, path)
    if agentIndex > 0:
        return exp_value(state, depthNow, depth, agentIndex, path)
def next_state(state, agentIndex, move):
    newState = copy.deepcopy(state)
    pacmanPos = newState['pacman']
    ghostPos = newState['ghosts']
    layout = newState['layout']
    original = newState['original']
    if agentIndex == 0:  # Pacman
        x, y = pacmanPos
        newPos = direction_To_position(move, pacmanPos)
        newState['pacman'] = newPos
        if pacmanPos in ghostPos.values():
            for ghost, pos in ghostPos.items():
                if pos == pacmanPos:
                    # Whether P goes to ghost or ghost goes to P, the final display is ghost
                    newState['layout'][newPos[0]][newPos[1]] = ghost
                    newState['pacman'] = None
                    break
        else:
            if newPos in newState['bean']:
                newState['bean'].remove(newPos)
            newState['layout'][newPos[0]][newPos[1]] = 'P'
            # passed through point will be ' '
        newState['layout'][x][y] = ' '
    else:  # Ghosts
        if not move:
            return state
        indexGhost = {1: 'W', 2: 'X', 3: 'Y', 4: 'Z'}
        ghost = indexGhost.get(agentIndex)
        oldI, oldJ = ghostPos[ghost]
        newPosG = direction_To_position(move, ghostPos[ghost])
        ghostPos[ghost] = newPosG
        # with or without pac, the coordinates that w passes through are reverted
        # output layout and score
        # pacman already was eaten by ghost
        newState['layout'][oldI][oldJ] = original[ghost]
        # record the new position's value to recover the last position in next step
        original[ghost] = newState['layout'][newPosG[0]][newPosG[1]]
        # change ghost to next
        newState['layout'][newPosG[0]][newPosG[1]] = ghost
        if pacmanPos in ghostPos.values():
            newState['pacman'] = None
    return newState
# evaluation for state now
def bestmove_evaluation(state):
    pacmanPos = state['pacman']
    ghostPos = state['ghosts']
    layout = state['layout']
    beansPos = state['bean']
    moveBeansTonew = {}
    scoreBFS = 0
    evaluateScore = -100
    # record the next direction of pacman
    # calculate straight-line distance of ghost and pacman or bean and pacman
    if isWin(state):
        return float('inf')
    elif isLose(state):
        return float('-inf')
    else:
        # use BFS to calculate
        beansTonew = min(bfs(pacmanPos, bean, layout) for bean in beansPos)
        # the nearest ghost
        ghostTonew = min(bfs(pacmanPos, pos, layout) for pos in ghostPos.values() if pos)
        # reduce the effect of distant ghosts, so use math.log
        scoreBFS += ((math.log(ghostTonew + 1)) * 2 - beansTonew / 10)
        # if the next step is ghost, or if pacman don't die and will eat beans, increase the impact on the evaluation
        if ghostTonew == 0:
            scoreBFS -= 100
        elif ghostTonew == 1:
            scoreBFS -= 3
        if beansTonew == 0 and (ghostTonew > 2 or len(beansPos) == 1):
            scoreBFS += 100
    # choose the max score
    if scoreBFS >= evaluateScore:
        evaluateScore = scoreBFS
    return evaluateScore
def bfs(start, targets, layout):
    moveOffset = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
    distances = {}
    frontier = deque([(start, 0)])
    exploredSet = set()
    # print('bfs;targets', targets)
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
def all_possible_move(state, agentIndex):
    possibleMoves = []
    moveOffset = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
    ghostPos = state['ghosts']
    for move, (x, y) in moveOffset.items():
        if agentIndex == 0:
            anyPos = state['pacman']
            newPos = (anyPos[0] + x, anyPos[1] + y)
            if state['layout'][newPos[0]][newPos[1]] not in '%':
                possibleMoves.append(move)
        else:
            indexGhost = {1: 'W', 2: 'X', 3: 'Y', 4: 'Z'}
            ghost = indexGhost.get(agentIndex)
            anyPos = ghostPos.get(ghost)
            if anyPos is None:
                continue
            newPos = (anyPos[0] + x, anyPos[1] + y)
            if state['layout'][newPos[0]][newPos[1]] not in '%WXYZ':
                possibleMoves.append(move)
    return sorted(possibleMoves) if possibleMoves else None
def layout_possible_move(anyPos, layout):
    possibleMoves = []
    moveOffset = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
    for move, (x, y) in moveOffset.items():
        newPos = (anyPos[0] + x, anyPos[1] + y)
        if layout[newPos[0]][newPos[1]] not in '%':
            possibleMoves.append(move)
    # print('possibleMoves', possibleMoves)
    return sorted(possibleMoves) if possibleMoves else None
def isWin(state):
    if not state['bean']:
        return True
    return False
def isLose(state):
    if not state['pacman']:
        return True
    return False
def direction_To_position(move, position):
    x, y = position
    moveOffset = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
    dx, dy = moveOffset[move]
    position = (x + dx, y + dy)
    return position
# def pathCreate(state, move, depthNow):
#     path = []
#     # move = None
#     possibleMoves = all_possible_move(state, 0)
#     if isWin(state):
#         path = [('AAAAAA', state, move)]
#     else:
#         for move in possibleMoves:
#             pathCreate(state, move, depthNow)
#             nextState, bestMove = expectimax_decision(state, depthNow)
#         path.insert(0, ('AAAAAA', state, bestMove))
#     print('path', path)
#     return path
if __name__ == "__main__":
    test_case_id = int(sys.argv[1])    
    problem_id = 6
    file_name_problem = str(test_case_id)+'.prob' 
    file_name_sol = str(test_case_id)+'.sol'
    path = os.path.join('test_cases','p'+str(problem_id)) 
    problem = parse.read_layout_problem(os.path.join(path,file_name_problem))
    k = int(sys.argv[2])
    num_trials = int(sys.argv[3])
    verbose = bool(int(sys.argv[4]))
    print('test_case_id:',test_case_id)
    print('k:',k)
    print('num_trials:',num_trials)
    print('verbose:',verbose)
    start = time.time()
    win_count = 0
    for i in range(num_trials):
        solution, winner = expecti_max_multiple_ghosts(copy.deepcopy(problem), k)
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count/num_trials * 100
    end = time.time()
    print('time: ',end - start)
    print('win %',win_p)