# passed code python3 p1.py -6
import sys, random, grader, parse
# Random Pacman play against a single random Ghost
def random_play_single_ghost(problem):
    #Your p1 code here
    EAT_FOOD_SCORE = 10
    PACMAN_EATEN_SCORE = -500
    PACMAN_WIN_SCORE = 500
    PACMAN_MOVING_SCORE = -1

    solution = ''
    # Import the graph and random seed of the problem
    seed = problem['seed']
    layout = problem['layout']
    # random but unchanged
    random.seed(seed, version=1)
    results = []
    # first row
    results.append(f'seed: {seed}')
    # position pf pacman & ghost
    pacmanPos = None
    ghostPos = None

    o1, o2 = 0, 0
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
                pacNum += 1

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
    original = ' '
    results.append(f'{count}')
    results.append('\n'.join([''.join(row) for row in layout]))
    while True:
        if count % 2 == 0:
            # pacman
            moveP = random.choice(possibleMoves[pacmanPos])
            results.append(f"{count+1}: P moving {moveP}")
            score += PACMAN_MOVING_SCORE

            x, y = pacmanPos
            pacmanPos = direction_To_position(moveP, pacmanPos)

            if pacmanPos == ghostPos:
                score += PACMAN_EATEN_SCORE
                # Whether P goes to W or W goes to P, the final display is W
                layout[pacmanPos[0]][pacmanPos[1]] = 'W'
            else:
                if layout[pacmanPos[0]][pacmanPos[1]] == '.':
                    # print('eat')
                    pacNum -= 1
                    score += EAT_FOOD_SCORE
                    if pacNum == 0:
                        score += PACMAN_WIN_SCORE

                layout[pacmanPos[0]][pacmanPos[1]] = 'P'
            layout[x][y] = ' '
            results.append('\n'.join([''.join(row) for row in layout]))
            results.append(f"score: {score}")

            # layout[i][j] = ' '
        else:
            # !!MAIN CODE for ghost
            moveG = random.choice(possibleMoves[ghostPos])
            results.append(f"{count+1}: W moving {moveG}")

            i, j = ghostPos
            ghostPos = direction_To_position(moveG, ghostPos)

            # whether W will eat Pacman
            if pacmanPos == ghostPos:
                score += PACMAN_EATEN_SCORE
            # with or without pac, the coordinates that w passes through are reverted
            layout[i][j] = original
            # recorded next one
            original = layout[ghostPos[0]][ghostPos[1]]
            # print('already restore')
            layout[ghostPos[0]][ghostPos[1]] = 'W'
            results.append('\n'.join([''.join(row) for row in layout]))
            results.append(f"score: {score}")

        count += 1

        # Even though the break game is over, the flow is still complete, so break is placed last, along with WIN
        if pacNum == 0:
            results.append(f"WIN: Pacman")
            break
        elif pacmanPos == ghostPos:
            results.append(f"WIN: Ghost")
            break

    solution += '\n'.join(results)

    # solution = ''
    return solution

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
    position = (x + dx, y + dy)

    return position

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 1
    grader.grade(problem_id, test_case_id, random_play_single_ghost, parse.read_layout_problem)
