def read_grid_mdp_problem_p1(file_path):
    # Your p1 code here
    problem = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
    current_section = None

    for line in lines:
        lines = line.strip()
        if line.startswith('seed'):
            problem['seed'] = int(lines.strip().split(': ')[1])
        elif line.startswith('noise:'):
            problem['noise'] = float(line.strip().split(': ')[1])
        elif line.startswith('livingReward:'):
            problem['livingReward'] = float(line.strip().split(': ')[1])
        elif line.startswith('grid:'):
            current_section = 'grid'
            problem['grid'] = []
        elif line.startswith('policy:'):
            current_section = 'policy'
            problem['policy'] = []
        elif current_section == 'grid' and line != 'policy:':
            problem['grid'].append([cell for cell in line.split() if cell])
        elif current_section == 'policy' and line != 'solution':
            parts = line.split()
            newLines = []
            for part in parts:
                if part == 'exit':
                    newLines.append('exit')
                else:
                    newLines.append(part)
            problem['policy'].append(newLines)

    return problem


def read_grid_mdp_problem_p2(file_path):
    # Your p2 code here
    with open(file_path, 'r') as file:
        lines = file.readlines()

    problem = {}
    current_section = None

    for line in lines:
        if line.startswith('discount:'):
            problem['discount'] = float(line.split(': ')[1])
        elif line.startswith('noise:'):
            problem['noise'] = float(line.split(': ')[1])
        elif line.startswith('livingReward:'):
            problem['livingReward'] = float(line.split(': ')[1])
        elif line.startswith('iterations:'):
            problem['iterations'] = int(line.split(': ')[1])
        elif line.startswith('grid:'):
            current_section = 'grid'
            problem['grid'] = []
        elif line.startswith('policy:'):
            current_section = 'policy'
            problem['policy'] = []
        elif current_section == 'grid' and line != 'policy:':
            problem['grid'].append([cell for cell in line.split() if cell])
        elif current_section == 'policy' and line != 'solution':
            parts = line.split()
            newLines = []
            for part in parts:
                if part == 'exit':
                    newLines.append('exit')
                else:
                    newLines.append(part)
            problem['policy'].append(newLines)
    return problem


def read_grid_mdp_problem_p3(file_path):
    # Your p3 code here
    with open(file_path, 'r') as file:
        lines = file.readlines()

    problem = {}
    current_section = None

    for line in lines:
        if line.startswith('discount:'):
            problem['discount'] = float(line.split(': ')[1])
        elif line.startswith('noise:'):
            problem['noise'] = float(line.split(': ')[1])
        elif line.startswith('livingReward:'):
            problem['livingReward'] = float(line.split(': ')[1])
        elif line.startswith('iterations:'):
            problem['iterations'] = int(line.split(': ')[1])
        elif line.startswith('grid:'):
            current_section = 'grid'
            problem['grid'] = []
        elif current_section == 'grid':
            problem['grid'].append([cell for cell in line.split() if cell])
    # print('problem', problem)
    return problem


def read_grid_mdp_problem_p4(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    problem = {}
    current_section = None

    for line in lines:
        if line.startswith('discount:'):
            problem['discount'] = float(line.split(': ')[1])
        elif line.startswith('noise:'):
            problem['noise'] = float(line.split(': ')[1])
        elif line.startswith('livingReward:'):
            problem['livingReward'] = float(line.split(': ')[1])
        elif line.startswith('iterations:'):
            problem['iterations'] = int(line.split(': ')[1])
        elif line.startswith('grid:'):
            current_section = 'grid'
            problem['grid'] = []
        elif current_section == 'grid':
            problem['grid'].append([cell for cell in line.split() if cell])
    # print('problem', problem)
    return problem
