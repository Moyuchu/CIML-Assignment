import sys
import grader
import parse
from decimal import Decimal, getcontext
import copy

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
            qDisval = (livingReward + (discount * value)) * weight
            expectedValue = qDisval + expectedValue
    return float(expectedValue)


def value_iteration(problem):
    return_value = ''
    results = []
    discount = problem['discount']
    noise = problem['noise']
    livingReward = problem['livingReward']
    iterations = problem['iterations']
    grid = problem['grid']
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
            if grid_matrix[i][j] == '#':
                newValues[i][j] = grid_matrix[i][j]
    results.append(f"V_k={count}")
    for row in newValues:
        line = "".join([f"|{float(val):7.2f}|" if not isinstance(val,
                                                                 str) else f"|{' ##### ':<7}|" for val in row])
        results.append(line)
    count = 1
    policy = [['' for _ in range(len(grid[0]))]
              for _ in range(len(grid))]

    while count < iterations:
        nowValues = copy.deepcopy(newValues)
        d = {'N': ['N', 'E', 'W'], 'E': ['E', 'S', 'N'],
             'S': ['S', 'W', 'E'], 'W': ['W', 'N', 'S']}
        expectedValue = 0.00
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                cell = grid_matrix[i][j]
                maxValue = float('-inf')
                bestAction = None
                for action in ['N', 'S', 'E', 'W']:
                    if cell == '#':
                        policy[i][j] = cell
                        break
                    elif cell == '_':
                        expectedValue = valueUpdate(
                            (i, j), action, grid_matrix, newValues, noise, discount, livingReward)
                        if expectedValue > maxValue:
                            maxValue = expectedValue
                            bestAction = action
                        nowValues[i][j] = float(maxValue)
                        policy[i][j] = str(bestAction)
                    else:
                        nowValues[i][j] = float(cell)
                        policy[i][j] = str(' x ')
                        break
        newValues = nowValues
        results.append(f"V_k={count}")
        for row in newValues:
            line = "".join([f"|{float(val):7.2f}|" if not isinstance(
                val, str) else f"|{' ##### ':<7}|" for val in row])
            results.append(line)
        results.append(f"pi_k={count}")
        for row in policy:
            line = "".join(
                [f"|{val.strip().center(3)}|" for val in row])
            results.append(line)
        count += 1
    return_value = '\n'.join(results)
    return return_value


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    #test_case_id = -4
    problem_id = 3
    grader.grade(problem_id, test_case_id, value_iteration,
                 parse.read_grid_mdp_problem_p3)
