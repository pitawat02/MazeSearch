import search
from graph import Graph
import pygame
import time
import random
from pygame.locals import *
import sys
from timeit import default_timer as timer

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

def draw_maze():

    pygame.draw.rect(screen, WHITE, (500, 50, GAMEWINX, GAMEWINY)) #draw outer background
    pygame.draw.rect(screen, BLUE, (500+linewidth/2+start[1]*linesizex, 50+linewidth/2+start[0]*linesizey, linesizex-linewidth/2, linesizey-linewidth/2)) #draw start

    for i in range(len(goals)):
        pygame.draw.rect(screen, YELLOW, (500+linewidth/2+goals[i][1]*linesizex, 50+linewidth/2+goals[i][0]*linesizey, linesizex-linewidth/2, linesizey-linewidth/2)) #draw goals

    for i in range(size[0]):    #draw vertical line
        for j in range(size[1]-1):
            if(wall_vertical[i][j] == 1):
                pygame.draw.line(screen, BLACK, (500+linesizex*(j+1),50+linesizey*i), (500+linesizex*(j+1),50+linesizey*(i+1)),linewidth)
            
    for i in range(size[0]-1):    #draw horizontal line
        for j in range(size[1]):
            if(walls_horizontal[i][j] == 1):
                pygame.draw.line(screen, BLACK, (500+linesizex*(j),50+linesizey*(i+1)), (500+linesizex*(j+1),50+linesizey*(i+1)),linewidth)
    
    
    pygame.draw.rect(screen, BLACK, (500, 50, GAMEWINX, GAMEWINY), 5) #draw outer

def extract(cost): #ดึงค่าใน array
    return cost[0]

def getdata(searchtype,solution,expand,cost,timeExecute): #Function ดึงข้อมูล
    state = 1
    answer = search.dfs_bfs_ids_ucs(searchtype) #ตัวอย่างการดึง array คำตอบมาที่ main เอาไปใช้ map คำตอบ //ถ้าจะไม่เอาคำตอบ DFS ทั้งหมด ไปคอมเม้นที่ไฟล์ search.py 
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
                draw_maze() 
                if WIDTH/10+85 <= mouse[0] <= WIDTH/10 + 185 and 710 <= mouse[1] <= 810: 
                    DFS()  
                elif WIDTH/10+535 <= mouse[0] <= WIDTH/10 + 635 and 710 <= mouse[1] <= 810: 
                    BFS()
                elif WIDTH/10+985 <= mouse[0] <= WIDTH/10 + 1085 and 710 <= mouse[1] <= 810: 
                    IDS() #ของ IDS
                elif 1325 <= mouse[0] <= 1325 + 100 and 35 <= mouse[1] <= 35+50 : 
                    pygame.quit()

def draw_answer(ans, c1, c2, c3):
    way = []
    for i in range(len(ans)-1):
        if ans[i][0] == ans[i+1][0] and ans[i][1] - ans[i+1][1] == 1:
                # print('north')
            way.append('left')
        elif ans[i][0] == ans[i+1][0] and ans[i+1][1] - ans[i][1] == 1:
                # print('south')
            way.append('right')
        elif ans[i][0] - ans[i+1][0] == 1 and ans[i+1][1] == ans[i][1]:
                # print('west')
            way.append('up')
        elif ans[i+1][0] - ans[i][0] == 1 and ans[i+1][1] == ans[i][1]:
                # print('west')
            way.append('down')
    
    for i in range(1,len(ans)-1):
        pygame.draw.rect(screen, (c1 + random.randint(0,255-c1), c2 , c3 ) , (500+linewidth/2+ans[i][1]*linesizex, 50+linewidth/2+ans[i][0]*linesizey, linesizex-linewidth/2, linesizey-linewidth/2))
        pygame.display.update()
            # pygame.display.set_caption(way[i])
        time.sleep(0.0001)
    
def DFS():
    DFS_solution = []
    DFS_expand = []
    DFS_cost = []
    DFS_time = []
    getdata("DFS",DFS_solution,DFS_expand,DFS_cost,DFS_time)
    DFS_cost = extract(DFS_cost)
    DFS_time = extract(DFS_time)

    draw_answer(DFS_expand, 0, 135, 162)
    draw_answer(DFS_solution, 152,251,152)

    print("DFS Example")
    print("Solution : ", DFS_solution) #ปรินต์เส้นทางที่ถูกต้อง
    print("Expanded : ", DFS_expand) #ปรินต์เส้นทางที่ผ่าน
    print("Cost : ", DFS_cost) #ปรินต์คอสที่เก็บไว้
    print("Time : ", DFS_time)

    DFS_text1 = font.render("DFS Summary", True , BLACK)
    DFS_text2 = font.render("Search time : "+ str(round(DFS_time,10)), True , BLACK)
    DFS_text3 = font.render("Cost : "+ str(DFS_cost), True , BLACK)
    DFS_text4 = font.render("Visited Node : "+ str(len(DFS_expand)), True , BLACK)
    screen.blit(DFS_text1,(100,480))
    screen.blit(DFS_text2,(100,550))
    screen.blit(DFS_text3,(100,600))
    screen.blit(DFS_text4,(100,650))

