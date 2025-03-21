import os, sys
import random
def read_layout_problem(file_path):
    #Your p1 code here
    problem = ''
    # random.seed(8)
    with open(file_path, 'r') as file:
        lines = file.readlines()

    seed = int(lines[0].strip().split(': ')[1])
    random.seed(seed, version=1)
    layout = [list(line.strip()) for line in lines[1:]]
    problem = {
        'seed': seed,
        'layout': layout
    }
    # random.seed(seed)
    # print('problem', problem)
    # print('seed', seed)
    return problem


if __name__ == "__main__":
    if len(sys.argv) == 3:
        problem_id, test_case_id = sys.argv[1], sys.argv[2]
        problem = read_layout_problem(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        print(problem)
    else:
        print('Error: I need exactly 2 arguments!')