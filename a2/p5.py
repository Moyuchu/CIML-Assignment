import math
import sys, parse
import time, os, copy
import random
from collections import deque
def min_max_multiple_ghosts(problem, k):
    #Your p5 code here
    # initialize the random seed if provided
    seed = problem['seed']
    if seed != -1:
        random.seed(seed, version=1)
    solution = ''
    # print('k', k)
    # Import the graph and random seed of the problem
    layout = problem['layout']
    results = []
    # Record the seed value
    results.append(f'seed: {seed}')
    # position pf pacman & ghost
    pacmanPos = None
    ghostPos = {'W': None, 'X': None, 'Y': None, 'Z': None}
    ghostIndex = {ghost: (index+1) for index, ghost in enumerate(sorted(ghostPos.keys()))}
    original = {'W': ' ', 'X': ' ', 'Y': ' ', 'Z': ' '}
    beansPos = []
    pacNum = 0
    ghostNum = 0
    score = 0
    possibleMoves = {}
    depthNow = 0
    # single list's index and cell
    for i, row in enumerate(layout):
        # single list's inside
        for j, item in enumerate(row):
            if item != '%':  # Assuming '%' represents walls
                everyPos = (i, j)
                possibleMove = layout_possible_move(everyPos, layout)
                possibleMoves[everyPos] = possibleMove
            if item == 'P':
                pacmanPos = (i, j)
            elif item in ghostPos:
                ghostPos[item] = (i, j)
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
    while True:
        # first step moved by pacman
        bestMove, state, newState = minimax_decision(state, depth, 0)
        results.append('\n'.join([''.join(row) for row in layout]))
        results.append(f"score: {score}")
        # check if all beans are eaten
        if not newState['bean']:
            winner = 'Pacman'
            break
        else:
            winner = 'Ghost'
            break
    solution += '\n'.join(results)
    # print('solution', solution)
    return solution, winner
# show image of state now
def showImage(state):
    layout = state['layout']
    check = []
    checkT = ''
    check.append('\n'.join([''.join(row) for row in layout]))
    checkT += '\n'.join(check)
    return checkT
# algorithm of minimax_decision
def minimax_decision(state, depth, agentIndex):
    alpha = -float('inf')
    beta = float('inf')
    depthNow = 0
    maxScore = float('-inf')
    bestMove = []
    nextState = {}
    possibleMoves = all_possible_move(state, agentIndex)
    for move in possibleMoves:
        # the next state of evey move
        nextState = next_state(state, agentIndex, move)
        # value included: mav_value and min_value; here is max_value for pacman first move
        m, moveValue, nextState = value(nextState, 0, depth, 1, alpha, beta)
        if moveValue > maxScore:
            bestMove = []
            maxScore = moveValue
            alpha = moveValue
            bestMove.append(move)
        elif moveValue == maxScore:
            bestMove.append(move)
        if not nextState['bean']:
            return bestMove, state, nextState
    nextState['pacman'] = None
    # if same value, choose the random move
    return random.choice(bestMove), state, nextState

def max_value(state, depthNow, depth, agentIndex, alpha, beta):
    if depth == depthNow:
        return None, bestmove_evaluation(state), state
    if isWin(state) or isLose(state):
        return None, bestmove_evaluation(state), state
    possibleMoves = all_possible_move(state, agentIndex)
    v = -float('inf')
    bestMove = None
    for move in possibleMoves:
        nextState = next_state(state, agentIndex, move)
        m, moveValue, newState = value(nextState, depthNow+1, depth, 1, alpha, beta)
        if moveValue > v:
            v = moveValue
            bestMove = move
        if v > beta:
            return bestMove, v, newState
        alpha = max(alpha, v)
    return bestMove, v, newState