def BFS():
    BFS_solution = []
    BFS_expand = []
    BFS_cost = []
    BFS_time = []
    getdata("BFS",BFS_solution,BFS_expand,BFS_cost,BFS_time)
    BFS_cost = extract(BFS_cost)
    BFS_time = extract(BFS_time)

    draw_answer(BFS_expand, 0, 135, 162)
    draw_answer(BFS_solution, 152,251,152)

    print("BFS Example")
    print("Solution : ", BFS_solution) #ปรินต์เส้นทางที่ถูกต้อง
    print("Expanded : ", BFS_expand) #ปรินต์เส้นทางที่ผ่าน
    print("Cost : ", BFS_cost) #ปรินต์คอสที่เก็บไว้
    print("Time : ", BFS_time)

    BFS_text1 = font.render("BFS Summary", True , BLACK)    
    BFS_text2 = font.render("Search time : "+ str(round(BFS_time,10)), True , BLACK)
    BFS_text3 = font.render("Cost : "+ str(BFS_cost), True , BLACK)
    BFS_text4 = font.render("Visited Node : "+ str(len(BFS_expand)), True , BLACK)
    screen.blit(BFS_text1,(600,480))
    screen.blit(BFS_text2,(600,550))
    screen.blit(BFS_text3,(600,600))
    screen.blit(BFS_text4,(600,650))

    
def IDS():
    IDS_solution = []
    IDS_expand = []
    IDS_cost = []
    IDS_time = []
    getdata("IDS",IDS_solution,IDS_expand,IDS_cost,IDS_time)
    IDS_cost = extract(IDS_cost)
    IDS_time = extract(IDS_time)

    draw_answer(IDS_expand, 0, 135, 162)
    draw_answer(IDS_solution, 152,251,152)

    print("IDS Example")
    print("Solution : ", IDS_solution) #ปรินต์เส้นทางที่ถูกต้อง
    print("Expanded : ", IDS_expand) #ปรินต์เส้นทางที่ผ่าน
    print("Cost : ", IDS_cost) #ปรินต์คอสที่เก็บไว้
    print("Time : ", IDS_time)

    IDS_text1 = font.render("IDS Summary", True , BLACK)    
    IDS_text2 = font.render("Search time : "+ str(round(IDS_time,10)), True , BLACK)
    IDS_text3 = font.render("Cost : "+ str(IDS_cost), True , BLACK)
    IDS_text4 = font.render("Visited Node : "+ str(len(IDS_expand)), True , BLACK)
    screen.blit(IDS_text1,(1100,480))
    screen.blit(IDS_text2,(1100,550))
    screen.blit(IDS_text3,(1100,600))
    screen.blit(IDS_text4,(1100,650))

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
    traps = graph.maze.traps
    start = graph.maze.start
    goals = graph.maze.goals

    search.graph = graph
    draw_maze()
    draw_button()
    # Setting graph we initiated to search class...
    

    #-------------------DFS------------------------
    # DFS_solution = []
    # DFS_expand = []
    # DFS_cost = []
    # DFS_time = []
    # getdata("DFS",DFS_solution,DFS_expand,DFS_cost,DFS_time)
    # DFS_cost = extract(DFS_cost)
    # DFS_time = extract(DFS_time)

    #----------------------------------------------

    # print("DFS Example")
    # print("Solution : ", DFS_solution) #ปรินต์เส้นทางที่ถูกต้อง
    # print("Expanded : ", DFS_expand) #ปรินต์เส้นทางที่ผ่าน
    # print("Cost : ", DFS_cost) #ปรินต์คอสที่เก็บไว้
    # print("Time : ", DFS_time)
    #-------------------BFS------------------------
    # BFS_solution = []
    # BFS_expand = []
    # BFS_cost = []
    # BFS_time = []
    # getdata("BFS",BFS_solution,BFS_expand,BFS_cost,BFS_time)
    # BFS_cost = extract(BFS_cost)
    # BFS_time = extract(BFS_time)
    #----------------------------------------------

    # print("BFS Example")
    # print("Solution : ", BFS_solution) #ปรินต์เส้นทางที่ถูกต้อง
    # print("Expanded : ", BFS_expand) #ปรินต์เส้นทางที่ผ่าน
    # print("Cost : ", BFS_cost) #ปรินต์คอสที่เก็บไว้
    # print("Time : ", BFS_time)
    #-------------------IDS------------------------
    # IDS_solution = []
    # IDS_expand = []
    # IDS_cost = []
    # IDS_time = []
    # getdata("IDS",IDS_solution,IDS_expand,IDS_cost,IDS_time)
    # IDS_cost = extract(IDS_cost)
    # IDS_time = extract(IDS_time)
    # #----------------------------------------------

    # print("IDS Example")
    # print("Solution : ", IDS_solution) #ปรินต์เส้นทางที่ถูกต้อง
    # print("Expanded : ", IDS_expand) #ปรินต์เส้นทางที่ผ่าน
    # print("Cost : ", IDS_cost) #ปรินต์คอสที่เก็บไว้
    # print("Time : ", IDS_time)


    #search.depth_first_search()
    #search.breath_first_search()
    #search.iterative_deepening_search()
    #search.uniform_cost_search()
    #search.greedy_best_first_search()
    #search.a_star_search()

    # font = pygame.font.SysFont("Arial",30)
    # DFS_text = font.render("DFS : "+ str(DFS_time), True , BLACK)
    # BFS_text = font.render("BFS : "+ str(BFS_time), True , BLACK)
    # IDS_text = font.render("IDS  : "+ str(IDS_time), True , BLACK)
    # screen.blit(DFS_text,(50,100))
    # screen.blit(BFS_text,(50,150))
    # screen.blit(IDS_text,(50,200))

    while True:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()    

