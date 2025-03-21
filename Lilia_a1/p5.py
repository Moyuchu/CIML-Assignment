import sys, parse, grader
from heapq import heappush, heappop
# A*-GSA
def astar_search(problem):
    #Your p5 code here
    frontier = []
    start_state = problem['startState']
    romaniaH = problem['romaniaH']
    # print('start_state', start_state)
    # print('romaniaH', romaniaH)
    # print('romaniaH[start_state]', romaniaH[start_state[0]])
    heappush(frontier, (romaniaH[start_state[0]], start_state))
    exploredSet = set()
    exploration_order = []
    # print('Initial frontier:', list(frontier))

    while frontier:
        node = heappop(frontier)
        # print('Exploring:', node[1], 'at cost', node[0])

        if node[1][-1] == problem['goalState']:
            solution_path = ' '.join(node[1])
            exploration_order_str = ' '.join(exploration_order)
            solution = f"{exploration_order_str}\n{solution_path}"
            # print('solution', solution)
            return solution

        if node[1][-1] not in exploredSet:
            # print('Exploring:', node[1][-1], 'at cost', node[0])
            exploredSet.add(node[1][-1])
            exploration_order.append(node[1][-1])
            for cost, child in problem['stateSpaceGraph'][node[1][-1]]:
                # print('child', child, 'cost', cost, '[child]', [child])
                heappush(frontier, (node[0] + cost - romaniaH[node[1][-1]] + romaniaH[child], node[1] + [child]))
            # print(list(frontier))
            # print(exploredSet)
    # solution = 'S D C B\nS C G'
    # return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 5
    grader.grade(problem_id, test_case_id, astar_search, parse.read_graph_search_problem)