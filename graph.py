import sys
from maze import Maze


class Node:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.cost = 0
        self.parent = None
        self.east = None
        self.south = None
        self.west = None
        self.north = None
        self.heuristic = 0

    def check_equality(self, x, y):
        return x == self.x and y == self.y

    def __str__(self):
        return "[" + str(self.x) + ", " + str(self.y) + "]"


class Graph:

    nodes = [] 
    maze = None
    
    def __init__(self):
        self.maze = Maze()
        self.root = self.create_node(self.maze.start[0], self.maze.start[1])

        # Finding maximum depth.
        self.maximum_depth = self.find_maximum_depth() - 1

        self.root.cost = 0
        
        

    def create_node(self, x, y):
        node = Node()

        node.x = x
        node.y = y

        self.nodes.append(node)
        
        node.cost = 1

        # Set child nodes.
        if self.maze.can_pass(node.x, node.y, "east"):
            node.east = self.node_exists(node.x, node.y + 1)
            if node.east is None:
                node.east = self.create_node(node.x, node.y + 1)
                node.east.parent = node

        if self.maze.can_pass(node.x, node.y, "south"):
            node.south = self.node_exists(node.x + 1, node.y)
            if node.south is None:
                node.south = self.create_node(node.x + 1, node.y)
                node.south.parent = node

        if self.maze.can_pass(node.x, node.y, "west"):
            node.west = self.node_exists(node.x, node.y - 1)
            if node.west is None:
                node.west = self.create_node(node.x, node.y - 1)
                node.west.parent = node

        if self.maze.can_pass(node.x, node.y, "north"):
            node.north = self.node_exists(node.x - 1, node.y)
            if node.north is None:
                node.north = self.create_node(node.x - 1, node.y)
                node.north.parent = node

        return node

    def node_exists(self, x, y):
        for node in self.nodes:
            if node.check_equality(x, y):
                return node
        return None

    def find_maximum_depth(self):
        maximum_depth = 0

        for node in self.nodes:
            current_node = node
            local_depth = 0
            while current_node is not None:
                current_node = current_node.parent
                local_depth += 1

            maximum_depth = max(maximum_depth, local_depth)

        return maximum_depth

    def get_node_cost(self, x, y):
        for node in self.nodes:
            if node.check_equality(x, y):
                return node.cost
        return 0

    def clear_parents(self):
        for node in self.nodes:
            node.parent = None