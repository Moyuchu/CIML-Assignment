import sys
import grader
import parse
import random
from collections import Counter
from decimal import Decimal, getcontext


getcontext().prec = 10


def update_state(currentState, action, grid):
    i, j = currentState
    if action == 'N' and i > 0 and grid[i - 1][j] != '#':
        return (i - 1, j)
    elif action == 'S' and i < len(grid) - 1 and grid[i + 1][j] != '#':
        return (i + 1, j)
    elif action == 'E' and j < len(grid[0]) - 1 and grid[i][j + 1] != '#':
        return (i, j + 1)
    elif action == 'W' and j > 0 and grid[i][j - 1] != '#':
        return (i, j - 1)
    else:
        return currentState


def format_decimal(number):
    formatted = f"{number:.2f}"
    if formatted.endswith('.00'):
        return formatted[:-1]
    else:
        return formatted.rstrip('0').rstrip('.')


def print_state(results, grid_matrix, cuReward):
    results.append(f'New state:')
    for row in grid_matrix:
        results.append(''.join([cell.rjust(5) for cell in row]))
    results.append(f'Cumulative reward sum: {format_decimal(cuReward)}')


def play_episode(problem):
    experience = ''
    results = []
    seed = problem['seed']
    if seed != -1:
        random.seed(seed, version=1)
    noise = problem['noise']
    livingReward = problem['livingReward']
    grid = problem['grid']
    policy = problem['policy']
    a = ''
    for row in grid:
        for char in row:
            if char.isalpha() and char.isascii():
                a += char
    grid_matrix = []
    for row in grid:
        new_row = []
        for cell in row:
            if cell != ' ':
                new_row.append(cell)
        grid_matrix.append(new_row)
    startState = None
    for i, row in enumerate(grid_matrix):
        for j, cell in enumerate(row):
            if cell == a:
                startState = (i, j)
                break
        if startState:
            break

    currentState = startState
    if currentState is None:
        return
    cuReward = 0.0
    count = 1
    original = 'S'
    results.append(f'Start state:')
    grid[currentState[0]][currentState[1]] = 'P'
    for row in grid:
        results.append(''.join([cell.rjust(5) for cell in row]))
    results.append(f'Cumulative reward sum: 0.0')
    while True:
        x, y = currentState
        intendedAction = policy[x][y]
        d = {'N': ['N', 'E', 'W'], 'E': ['E', 'S', 'N'],
             'S': ['S', 'W', 'E'], 'W': ['W', 'N', 'S']}
        noised_action = random.choices(population=d[intendedAction], weights=[
            1 - noise * 2, noise, noise])[0]
        reward = livingReward
        cuReward = Decimal(reward) + Decimal(cuReward)
        exitReward = 0.0
        grid_matrix[x][y] = original
        currentState = update_state(currentState, noised_action, grid)
        original = grid_matrix[currentState[0]][currentState[1]]
        if policy[currentState[0]][currentState[1]] == 'exit':
            exitReward = float(grid_matrix[currentState[0]][currentState[1]])

        grid_matrix[currentState[0]][currentState[1]] = 'P'
        results.append(f'-------------------------------------------- ')
        results.append(
            f'Taking action: {noised_action} (intended: {intendedAction})')
        results.append(f"Reward received: {reward}")
        print_state(results, grid_matrix, cuReward)

        if policy[currentState[0]][currentState[1]] == 'exit':
            cuReward = Decimal(exitReward) + Decimal(cuReward)
            grid_matrix[currentState[0]][currentState[1]] = original
            results.append(f'-------------------------------------------- ')
            results.append(
                f'Taking action: exit (intended: exit)')
            results.append(f"Reward received: {float(original)}")
            print_state(results, grid_matrix, cuReward)
            break
        count += 1
    experience += '\n'.join(results)

    return experience


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    # test_case_id = 1
    problem_id = 1
    grader.grade(problem_id, test_case_id, play_episode,
                 parse.read_grid_mdp_problem_p1)
