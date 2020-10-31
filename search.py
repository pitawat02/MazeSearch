from timeit import default_timer as timer
from collections import OrderedDict

graph = None
frontier = []
visited = OrderedDict()  

def heuristic_search(algorithm, sort_by):

    graph.clear_parents()
    
    # Variables
    goal_state = None
    solution_cost = 0
    solution = []
    node_solution = []
    temp_node = []
    time_start = timer()

    # Lets clear frontier and visited, then add root element to the frontier.
    frontier.clear()
    visited.clear()
    frontier.append(graph.root)

    while len(frontier) > 0:

        # Firstly, we need to sort the frontier according to heuristic...
        sort_frontier(sort_by)

        # We need to remove the correct node from the frontier and add it to the visited.
        current_node = frontier.pop(0)
        visited[current_node] = None


        # Stop GBFS, if we are in a goal state...
        if is_goal(current_node):
            goal_state = current_node
            break

        # Add to frontier as in BFS.
        add_to_frontier(current_node, "BFS")

    # Check if GBFS was successful...
    if goal_state is not None:

        # We need to calculate the cost of the solution AND get the solution itself...
        current = goal_state
        while current is not None:
            solution_cost += current.cost
            solution.insert(0, current)
            # Get the parent node and continue...
            current = current.parent

        for node in solution:
            temp_node.append(node.x)
            temp_node.append(node.y)
            node_solution.append(temp_node)
            temp_node = []
        node_solution.append("/")
    
        for node in visited:
            temp_node.append(node.x)
            temp_node.append(node.y)
            node_solution.append(temp_node)
            temp_node = []


        node_solution.append(solution_cost)
        time_end = timer()
        time_execute = time_end-time_start
        node_solution.append(time_execute)
    
        return node_solution    

    else: print("No goal state found.")

def search_ans(algorithm):
    
    graph.clear_parents()

    pop_index = 0
    goal_state = None
    solution_cost = 0
    solution = []
    expanded_nodes = []
    iteration = -1
    node_solution = []
    temp_node = []
    time_start = timer()
    while goal_state is None and iteration <= graph.maximum_depth:

        iteration += 1
        frontier.clear()
        visited.clear()
        frontier.append(graph.root)
        while len(frontier) > 0:

            if "DFS" in algorithm or "IDS" in algorithm:
                pop_index = len(frontier) - 1

            current_node = frontier.pop(pop_index)
            visited[current_node] = None

            if is_goal(current_node):
                goal_state = current_node
                break

            if "IDS" in algorithm:
                parent = current_node
                for i in range(iteration): #define that how many times node can loopback
                    # If parent is not none, iteration to upper parent.
                    parent = parent if parent is None else parent.parent
                if parent is None:  #ถ้า depth limit เกิน parent จะไม่ None    
                    add_to_frontier(current_node, "DFS")

            # DFS + BFS
            else:
                add_to_frontier(current_node, algorithm)

        
        for node in visited:
            expanded_nodes.append(node)

        if "IDS" not in algorithm:
            break

    if goal_state is None:
        print("No goal state found.")
        return

    current = goal_state
    while current is not None:
        solution_cost += current.cost
        solution.insert(0, current)
        current = current.parent
    
    for node in solution:
        temp_node.append(node.x)
        temp_node.append(node.y)
        node_solution.append(temp_node)
        temp_node = []
    node_solution.append("/")
    
    for node in expanded_nodes:
        temp_node.append(node.x)
        temp_node.append(node.y)
        node_solution.append(temp_node)
        temp_node = []


    node_solution.append(solution_cost)
    time_end = timer()
    time_execute = time_end-time_start
    node_solution.append(time_execute)
    
    return node_solution



def add_to_frontier(current_node, algorithm):
    nodes_to_add = []
    if current_node.east is not None and not is_in_visited(current_node.east):
        nodes_to_add.append(set_parent(current_node, current_node.east, algorithm))
    if current_node.south is not None and not is_in_visited(current_node.south):
        nodes_to_add.append(set_parent(current_node, current_node.south, algorithm))
    if current_node.west is not None and not is_in_visited(current_node.west):
        nodes_to_add.append(set_parent(current_node, current_node.west, algorithm))
    if current_node.north is not None and not is_in_visited(current_node.north):
        nodes_to_add.append(set_parent(current_node, current_node.north, algorithm))

    if "DFS" in algorithm:
        nodes_to_add.reverse()

    for node in nodes_to_add:
        if node.cost is not 0:
            node.cur_cost = node.cost+ node.parent.cur_cost
        else:
            node.cur_cost = 1
        frontier.append(node)

def set_parent(parent_node, child_node, algorithm):
    if "DFS" in algorithm or child_node.parent is None:
        child_node.parent = parent_node
    return child_node


def is_in_visited(node):
    if node in visited:
        return True
    return False


def is_goal(node):
    for goal in graph.maze.goals:
        if goal[0] == node.x and goal[1] == node.y:
            return True
    return False

def return_cost(node):
    return node.cost


def return_heuristic(node):
    return node.heuristic


def return_cost_and_heuristic(node):
    return node.heuristic + node.cur_cost


def sort_frontier(sort_by):
    frontier.sort(key=sort_by)
