import sys, grader, parse
import collections
# DFS-GSA
def dfs_search(problem):
    #Your p1 code here
    frontier = collections.deque([problem['startState']])
    exploredSet = set()
    exploration_order = []

    print('Initial frontier:', list(frontier))
    while frontier:
        node = frontier.pop()
        node_back = node[-1]
        # exploration_order.append(node_back)
        # print('Exploration:', exploration_order)

        # 避免重复
        if node_back not in exploredSet:
            exploration_order.append(node_back)
            # print('Exploration:', exploration_order)

        if node_back == problem['goalState']:
            solution_path = ' '.join(node)
            # 不包括最后的goal_state
            exploration_order_str = ' '.join(exploration_order[:-1])
            solution = f"{exploration_order_str}\n{solution_path}"
            # print('solution', solution)
            # solution = 'Ar D C\nAr C G'
            return solution

        if node_back not in exploredSet:
            # print('Exploring:',node_back,'...')
            exploredSet.add(node_back)
            # for child in problem['stateSpaceGraph'][node_back]:
            for cost, child in problem['stateSpaceGraph'].get(node_back, []):
                # Ar无法使用
                # frontier.append(node + child)
                if child not in node:
                    new_path = node + [child]  # 创建新路径
                    frontier.append(new_path)
                    # print('new_path', new_path)
            # print('list(frontier)', list(frontier))
            # print('exploredSet', exploredSet)

        # # solution = 'Ar D C\nAr C G'
        #  return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 1
    grader.grade(problem_id, test_case_id, dfs_search, parse.read_graph_search_problem)