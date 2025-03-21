import sys, parse, grader
from heapq import heappush, heappop
# UCS-GSA
def ucs_search(problem):
    #Your p3 code here
    frontier = []
    heappush(frontier, (0, problem['startState']))
    exploredSet = set()
    exploration_order = []
    # print('Initial frontier:', list(frontier))

    while frontier:
        node = heappop(frontier)
        # print('node', node, 'node[0]', node[0], 'node[1]', node[1], 'node[1][-1]', node[1][-1])
        # if node[1] not in exploredSet:
        #     exploration_order.append(node)
        #     print('Exploration:', exploration_order)

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
                # heappush(frontier, (node[0] + child[0], node[1] + child[1]))
                # print('child', child, 'cost', cost)
                heappush(frontier, (node[0] + cost, node[1] + [child]))
            # print(list(frontier))
            # print(exploredSet)
    # solution = 'S D B C\nS C G'
    # return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 3
    grader.grade(problem_id, test_case_id, ucs_search, parse.read_graph_search_problem)