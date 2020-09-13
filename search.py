from timeit import default_timer as timer
from collections import OrderedDict

# ############################################## GLOBAL VARIABLES
graph = None
frontier = []
visited = OrderedDict()  

def dfs_bfs_ids_ucs(algorithm):
    
    graph.clear_parents()
    # Variables
    pop_index = 0
    goal_state = None
    solution_cost = 0
    solution = []
    expanded_nodes = []
    iteration = -1
    node_solution = []
    temp_node = []
    time_start = timer()
    # DFS_BFS_IDS
    while goal_state is None and iteration <= graph.maximum_depth:

        # For each iteration, we will increase iteration by one and clear frontier and visited. Also append root node.
        iteration += 1
        frontier.clear()
        visited.clear()
        frontier.append(graph.root)
        while len(frontier) > 0:

            # If DFS or IDS, we will remove last node from the frontier.
            # IF BFS, we will remove the first node from the frontier.
            if "DFS" in algorithm or "IDS" in algorithm:
                pop_index = len(frontier) - 1

            # We need to remove the correct node from the frontier according to the algorithm and add it to the visited.
            current_node = frontier.pop(pop_index)
            visited[current_node] = None
            # Stop DFS_BFS_IDS, if we are in a goal state...
            if is_goal(current_node):
                goal_state = current_node
                break

            # Lets add all child nodes of the current element to the end of the list...
            # If IDS, we need to add child nodes according to the iteration number.
            if "IDS" in algorithm:
                parent = current_node
                for i in range(iteration): #define that how many times node can loopback
                    # If parent is not none, iteration to upper parent.
                    parent = parent if parent is None else parent.parent
                if parent is None:  #ถ้า depth limit เกิน parent จะไม่ None    
                    add_to_frontier(current_node, "DFS")

            # Else, we add all child nodes.
            else:
                add_to_frontier(current_node, algorithm)

        
        # Add all visited nodes to expanded nodes, before clearing it.
        for node in visited:
            expanded_nodes.append(node)

        # We will continue only if this is an IDS search...
        if "IDS" not in algorithm:
            break

    # Check if DFS_BFS_IDS was successful...
    if goal_state is None:
        print("No goal state found.")
        return

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
    # If the child nodes are not None AND if they are not in visited, we will add them to the frontier.
    nodes_to_add = []
    if current_node.east is not None and not is_in_visited(current_node.east):
        nodes_to_add.append(set_parent(current_node, current_node.east, algorithm))
    if current_node.south is not None and not is_in_visited(current_node.south):
        nodes_to_add.append(set_parent(current_node, current_node.south, algorithm))
    if current_node.west is not None and not is_in_visited(current_node.west):
        nodes_to_add.append(set_parent(current_node, current_node.west, algorithm))
    if current_node.north is not None and not is_in_visited(current_node.north):
        nodes_to_add.append(set_parent(current_node, current_node.north, algorithm))

    # For DFS we'll do it in reverse order because we add each node to the end and EAST should be the last node.
    # For BFS we'll do it in correct order.
    if "DFS" in algorithm:
        nodes_to_add.reverse()

    # Then add each node to the frontier.
    for node in nodes_to_add:
        frontier.append(node)


def set_parent(parent_node, child_node, algorithm):
    # We need to set the parent node it is None and if DFS is used.
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
