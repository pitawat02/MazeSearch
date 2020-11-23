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

buttfont = pygame.font.SysFont('Aerial',22)
font = pygame.font.SysFont("Arial",20)
DFS_butt = buttfont.render('DFS' , True , BLACK)
BFS_butt = buttfont.render('BFS' , True , BLACK)
IDS_butt = buttfont.render('IDS' , True , BLACK)
ASTAR_butt = buttfont.render('ASTAR' , True , BLACK)
GREEDY_butt = buttfont.render('GREEDY' , True , BLACK)
end_butt = buttfont.render('END' , True , BLACK)
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
        pygame.draw.rect(screen,LIGHTBLUE,(WIDTH/10,710,100,50))
        pygame.draw.rect(screen,YELLOW,(WIDTH/10+250,710,100,50))
        pygame.draw.rect(screen,GREEN,(WIDTH/10+500,710,100,50)) 
        pygame.draw.rect(screen,WHITE,(WIDTH/10+800,710,100,50))
        pygame.draw.rect(screen,WHITE,(WIDTH/10+1050,710,100,50))
        pygame.draw.rect(screen,(244,0,0),(1325,35,100,50)) 
    
        screen.blit(DFS_butt , (WIDTH/10 + 30 ,730))
        screen.blit(BFS_butt , (WIDTH/10 + 280 ,730))
        screen.blit(IDS_butt , (WIDTH/10 + 530 ,730))
        screen.blit(ASTAR_butt , (WIDTH/10 + 820 ,730))
        screen.blit(GREEDY_butt , (WIDTH/10 + 1070 ,730))

        screen.blit(end_butt , (WIDTH/10 + 1200 ,50))

        pygame.display.update()

        for ev in pygame.event.get(): 
            if ev.type == pygame.QUIT: 
                pygame.quit()   
            elif ev.type == pygame.MOUSEBUTTONDOWN: #กดปุ่ม+ตำแหน่ง
                
                if WIDTH/10 <= mouse[0] <= WIDTH/10 + 100 and 710 <= mouse[1] <= 810: 
                    pygame.draw.rect(screen,GREY,(100,450,200,250))
                    draw_maze() 
                    DFS()  
                elif WIDTH/10+250 <= mouse[0] <= WIDTH/10 + 350 and 710 <= mouse[1] <= 810: 
                    pygame.draw.rect(screen,GREY,(350,450,200,250))
                    draw_maze() 
                    BFS()
                elif WIDTH/10+500 <= mouse[0] <= WIDTH/10 + 600 and 710 <= mouse[1] <= 810: 
                    pygame.draw.rect(screen,GREY,(600,450,200,250))
                    draw_maze() 
                    IDS()
                elif WIDTH/10+800 <= mouse[0] <= WIDTH/10 + 900 and 710 <= mouse[1] <= 810: 
                    pygame.draw.rect(screen,GREY,(900,450,200,250))
                    draw_maze() 
                    ASTAR()
                elif WIDTH/10+1050 <= mouse[0] <= WIDTH/10 + 1150 and 710 <= mouse[1] <= 810: 
                    pygame.draw.rect(screen,GREY,(1150,450,200,250))
                    draw_maze() 
                    GREEDY()
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
    getdata("DFS",DFS_solution,DFS_expand,DFS_cost,DFS_time)
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
    screen.blit(DFS_text1,(120,450))
    screen.blit(DFS_text2,(100,500))
    screen.blit(DFS_text3,(100,530))
    screen.blit(DFS_text4,(100,560))
    screen.blit(DFS_text5,(100,590))

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
    screen.blit(BFS_text1,(370,450))
    screen.blit(BFS_text2,(350,500))
    screen.blit(BFS_text3,(350,530))
    screen.blit(BFS_text4,(350,560))
    screen.blit(BFS_text5,(350,590))
    
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
    screen.blit(IDS_text1,(620,450))
    screen.blit(IDS_text2,(600,500))
    screen.blit(IDS_text3,(600,530))
    screen.blit(IDS_text4,(600,560))
    screen.blit(IDS_text5,(600,590))

def ASTAR():
    ASTAR_solution = []
    ASTAR_expand = []
    ASTAR_cost = []
    ASTAR_time = []
    tracemalloc.start()
    getdata("a_star",ASTAR_solution,ASTAR_expand,ASTAR_cost,ASTAR_time)
    current, peak = tracemalloc.get_traced_memory()
    ASTAR_peak = peak / 10**3
    tracemalloc.stop()
    ASTAR_cost = extract(ASTAR_cost)
    ASTAR_time = extract(ASTAR_time)

    draw_expand(ASTAR_expand, 0, 135, 162)
    draw_answer(ASTAR_solution, 152,251,152)

    ASTAR_text1 = font.render("ASTAR Summary", True , BLACK)
    ASTAR_text2 = font.render("Search time : "+ str(round(ASTAR_time*1000,5))+" ms", True , BLACK)
    ASTAR_text3 = font.render("Solution Path Cost : "+ str(ASTAR_cost), True , BLACK)
    ASTAR_text4 = font.render("Visited Node : "+ str(len(ASTAR_expand)), True , BLACK)
    ASTAR_text5 = font.render("Peak memory : "+ str(ASTAR_peak)+" kB", True , BLACK)
    screen.blit(ASTAR_text1,(920,450))
    screen.blit(ASTAR_text2,(900,500))
    screen.blit(ASTAR_text3,(900,530))
    screen.blit(ASTAR_text4,(900,560))
    screen.blit(ASTAR_text5,(900,590))

def GREEDY():
    GREEDY_solution = []
    GREEDY_expand = []
    GREEDY_cost = []
    GREEDY_time = []
    tracemalloc.start()
    getdata("greedy",GREEDY_solution,GREEDY_expand,GREEDY_cost,GREEDY_time)
    current, peak = tracemalloc.get_traced_memory()
    GREEDY_peak = peak / 10**3
    tracemalloc.stop()
    GREEDY_cost = extract(GREEDY_cost)
    GREEDY_time = extract(GREEDY_time)

    draw_expand(GREEDY_expand, 0, 135, 162)
    draw_answer(GREEDY_solution, 152,251,152)

    GREEDY_text1 = font.render("GREEDY Summary", True , BLACK)
    GREEDY_text2 = font.render("Search time : "+ str(round(GREEDY_time*1000,5))+" ms", True , BLACK)
    GREEDY_text3 = font.render("Solution Path Cost : "+ str(GREEDY_cost), True , BLACK)
    GREEDY_text4 = font.render("Visited Node : "+ str(len(GREEDY_expand)), True , BLACK)
    GREEDY_text5 = font.render("Peak memory : "+ str(GREEDY_peak)+" kB", True , BLACK)
    screen.blit(GREEDY_text1,(1170,450))
    screen.blit(GREEDY_text2,(1150,500))
    screen.blit(GREEDY_text3,(1150,530))
    screen.blit(GREEDY_text4,(1150,560))
    screen.blit(GREEDY_text5,(1150,590))

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