def min_value(state, depthNow, depth, agentIndex, alpha, beta):
    if depth == depthNow:
        return None, bestmove_evaluation(state), state
    if isWin(state) or isLose(state):
        return None, bestmove_evaluation(state), state
    possibleMoves = all_possible_move(state, agentIndex)
    v = float('inf')
    bestMove = None
    if possibleMoves:
        for move in possibleMoves:
            nextState = next_state(state, agentIndex, move)
            if agentIndex + 1 == agentNum(state):
                m, moveValue, newState = value(nextState, depthNow+1, depth, 0, alpha, beta)
            else:
                m, moveValue, newState = value(nextState, depthNow, depth, agentIndex+1, alpha, beta)
            if moveValue < v:
                v = moveValue
                bestMove = move
            if v < alpha:
                return bestMove, v, newState
            beta = min(beta, v)
        return bestMove, v, newState
    else:
        move = None
        nextState = next_state(state, agentIndex, move)
        if agentIndex + 1 == agentNum(state):
            m, moveValue, newState = value(nextState, depthNow+1, depth, 0, alpha, beta)
        else:
            m, moveValue, newState = value(nextState, depthNow, depth, agentIndex + 1, alpha, beta)
        if moveValue < v:
            v = moveValue
    return bestMove, v, newState
def value(state, depthNow, depth, agentIndex, alpha, beta):
    if depth == depthNow or isWin(state) or isLose(state):
        return None, bestmove_evaluation(state), state
    if agentIndex == 0:
        return max_value(state, depthNow, depth, agentIndex, alpha, beta)
    if agentIndex > 0:
        return min_value(state, depthNow, depth, agentIndex, alpha, beta)
def agentNum(state):
    count = 1
    for ghost in state['ghosts']:
        if state['ghosts'].get(ghost) is not None:
            count += 1
    return count
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
                if not newState['bean']:
                    newState['bean'] = None
            newState['layout'][newPos[0]][newPos[1]] = 'P'
            # passed through point will be ' '
        newState['layout'][x][y] = ' '
    else:  # Ghosts
        if not move:
            return state
        indexGhost = {1: 'W', 2: 'X', 3: 'Y', 4: 'Z'}
        ghost = indexGhost.get(agentIndex)
        oldI, oldJ = ghostPos[ghost]
        newPos = direction_To_position(move, ghostPos[ghost])
        ghostPos[ghost] = newPos
        # pacman already was eaten by ghost
        newState['layout'][oldI][oldJ] = original[ghost]
        # record the new position's value to recover the last position in next step
        original[ghost] = newState['layout'][newPos[0]][newPos[1]]
        # change ghost to next
        newState['layout'][newPos[0]][newPos[1]] = ghost
        if pacmanPos in ghostPos.values():
            newState['pacman'] = None
    return newState
def bestmove_evaluation(state):
    pacmanPos = state['pacman']
    ghostPos = state['ghosts']
    layout = state['layout']
    beansPos = state['bean']
    evaluateScore = -100
    if isWin(state):
        return float('inf')
    elif isLose(state):
        return float('-inf')
    else:
        # the nearest ghost
        ghostTonew = min(manhattan_distance(pacmanPos, pos) for pos in ghostPos.values() if pos)
        # the nearest bean
        beansTonew = min(manhattan_distance(pacmanPos, bean) for bean in beansPos)
        # reduce the effect of distant ghosts, so use math.log
        scoreBFS = ((math.log(ghostTonew + 1)) * 2 - beansTonew / 10)
        # if the next step is ghost, or if pacman don't die and will eat beans, increase the impact on the evaluation
        if ghostTonew == 0:
            scoreBFS -= 100
        elif ghostTonew == 1:
            scoreBFS -= 3
        if beansTonew == 0 and (ghostTonew > 2 or len(beansPos) == 1):
            scoreBFS += 100
    if scoreBFS >= evaluateScore:
        evaluateScore = scoreBFS
    return evaluateScore
def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

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
# all possible move
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
# layout possible move
def layout_possible_move(anyPos, layout):
    possibleMoves = []
    moveOffset = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
    for move, (x, y) in moveOffset.items():
        newPos = (anyPos[0]+x, anyPos[1]+y)
        if layout[newPos[0]][newPos[1]] not in '%':
            possibleMoves.append(move)
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

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])    
    problem_id = 5
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
        solution, winner = min_max_multiple_ghosts(copy.deepcopy(problem), k)
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count/num_trials * 100
    end = time.time()
    print('time: ',end - start)
    print('win %',win_p)