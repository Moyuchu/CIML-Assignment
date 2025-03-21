import sys
import grader
import parse
from decimal import Decimal, getcontext
import copy

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
        return (i, j)


def valueUpdate(currentState, action, grid, newValues, noise, discount, livingReward):
    d = {'N': ['N', 'E', 'W'], 'E': ['E', 'S', 'N'],
         'S': ['S', 'W', 'E'], 'W': ['W', 'N', 'S']}
    population = d.get(action)
    weights = [1 - 2 * noise, noise, noise]
    value = 0.0
    expectedValue = 0.0
    if population:
        for item in population:
            nextState = update_state(currentState, item, grid)
            nextI, nextJ = nextState
            value = float(newValues[nextI][nextJ])
            weight = weights[population.index(item)]
            # print('weight', weight, 'value', value)
            qDisval = (livingReward + (discount * value)) * weight
            expectedValue = qDisval + expectedValue
    return float(expectedValue)


def policy_evaluation(problem):
    return_value = ''
    results = []
    discount = problem['discount']
    noise = problem['noise']
    livingReward = problem['livingReward']
    iterations = problem['iterations']
    grid = problem['grid']
    policy = problem['policy']
    a = ''
    for row in grid:
        for char in row:
            if char.isalpha() and char.isascii():
                a += char

    grid_matrix = []
    for row in grid:
        row_matrix = []
        for num in row:
            if num == a:
                row_matrix.append('_')
            elif num == '_' or num == '#':
                row_matrix.append(num)
            else:
                num = f"{float(num):.2f}"
                row_matrix.append(num)
        grid_matrix.append(row_matrix)
    count = 0

    newValues = [
        [0.00 for _ in range(len(grid[0]))] for _ in range(len(grid))]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if policy[i][j] == '#':
                newValues[i][j] = policy[i][j]

    results.append(f"V^pi_k={count}")
    for row in newValues:
        line = "".join([f"|{float(val):7.2f}|" if not isinstance(val,
                                                                 str) else f"|{' ##### ':<7}|" for val in row])
        results.append(line)
    count = 1
    while count < iterations:
        nowValues = copy.deepcopy(newValues)
        expectedValue = 0.00
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                cell = grid_matrix[i][j]
                action = policy[i][j]
                if action == '#':
                    pass
                elif action != 'exit':
                    expectedValue = valueUpdate(
                        (i, j), action, grid_matrix, newValues, noise, discount, livingReward)
                    nowValues[i][j] = float(expectedValue)
                elif action == 'exit':
                    nowValues[i][j] = float(cell)
        newValues = nowValues
        results.append(f"V^pi_k={count}")
        for row in newValues:
            line = "".join([f"|{float(val):7.2f}|" if not isinstance(val,
                                                                     str) else f"|{' ##### ':<7}|" for val in row])
            results.append(line)
        count += 1
    return_value = '\n'.join(results)
    return return_value


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    # test_case_id = -7
    problem_id = 2
    grader.grade(problem_id, test_case_id, policy_evaluation,
                 parse.read_grid_mdp_problem_p2)
