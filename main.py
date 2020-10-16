import search
from graph import Graph
import pygame
import time
import random
from pygame.locals import *
import sys
from timeit import default_timer as timer
import tracemalloc

# set up pygame window
WIDTH = 1500
HEIGHT = 800
FPS = 30
GAMEWINY = 400
GAMEWINX = 400

# Define colours
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255 ,255 ,0)
GREY = (181,181,181)
GREY2 = (70,70,70)
BLACK = (0,0,0)
LIGHTBLUE = (100,149,237)
LIGHTGREEN = (152,251,152)


# initalize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(GREY)
pygame.display.set_caption("Maze")
FramePerSec = pygame.time.Clock()

smallfont = pygame.font.SysFont('Aerial',35)
font = pygame.font.SysFont("Arial",30)
DFS_butt = smallfont.render('DFS' , True , BLACK)
BFS_butt = smallfont.render('BFS' , True , BLACK)
IDS_butt = smallfont.render('IDS' , True , BLACK)
end_butt = smallfont.render('END' , True , BLACK)
strap = []

def draw_maze():

    pygame.draw.rect(screen, WHITE, (500, 50, GAMEWINX, GAMEWINY)) #draw outer background
    pygame.draw.rect(screen, BLUE, (500+linewidth/2+start[1]*linesizex, 50+linewidth/2+start[0]*linesizey, linesizex-linewidth/2, linesizey-linewidth/2)) #draw start

    for i in range(len(goals)):
        pygame.draw.rect(screen, YELLOW, (500+linewidth/2+goals[i][1]*linesizex, 50+linewidth/2+goals[i][0]*linesizey, linesizex-linewidth/2, linesizey-linewidth/2)) #draw goals

    for i in range(len(traps)):
        for j in range(len(traps)):
            if traps[i][j] == 1:
                pygame.draw.rect(screen, BLACK, (500+linewidth/2+j*linesizex, 50+linewidth/2+i*linesizey, linesizex-linewidth/2, linesizey-linewidth/2)) #draw traps
                strap.append([i,j])

    for i in range(size[0]):    #draw vertical line
        for j in range(size[1]-1):
            if(wall_vertical[i][j] == 1):
                pygame.draw.line(screen, BLACK, (500+linesizex*(j+1),50+linesizey*i), (500+linesizex*(j+1),50+linesizey*(i+1)),linewidth+1)
            
    for i in range(size[0]-1):    #draw horizontal line
        for j in range(size[1]):
            if(walls_horizontal[i][j] == 1):
                pygame.draw.line(screen, BLACK, (500+linesizex*(j),50+linesizey*(i+1)), (500+linesizex*(j+1),50+linesizey*(i+1)),linewidth+1)
    
    
    pygame.draw.rect(screen, BLACK, (500, 50, GAMEWINX, GAMEWINY), 5) #draw outer

def extract(cost): #ดึงค่าใน array
    return cost[0]

def getdata(searchtype,solution,expand,cost,timeExecute): #Function ดึงข้อมูล
    if "DFS" in searchtype or "IDS" in searchtype or "BFS" in searchtype:
        state = 1
        answer = []
        answer = search.search_ans(searchtype) 
        timeExecute.append(answer.pop())
        cost.append(answer.pop()) #ดึงตัวท้ายที่เป็น Cost 
        for i in range(len(answer)): #แยก expand กับ solution
            if state == 1:
                if answer[i] is '/':
                    state = 0
                else:
                    solution.append(answer[i])
            elif state == 0:
                expand.append(answer[i])
    elif "a_star" in searchtype:
        state = 1
        answer = []
        answer = search.heuristic_search("A Star Search(A*):", search.return_cost_and_heuristic)
        timeExecute.append(answer.pop())
        cost.append(answer.pop()) #ดึงตัวท้ายที่เป็น Cost 
        for i in range(len(answer)): #แยก expand กับ solution
            if state == 1:
                if answer[i] is '/':
                    state = 0
                else:
                    solution.append(answer[i])
            elif state == 0:
                expand.append(answer[i])
                
    elif "greedy" in searchtype:
        state = 1
        answer = []
        answer = search.heuristic_search("Greedy Best First Search(GBFS):", search.return_heuristic) 
        timeExecute.append(answer.pop())
        cost.append(answer.pop()) #ดึงตัวท้ายที่เป็น Cost 
        for i in range(len(answer)): #แยก expand กับ solution
            if state == 1:
                if answer[i] is '/':
                    state = 0
                else:
                    solution.append(answer[i])
            elif state == 0:
                expand.append(answer[i])        

