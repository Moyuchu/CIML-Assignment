import sys
import grader
import parse
import random
# ###you can run this code using "python p4.py 2"###

# Analysis of Experience:
# After I implemented temporal Difference Learning, the experiment mainly studied the balance
# between exploration and exploitation in reinforcement learning.
# Exploration involves trying new actions to discover their effects, while exploitation uses
# known information to maximize rewards. My approach tries to combine the strengths of both strategies.
# I find that using exploration for value updates is suboptimal. Therefore, I use exploration
# to optimize the selection of the best direction. This method facilitates the exploration in the
# initial stage and uses the exploration to assist in the selection of the optimal direction,
# thus effectively converging to the optimal policy. For hyper-parameter tuning, I mainly adjusted
# epsilon and the parameter k in the exploitation function. I found that these optimizations
# significantly improved the results. During policy validation, I observed that the algorithm
# generally converged after a few iterations, and the convergence results matched the policy validation
# outcomes. Overall, this approach highlights the importance of parameter tuning and the balance
# between exploration and exploitation in reinforcement learning to achieve optimal performance.

# Updates the current state based on the action taken and the grid layout
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
# Takes a value estimate u and a visit count n, and returns an optimistic utility
def f(u, n, k):
    return u + k / n
# converts a 2D grid state to a 1D index
def state_to_index(state, grid_width):
    return state[0] * grid_width + state[1]
# chooses an action (using exploitation)
def choose_action(state, q_values, epsilon, N, k):
    random.seed(5, version=1)
    actions = ['N', 'S', 'E', 'W']
    # check if the state has any unvisited actions
    unvisited_actions = [action for action in actions if (state, action) not in N]
    # between exploration (randomly choosing actions) and exploitation (choosing the optimal action)
    if unvisited_actions:
        return random.choice(unvisited_actions)
    elif random.random() < epsilon:
        return random.choice(actions)  # Explore
    else:
        return max(actions, key=lambda action: f(q_values.get((state, action), 0.0), N.get((state, action), 1), k))

# mainly using exploration
# updates the value of a state-action pair considering noise and discount factors
def valueUpdate(currentState, action, grid, q_values, noise, discount, livingReward, alpha):
    d = {'N': ['N', 'E', 'W'], 'E': ['E', 'S', 'N'],
         'S': ['S', 'W', 'E'], 'W': ['W', 'N', 'S']}
    population = d.get(action)
    weights = [1 - 2 * noise, noise, noise]
    value = 0.0
    expectedValue = 0.0
    # function:
    # Q(s,a) <- (1-alpha) * Q(s,a) + alpha * sample;
    # sample = R(s,a,s') + discount * max_a' Q(s',a')
    for item in population:
        nextState = update_state(currentState, item, grid)
        max_future_q = max(q_values.get((nextState, a), 0.0) for a in ['N', 'S', 'E', 'W'])
        weight = weights[population.index(item)]
        sample = livingReward + discount * max_future_q
        q_value = q_values.get((currentState, action), 0.0)
        q_values[(currentState, action)] = (1 - alpha) * q_value + alpha * sample
        # it was hard to close the optimal results, so I choose to use exploration
        # n_value = N.get((nextState, item), 1)
        # f_value = f(value, n_value, k)
        # 3 direction, chosen one(0.8) and two right directions(0.1)
        expectedValue += sample * weight
    return expectedValue

# implement 'Policy Iteration to Validate Optimal'
def policy_evaluation(policy, q_values, grid, discount, livingReward, iterations):
    grid_width = len(grid[0])
    grid_height = len(grid)
    state_values = {}
    for _ in range(iterations):
        for i in range(grid_height):
            for j in range(grid_width):
                if grid[i][j] in ['#', '1', '-1']:
                    continue
                state = (i, j)
                action = policy[state_to_index(state, grid_width)]
                valueUpdate(state, action, grid, q_values, noise=0.1, discount=discount, livingReward=livingReward, alpha=0.5)
                state_values[state] = {
                    'value': sum(q_values.get((state, a), 0.0) for a in ['N', 'S', 'E', 'W']) / len(['N', 'S', 'E', 'W']),
                    'action': action
                }
    return state_values
# implement 'Temporal Difference Learning'
# use TD Learning to update Q-values and derive a policy
def td_learning(problem):
    discount = problem['discount']
    noise = problem['noise']
    livingReward = problem['livingReward']
    grid = problem['grid']
    grid_width = len(grid[0])
    grid_height = len(grid)
    q_values = {}
    N = {}
    epsilon = 0.9
    k = 5.0
    policy = {}
    unchanged_iterations = 0
    max_unchanged_iterations = 10
    iteration = 0
    while unchanged_iterations < max_unchanged_iterations:
        iteration += 1
        previous_policy = policy.copy()
        for i in range(grid_height):
            for j in range(grid_width):
                if grid[i][j] in ['#', '1', '-1']:
                    continue
                state = (i, j)
                state_index = state_to_index(state, grid_width)
                # choose action based on policy
                if state_index in policy:
                    action = policy[state_index]
                else:
                    action = choose_action(state, q_values, epsilon, N, k)
                # update N
                N[(state, action)] = N.get((state, action), 0) + 1

        for i in range(grid_height):
            for j in range(grid_width):
                if grid[i][j] in ['#', '1', '-1']:
                    continue
                state = (i, j)
                state_index = state_to_index(state, grid_width)
                best_action = None
                best_value = float('-inf')
                for a in ['N', 'S', 'E', 'W']:
                    # use valueUpdate function calculate and update Q value
                    action_value = valueUpdate(state, a, grid, q_values, noise, discount, livingReward, alpha=0.5)
                    if action_value > best_value:
                        best_value = action_value
                        best_action = a
                policy[state_index] = best_action
            if policy == previous_policy:
                unchanged_iterations += 1
            else:
                unchanged_iterations = 0
        # epsilon decay
        epsilon *= 0.9
    # converged
    print(f"Converged after {iteration} iterations.")

    state_values = policy_evaluation(policy, q_values, grid, discount, livingReward, iterations=20)
    if state_values is None:
        print("Error: policy_evaluation returned None")
        return
    # implement 'Intuitive Experiments Conducted by Myself'
    # print policy
    for state_index, action in policy.items():
        print(f"Policy({state_index}) = {action}")
    # policy evaluation
    for state, info in state_values.items():
        print(f"State: {state}, Action: {info['action']}")

    return policy


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 4
    problem = parse.read_grid_mdp_problem_p4(
        f"test_cases/p4/{test_case_id}.prob")
    print(td_learning(problem))
