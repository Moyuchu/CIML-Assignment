import os, sys
def read_graph_search_problem(file_path):
    #Your p1 code here
    # problem = ''
    # readfile + 数据处理
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # start&goal
    start_state = lines[0].split(': ')[1].strip().split()
    print(start_state)
    goal_states = lines[1].split(': ')[1].strip().split()
    print(goal_states)

    # node
    state_space_graph = {}
    romaniaH = {}
    # state_space_graph = collections.defaultdict(list)
    for line in lines[2:]:
        if len(line.split()) == 2:
            nodes, h = line.split()
            romaniaH[nodes] = float(h)
            print(romaniaH)
            if nodes not in state_space_graph:
                state_space_graph[nodes] = []

        if len(line.split()) == 3:
            line_start, line_end, cost = line.split()
            # if line_start not in state_space_graph[line_end]:
            #     state_space_graph[line_end].append(line_start)
            cost = float(cost)
            if line_start not in state_space_graph:
                state_space_graph[line_start] = []
            # if line_end not in state_space_graph:
            #     state_space_graph[line_end] = []
                # 避免重复
            # if line_end not in state_space_graph[line_start]:
                # state_space_graph[line_start].append(line_end)
            state_space_graph[line_start].append((cost, line_end))
            print(state_space_graph)

    problem = {
        'stateSpaceGraph': state_space_graph,
        'startState': start_state,
        'goalState': goal_states[0],
        'romaniaH': romaniaH
    }
    print('problem:', problem)

    return problem

def read_8queens_search_problem(file_path):
    #Your p6 code here
    # problem = ''
    # Randomly initialize currentState
    # If cost of currentState == 0 return currentState
    # If min(cost(getNeighbors(currentState))) > cost(currentState)
    # goto step 1 (we have reached a local minimum)
    # Select cheapest neighbor as currentState and goto step 2
    problem = [-1] * 8
    with open(file_path, 'r') as file:
        lines = file.readlines()
    for i, line in enumerate(lines):
        chars = line.strip().split()
        for j, char in enumerate(chars):
            if char == 'q':
                problem[j] = i
    print('problem in parse:', problem)
    return problem

if __name__ == "__main__":
    if len(sys.argv) == 3:
        problem_id, test_case_id = sys.argv[1], sys.argv[2]
        if int(problem_id) <= 5:
            problem = read_graph_search_problem(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        else:
            problem = read_8queens_search_problem(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        print(problem)
    else:
        print('Error: I need exactly 2 arguments!')