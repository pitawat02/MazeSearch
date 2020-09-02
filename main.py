import search
from graph import Graph
import pygame
import time
import random
from pygame.locals import *
import sys

# set up pygame window
WIDTH = 1600
HEIGHT = 900
FPS = 30
GAMEWIN = 600

# Define colours
WHITE = (255, 255, 255)
GREEN = (0, 255, 0,)
BLUE = (0, 0, 255)
YELLOW = (255 ,255 ,0)
GREY = (181,181,181)
BLACK = (0,0,0)

# initalize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(GREY)
pygame.display.set_caption("Maze")
FramePerSec = pygame.time.Clock()


def draw_maze():
    pygame.draw.rect(screen, BLUE, (500+linewidth/2+start[1]*linesizex, 50+linewidth/2+start[0]*linesizey, linesizex-linewidth/2, linesizey-linewidth/2)) #draw start

    for i in range(len(goals)):
        pygame.draw.rect(screen, YELLOW, (500+linewidth/2+goals[i][1]*linesizex, 50+linewidth/2+goals[i][0]*linesizey, linesizex-linewidth/2, linesizey-linewidth/2)) #draw start

    for i in range(size[0]):    #draw vertical line
        for j in range(size[1]-1):
            if(wall_vertical[i][j] == 1):
                pygame.draw.line(screen, BLACK, (500+linesizex*(j+1),50+linesizey*i), (500+linesizex*(j+1),50+linesizey*(i+1)),linewidth)
            
    for i in range(size[0]-1):    #draw horizontal line
        for j in range(size[1]):
            if(walls_horizontal[i][j] == 1):
                pygame.draw.line(screen, BLACK, (500+linesizex*(j),50+linesizey*(i+1)), (500+linesizex*(j+1),50+linesizey*(i+1)),linewidth)

    pygame.draw.rect(screen, BLACK, (500, 50, GAMEWIN, GAMEWIN), 5) #draw outer

if __name__ == "__main__":
    graph = Graph()

    size = graph.maze.size

    #initialize
    linesizex = int(600/size[0])
    linesizey = int(600/size[1])
    linewidth = int(40/size[0])
    wall_vertical = graph.maze.wall_vertical
    walls_horizontal = graph.maze.walls_horizontal
    traps = graph.maze.traps
    start = graph.maze.start
    goals = graph.maze.goals

    draw_maze()

        
    # Setting graph we initiated to search class...
    search.graph = graph
    state = 1
    DFS_solution = []
    DFS_expand = []
    DFS_answer = search.dfs_bfs_ids_ucs("DFS") #ตัวอย่างการดึง array คำตอบมาที่ main เอาไปใช้ map คำตอบ //ถ้าจะไม่เอาคำตอบ DFS ทั้งหมด ไปคอมเม้นที่ไฟล์ search.py 
    solution_cost = DFS_answer.pop() #ดึงตัวท้ายที่เป็น Cost 
    for i in range(len(DFS_answer)): #แยก expand กับ solution
        if state == 1:
            if DFS_answer[i] is '/':
                state = 0
            else:
                DFS_solution.append(DFS_answer[i])
        elif state == 0:
            DFS_expand.append(DFS_answer[i])

    print(DFS_solution) #ปรินต์เส้นทางที่ถูกต้อง
    print(DFS_expand) #ปรินต์เส้นทางที่ผ่าน
    print(solution_cost) #ปรินต์คอสที่เก็บไว้

    search.depth_first_search()
    search.breath_first_search()
    search.iterative_deepening_search()
    #search.uniform_cost_search()
    #search.greedy_best_first_search()
    #search.a_star_search()
    
    

    while True:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()    