def draw_button():
    
    while True: 
        mouse = pygame.mouse.get_pos() 
        pygame.draw.rect(screen,(0,0,240),(WIDTH/10+85,710,100,50))
        pygame.draw.rect(screen,YELLOW,(WIDTH/10+535,710,100,50))
        pygame.draw.rect(screen,GREEN,(WIDTH/10+985,710,100,50)) 
        pygame.draw.rect(screen,(244,0,0),(1325,35,100,50)) 
    
        screen.blit(DFS_butt , (WIDTH/10 + 100 ,720)) 
        screen.blit(BFS_butt , (WIDTH/10 + 550 ,720))
        screen.blit(IDS_butt , (WIDTH/10 + 1000 ,720))
        screen.blit(end_butt , (WIDTH/10 + 1200 ,50))

        pygame.display.update()

        for ev in pygame.event.get(): 
            if ev.type == pygame.QUIT: 
                pygame.quit()   
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                
                if WIDTH/10+85 <= mouse[0] <= WIDTH/10 + 185 and 710 <= mouse[1] <= 810: 
                    pygame.draw.rect(screen,GREY,(100,450,400,250)) 
                    draw_maze() 
                    DFS()  
                elif WIDTH/10+535 <= mouse[0] <= WIDTH/10 + 635 and 710 <= mouse[1] <= 810: 
                    pygame.draw.rect(screen,GREY,(600,450,400,250)) 
                    draw_maze() 
                    BFS()
                elif WIDTH/10+985 <= mouse[0] <= WIDTH/10 + 1085 and 710 <= mouse[1] <= 810: 
                    pygame.draw.rect(screen,GREY,(1100,450,400,250)) 
                    draw_maze() 
                    IDS()
                elif 1325 <= mouse[0] <= 1325 + 100 and 35 <= mouse[1] <= 35+50 : 
                    pygame.quit()

def draw_expand(ans, c1, c2, c3):
    way = []
    for i in range(len(ans)-1):
        if ans[i][0] == ans[i+1][0] and ans[i][1] - ans[i+1][1] == 1:
            way.append('left')
        elif ans[i][0] == ans[i+1][0] and ans[i+1][1] - ans[i][1] == 1:
            way.append('right')
        elif ans[i][0] - ans[i+1][0] == 1 and ans[i+1][1] == ans[i][1]:
            way.append('up')
        elif ans[i+1][0] - ans[i][0] == 1 and ans[i+1][1] == ans[i][1]:
            way.append('down')
    
    for i in range(1,len(ans)-1):
        pygame.draw.rect(screen, (c1 + random.randint(0,255-c1), c2 , c3 ) , (500+linewidth/2+ans[i][1]*linesizex + 2, 50+linewidth/2+ans[i][0]*linesizey+2, linesizex-linewidth/2-2, linesizey-linewidth/2-2))
        pygame.display.update()
        time.sleep(0.001)

def draw_answer(ans, c1, c2, c3):
    way = []
    for i in range(len(ans)-1):
        if ans[i][0] == ans[i+1][0] and ans[i][1] - ans[i+1][1] == 1:
            way.append('left')
        elif ans[i][0] == ans[i+1][0] and ans[i+1][1] - ans[i][1] == 1:
            way.append('right')
        elif ans[i][0] - ans[i+1][0] == 1 and ans[i+1][1] == ans[i][1]:
            way.append('up')
        elif ans[i+1][0] - ans[i][0] == 1 and ans[i+1][1] == ans[i][1]:
            way.append('down')
    
    for i in range(1,len(ans)-1):
        if ans[i] in strap:
            pygame.draw.rect(screen, GREY2 , (500+linewidth/2+ans[i][1]*linesizex + 2, 50+linewidth/2+ans[i][0]*linesizey+2, linesizex-linewidth/2-2, linesizey-linewidth/2-2))
        else:
            pygame.draw.rect(screen, (c1 + random.randint(0,255-c1), c2 , c3 ) , (500+linewidth/2+ans[i][1]*linesizex + 2, 50+linewidth/2+ans[i][0]*linesizey+2, linesizex-linewidth/2-2, linesizey-linewidth/2-2))
        pygame.display.update()
        time.sleep(0.001)
    
