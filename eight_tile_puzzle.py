import time
import copy

# Our targetted goal state
goal_state= [[1,2,3],[4,5,6],[7,8,0]]

# Represents a node in a search algorithm and stores the problem/puzzle
class Node:
    def __init__(self, problem, depth = 0, cost = 0):
        self.problem = problem # The problem state associated with the node
        self.depth = depth # The depth or level of the node in the search tree. Default is 0
        self.cost = cost # The cost associated with the node. Default is 0


# Generic Search algorithm
def generic_search(root: Node, algorithm):
    nodes = [root] # nodes = MAKE-QUEUE(MAKE-NODE(problem.INITIAL-STATE))
    max_depth = 0 # to track deepest level
    expanded_nodes = 0 # count of nodes that have been expanded or visited
    while nodes:
        node = nodes.pop(0) # popping the first element in the list
        if node.problem == goal_state: # check if at goal state
            print(f'Hooray!!! We solved it!! \nExpanded {expanded_nodes} nodes')
            return node
        nodes = queueing_function(node, nodes, algorithm) # nodes is updated with the newly generated nodes as per chosen search algorithm
        expanded_nodes+=1
        max_depth = max(max_depth, node.depth)
    print('NADA!!')
    return None # return None if no solution



# Calculates the number of misplaced tiles in the given puzzle state compared to the goal state.
def heuristic_misplaced_tile(root: Node):
    misplaced_count = 0
    for i in range(len(root.problem)):
        for j in range(len(root.problem[i])):
            # Check if the tile at position (i, j) is misplaced
            if goal_state[i][j] != root.problem[i][j] and not (i == len(root.problem[i]) - 1 and j == len(root.problem) - 1):
                misplaced_count += 1
    return misplaced_count


# Calculates the Manhattan distance heuristic for the given puzzle state compared to the goal state.
def heuristic_manhattan_distance(root: Node):
    total_distance = 0
    for i in range(len(root.problem)):
        for j in range(len(root.problem[i])):
            if root.problem[i][j] != 0:
                # Find the target position (x, y) of the tile in the goal state
                for x in range(len(goal_state)):
                    if root.problem[i][j] in goal_state[x]:
                        y = goal_state[x].index(root.problem[i][j])
                        break
                # Calculate the Manhattan distance between the current position (i, j) and the target position (x, y)
                total_distance += abs(x - i) + abs(y - j)
    return total_distance



def queueing_function(node, nodes, algorithm):
    global visited_states # to keep track of the visited states 
    a = copy.deepcopy(node) # making a copy of the problem

    # Update the depth and cost of the node a based on the selected algorithm
    def update_node_cost(a, algorithm):
        a.depth = node.depth + 1
        if algorithm == '1':
            a.cost = a.depth
        elif algorithm == '2':
            a.cost = a.depth + heuristic_misplaced_tile(a)
        elif algorithm == '3':
            a.cost = a.depth + heuristic_manhattan_distance(a)
    
    # Enqueue the node a into the list of nodes if it has not been visited before
    def enqueue_node(a):
        if [a.cost, a.problem] not in visited_states:
            nodes.append(a)
            visited_states.append([a.cost, a.problem])

    
    # Generate successor nodes by applying the up, down, left, and right operators 
    # to the current node node.
    # If a successor node is valid (not None), update its cost based on the selected algorithm 
    # and enqueue it into the list of nodes.

    a = Operators.go_up(copy.deepcopy(node))
    if a is not None:
        update_node_cost(a, algorithm)
        enqueue_node(a)

    a = Operators.go_down(copy.deepcopy(node))
    if a is not None:
        update_node_cost(a, algorithm)
        enqueue_node(a)

    a = Operators.go_left(copy.deepcopy(node))
    if a is not None:
        update_node_cost(a, algorithm)
        enqueue_node(a)

    a = Operators.go_right(copy.deepcopy(node))
    if a is not None:
        update_node_cost(a, algorithm)
        enqueue_node(a)

    nodes.sort(key = lambda a:(a.cost,a.depth)) # Sort the list of nodes based on their cost and depth
    print ('\n***Expanding at depth', str(nodes[0].depth),'\n') # Depth of the node with the lowest cost
    display_state(nodes[0])
    return nodes



# Methods for moving the blank space (0) in different directions,
# swaps the blank space with the adjacent number in the specified direction 
# and returns the updated node. Else, return None indicating 
# that the move is not possible in that direction.

class Operators():
    def swap_elements(problem, i1, j1, i2, j2):
        problem[i1][j1], problem[i2][j2] = problem[i2][j2], problem[i1][j1]

    def go_up(root: Node):
        i, j = is_possible(root.problem, 0)
        if i != 2:
            Operators.swap_elements(root.problem, i, j, i+1, j)
            return root
        else:
            return None

    def go_down(root: Node):
        i, j = is_possible(root.problem, 0)
        if i != 0:
            Operators.swap_elements(root.problem, i, j, i-1, j)
            return root
        else:
            return None

    def go_left(root: Node):
        i, j = is_possible(root.problem, 0)
        if j != 2:
            Operators.swap_elements(root.problem, i, j, i, j+1)
            return root
        else:
            return None

    def go_right(root: Node):
        i, j = is_possible(root.problem, 0)
        if j != 0:
            Operators.swap_elements(root.problem, i, j, i, j-1)
            return root
        else:
            return None



# checks if a given value is present in a 2D problem array and 
# returns its coordinates (row, column) if found
def is_possible(problem, value):
    for i in range(len(problem)):
        for j in range(len(problem[i])):
            if problem[i][j] == value:
                return i, j
    return -1, -1 # returns -1 if the problem match fails 

# Display the state of a node by printing its problem array
def display_state(node: Node):
    for i in node.problem:
        for j in i:
            if j == 0:
                print('*', end=' ')  
                continue 
            print(j, end=' ')
        print()


# A menu to the user for selecting options related to the 8-tile puzzle
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
        if sl_no < '1' or sl_no > '8':
            print("\n***Enter a valid puzzle number***\n")
            print("Run the program again!\n")
            exit()
        else:
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
        print('Enter your input for 8-tile puzzle:\n(Use 0 for blank tile)')
        problem = []
        for _ in range(3): # this is for 3x3 puzzle (8 tile), change from 3 to 4 or 5 for a 15 or 25 tile puzzle respectively
            row = list(map(int, input().split()))
            problem.append(row)
    
    else:
        print("\n***Invalid input***\n")
        print("Run the program again!\n")
        exit()

    print('\n*********\n')
    method = input('Select one of the search methods:\n1. Uniform Cost Search\n2. A* with the misplaced tile heuristic\n3. A* with the Manhattan Distance heuristic\nEnter the search algorithm number: ')
    root = Node(problem, 0, 0)
    if '1' <= method <= '3':
        start = time.time()
        answer = generic_search(root, method)
        end = time.time()
        print('Solved with a depth of', str(answer.depth))
        print('Algorithm took', str(round((end - start), 3)), 'seconds to complete')
    else:
        print("\n***Oops!! Invalid algorithm chosen!!***\n")
        print("Run the program again!\n")

visited_states = []
menu()