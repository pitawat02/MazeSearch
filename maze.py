import re
import os
class Maze:

    size = []
    wall_vertical = [[]]
    walls_horizontal = [[]]
    traps = [[]]
    start = []
    goals = []

    def __init__(self):
        self.read_maze()


    def read_maze(self):
        temp = os.path.dirname(os.path.abspath(__file__))+'/map/maze24-2.txt'
        temp = temp.replace("\\","/")
        file = open(temp, "r")
        line = file.readline().rstrip("\n\r")
        empty_line = 0

        while empty_line < 2:
            if not line:
                empty_line += 1
            else:
                empty_line = 0

            if line == "Size":
                first_size = file.readline().rstrip("\n\r")
                second_size = file.readline().rstrip("\n\r")
                self.set_size(first_size, second_size)
            elif line == "Walls":
                walls = []
                line = file.readline().rstrip("\n\r")
                while line:
                    walls.append(line)
                    line = file.readline().rstrip("\n\r")
                self.set_walls(walls)
            elif line == "Traps":
                traps = []
                line = file.readline().rstrip("\n\r")
                while line:
                    traps.append(line)
                    line = file.readline().rstrip("\n\r")
                self.set_traps(traps)
            elif line == "Start":
                start = file.readline().rstrip("\n\r")
                self.set_start(start)
            elif line == "Goals":
                goals = []
                line = file.readline().rstrip("\n\r")
                while line:
                    goals.append(line)
                    line = file.readline().rstrip("\n\r")
                self.set_goals(goals)

            line = file.readline().rstrip("\n\r")

        file.close()

    def set_size(self, x, y):
        if "rows" in x:
            self.size.append(int(re.sub("[^0-9]", "", x)))
        elif "rows" in y:
            self.size.append(int(re.sub("[^0-9]", "", y)))

        if "columns" in x:
            self.size.append(int(re.sub("[^0-9]", "", x)))
        elif "columns" in y:
            self.size.append(int(re.sub("[^0-9]", "", y)))

        self.wall_vertical = [[0 for i in range(self.size[1] - 1)] for i in range(self.size[0])]
        self.walls_horizontal = [[0 for i in range(self.size[1])] for i in range(self.size[0] - 1)]
        self.traps = [[0 for i in range(self.size[1])] for i in range(self.size[0])]

    def set_walls(self, walls):
        walls_length = len(walls)

        for i in range(walls_length):
            if "row" in walls[i]:
                row_index = int(re.sub("[^0-9]", "", walls[i]))
                column_indexes = walls[i+1].split()
                for index in column_indexes:
                    self.wall_vertical[row_index - 1][int(index) - 1] = 1
            elif "column" in walls[i]:
                column_index = int(re.sub("[^0-9]", "", walls[i]))
                row_indexes = walls[i + 1].split()
                for index in row_indexes:
                    self.walls_horizontal[int(index) - 1][column_index - 1] = 1

    def set_traps(self, traps):
        for trap in traps:
            indexes = list(map(int, trap.split()))
            self.traps[indexes[0] - 1][indexes[1] - 1] = 1
    def set_start(self, start):
        indexes = list(map(int, start.split()))
        self.start.append(indexes[0] - 1)
        self.start.append(indexes[1] - 1)
    def set_goals(self, goals):
        for goal in goals:
            indexes = list(map(int, goal.split()))
            indexes = list(map(lambda x: x - 1, indexes))
            self.goals.append(indexes)
    def can_pass(self, row, column, direction):
        if direction == "east":
            if column == (self.size[1] - 1):
                return False
            return self.wall_vertical[row][column] == 0
        elif direction == "south":
            if row == (self.size[0] - 1):
                return False
            return self.walls_horizontal[row][column] == 0
        elif direction == "west":
            if column == 0:
                return False
            return self.wall_vertical[row][column - 1] == 0
        elif direction == "north":
            if row == 0:
                return False
            return self.walls_horizontal[row - 1][column] == 0

