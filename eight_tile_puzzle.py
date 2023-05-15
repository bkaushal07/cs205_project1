import copy, time
goal_state= [[1,2,3],[4,5,6],[7,8,0]]

class Node:
    def __init__(self, problem, depth = 0, cost = 0):
        self.problem = problem
        self.depth = depth
        self.cost = cost

def generic_search(root: Node, algorithm):
    nodes = [root]
    max_depth = 0 
    expanded_nodes = 0 
    
    while nodes:
        node = nodes.pop(0) # popping the first element in the list
        # print(node)
        # print(node.problem)
        if node.problem == goal_state:
            print(f'Hooray!!! We did it in {expanded_nodes} steps')
            return node
        nodes = queueing_function(node, nodes, algorithm)        
        expanded_nodes+=1
        max_depth = max(max_depth, node.depth)
    print('NADA!!')
    return None


def queueing_function(node, nodes, algorithm):
    global visited_states # to keep track of the visited states 
    a=copy.deepcopy(node)
    # print(a)

    def update_node_cost(a, algorithm):
        a.depth = node.depth + 1
        if algorithm == '1':
            # print("here")
            a.cost = a.depth
    
    def enqueue_node(a):
        if [a.cost, a.problem] not in visited_states:
            nodes.append(a)
            # print(nodes)
            visited_states.append([a.cost, a.problem])
            # print(visited_states)

    a = Movement.go_up(copy.deepcopy(node))
    if a is not None:
        update_node_cost(a, algorithm)
        enqueue_node(a)

    a = Movement.go_down(copy.deepcopy(node))
    if a is not None:
        update_node_cost(a, algorithm)
        enqueue_node(a)

    a = Movement.go_left(copy.deepcopy(node))
    if a is not None:
        update_node_cost(a, algorithm)
        enqueue_node(a)

    a = Movement.go_right(copy.deepcopy(node))
    if a is not None:
        update_node_cost(a, algorithm)
        enqueue_node(a)

    nodes.sort(key = lambda a:(a.cost,a.depth))
    print ('\n***Searching at depth', str(nodes[0].depth),'\n')
    display_state(nodes[0])
    return nodes

class Movement():
    def go_up(root: Node):
        i, j = is_possible(root.problem, 0)
        if i != 2:
            root.problem[i][j], root.problem[i+1][j] = root.problem[i+1][j], root.problem[i][j]
            return root
        else:
            return None
        
    def go_down(root: Node):
        i, j = is_possible(root.problem, 0)
        if i != 0:
            root.problem[i][j], root.problem[i-1][j] = root.problem[i-1][j], root.problem[i][j]
            return root
        else:
            return None

    def go_left(root: Node):
        i, j = is_possible(root.problem, 0)
        if j != 2:
            root.problem[i][j], root.problem[i][j+1] = root.problem[i][j+1], root.problem[i][j]
            return root
        else:
            return None

    def go_right(root: Node):
        i, j = is_possible(root.problem, 0)
        if j != 0:
            root.problem[i][j], root.problem[i][j-1] = root.problem[i][j-1], root.problem[i][j]
            return root
        else:
            return None

# checks and returns coordinates if the numbers match with the any state of problem 
def is_possible(problem, value):
    for i in range(len(problem)):
        for j in range(len(problem[i])):
            if problem[i][j] == value:
                return i, j
    return -1, -1 # returns -1 if the problem match fails 

def display_state(node: Node):
    for i in node.problem:
        for j in i:
            if j == 0:
                print('*', end=' ')  
                continue 
            print(j, end=' ')
        print()

def menu():
    test_cases = {
                    '1':[[1,2,3],[4,5,6],[7,8,0]],
                    '2':[[1,2,3],[4,5,6],[0,7,8]],
                    '3':[[1,2,3],[5,0,6],[4,7,8]],
                    '4':[[1,3,6],[5,0,2],[4,7,8]],
                    '5':[[1,3,6],[5,0,7],[4,8,2]],
                    '6':[[1,6,7],[5,0,3],[4,8,2]],
                    '7':[[7,1,2],[4,8,5],[6,3,0]],
                    '8':[[0,7,2],[4,6,1],[3,5,8]]
                }
    option = int(input("Choose an option:\n1. Use Default Puzzle\n2. Enter your own 8-tile Puzzle\nEnter the option: "))
    if option == 1:
        sl_no = input('Enter any puzzle number between 1 and 8 (1 easiest and 8 hardest): ')
        problem = test_cases[sl_no]
        print('You selected this puzzle:')
        for row in problem:
            for number in row:
                if number == 0:
                    print('*', end=' ')
                else:
                    print(number, end=' ')
            print()

    elif option == 2:
        print('Enter your input for 8-tile puzzle:\n(Use 0 for blank space)')
        problem = []
        for _ in range(3):
            row = list(map(int, input().split()))
            problem.append(row)

    print('\n*********\n')
    method = input('Select one of the search methods:\n1. Uniform Cost Search\nInput: ')
    root = Node(problem, 0, 0)
    start = time.time()
    answer = generic_search(root, method)
    end = time.time()
    print('Solved with a depth of ', str(answer.depth))
    print('Algorithm took', str(round((end - start), 3)), 'seconds to complete')

visited_states = []
menu()