def DFS():
    DFS_solution = []
    DFS_expand = []
    DFS_cost = []
    DFS_time = []
    tracemalloc.start()
    getdata("a_star",DFS_solution,DFS_expand,DFS_cost,DFS_time)
    current, peak = tracemalloc.get_traced_memory()
    DFS_peak = peak / 10**3
    tracemalloc.stop()
    DFS_cost = extract(DFS_cost)
    DFS_time = extract(DFS_time)

    draw_expand(DFS_expand, 0, 135, 162)
    draw_answer(DFS_solution, 152,251,152)

    DFS_text1 = font.render("DFS Summary", True , BLACK)
    DFS_text2 = font.render("Search time : "+ str(round(DFS_time*1000,5))+" ms", True , BLACK)
    DFS_text3 = font.render("Solution Path Cost : "+ str(DFS_cost), True , BLACK)
    DFS_text4 = font.render("Visited Node : "+ str(len(DFS_expand)), True , BLACK)
    DFS_text5 = font.render("Peak memory : "+ str(DFS_peak)+" kB", True , BLACK)
    screen.blit(DFS_text1,(100,450))
    screen.blit(DFS_text2,(100,510))
    screen.blit(DFS_text3,(100,560))
    screen.blit(DFS_text4,(100,610))
    screen.blit(DFS_text5,(100,660))

def BFS():
    BFS_solution = []
    BFS_expand = []
    BFS_cost = []
    BFS_time = []
    tracemalloc.start()
    getdata("BFS",BFS_solution,BFS_expand,BFS_cost,BFS_time)
    current, peak = tracemalloc.get_traced_memory()
    BFS_peak = peak / 10**3
    tracemalloc.stop()
    BFS_cost = extract(BFS_cost)
    BFS_time = extract(BFS_time)

    draw_expand(BFS_expand, 0, 135, 162)
    draw_answer(BFS_solution, 152,251,152)

    BFS_text1 = font.render("BFS Summary", True , BLACK)    
    BFS_text2 = font.render("Search time : "+ str(round(BFS_time*1000,5))+" ms", True , BLACK)
    BFS_text3 = font.render("Solution Path Cost : "+ str(BFS_cost), True , BLACK)
    BFS_text4 = font.render("Visited Node : "+ str(len(BFS_expand)), True , BLACK)
    BFS_text5 = font.render("Peak memory : "+ str(BFS_peak)+" kB", True , BLACK)
    screen.blit(BFS_text1,(600,450))
    screen.blit(BFS_text2,(600,510))
    screen.blit(BFS_text3,(600,560))
    screen.blit(BFS_text4,(600,610))
    screen.blit(BFS_text5,(600,660))
    
def IDS():
    IDS_solution = []
    IDS_expand = []
    IDS_cost = []
    IDS_time = []
    tracemalloc.start()
    getdata("IDS",IDS_solution,IDS_expand,IDS_cost,IDS_time)
    current, peak = tracemalloc.get_traced_memory()
    IDS_peak = peak / 10**3
    tracemalloc.stop()
    IDS_cost = extract(IDS_cost)
    IDS_time = extract(IDS_time)

    draw_expand(IDS_expand, 0, 135, 162)
    draw_answer(IDS_solution, 152,251,152)

    IDS_text1 = font.render("IDS Summary", True , BLACK)    
    IDS_text2 = font.render("Search time : "+ str(round(IDS_time*1000,5))+" ms", True , BLACK)
    IDS_text3 = font.render("Solution Path Cost : "+ str(IDS_cost), True , BLACK)
    IDS_text4 = font.render("Visited Node : "+ str(len(IDS_expand)), True , BLACK)
    IDS_text5 = font.render("Peak memory : "+ str(IDS_peak)+" kB", True , BLACK)
    screen.blit(IDS_text1,(1100,450))
    screen.blit(IDS_text2,(1100,510))
    screen.blit(IDS_text3,(1100,560))
    screen.blit(IDS_text4,(1100,610))
    screen.blit(IDS_text5,(1100,660))

if __name__ == "__main__":
    graph = Graph()

    size = graph.maze.size

    #initialize
    linesizex = int(GAMEWINX/size[1])
    linesizey = int(GAMEWINY/size[0])
    linewidth = int(40/size[0])
    GAMEWINX = linesizex*size[1]
    GAMEWINY = linesizey*size[0]

    wall_vertical = graph.maze.wall_vertical
    walls_horizontal = graph.maze.walls_horizontal
    start = graph.maze.start
    goals = graph.maze.goals
    traps = graph.maze.traps

    search.graph = graph
    
    draw_maze()
    draw_button()

    while True:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()    

