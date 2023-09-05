import numpy as np
import pygame

from numpy import cos, sin
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT



# CONSTANTS -------------------------------------------------------------------
WIDTH, HEIGHT = 1280, 720
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
COLORS = [(43, 120, 42), (56, 89, 144), (144, 56, 130)]


DDL = 100

g = 9.81
IPS = 60
spend = 1
p = 1
SPEED = .5
t = SPEED / (IPS * p)
time = 0

SCALE = 100

class Pendule:
    def __init__(self, t1=0, t2=0, t3=0, t4=0):
        super(Pendule, self).__init__()
        
        self.l = .1
        self.m = 1
        
        self.theta = np.ones(DDL) * np.radians(-4)


        self.wp = np.zeros(DDL)
        self.w = np.ones(DDL) * 0
        self.pos = np.zeros((DDL+1, 2))
        self.pos[0,0], self.pos[0,1] = [WIDTH / 2, HEIGHT / 10]
        
        self.pos3 = []
        self.T = []
        self.V = []
        self.Em = []
        
    
    def update(self, n):
        for i in range(n):

            A = np.zeros((DDL, DDL))
            
            for i in range(DDL):
                A += np.diag(np.arange(DDL-i, 0, -1), i)
                A += np.diag(np.arange(DDL-i, 0, -1), -i) if i >0 else 0
            
            B = -g / self.l * np.arange(1, DDL+1) * self.theta
            
            self.wp = np.linalg.solve(A, B)
            self.w += self.wp * t
            self.theta += self.w * t
        
        # print(self.theta.shape)
        for i in range(DDL):
            self.pos[i+1,0], self.pos[i+1,1] = self.pos[i,0] + self.l*SCALE * sin(self.theta[i]), self.pos[i,1] + self.l*SCALE * cos(self.theta[i])

        
        if t != 0:
            self.pos3.append((self.pos[-1][0], self.pos[-1][1]))
    
    
            
    
    def draw_lines(self, color):
        
        color1, color2, color3 = color
        if min(color1, color2, color3) < 20:
            if min(color1, color2, color3) < 10:
                color_back = color
            else:
                color_back = (color1-10, color2-10, color3-10)
        else:
            color_back = (color1-20, color2-20, color3-20)
        
        if len(self.pos3) > 2:
            if len(self.pos3) >= int(IPS * spend / SPEED):
                pygame.draw.lines(screen, (color1/2, color2/2, color3/2), False, self.pos3[-int(IPS*spend/SPEED):-1])
            else:
                pygame.draw.lines(screen, (color1/2, color2/2, color3/2), False, self.pos3)
    
    
    
    def draw_pend(self, color):
        corde = []
        for i in range(DDL+1):
            position = (self.pos[i][0], self.pos[i][1])
            pygame.draw.circle(screen, color, position, 4)
            corde.append(position)
        

        # pygame.draw.lines(screen, color, False, corde, width=3)
            
        
            

    
        
        
 
# ---------------GAME----------------------

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pendule double')


pendule1 = Pendule(10, 10, 10, 10)

pendules = [pendule1]


FONT = pygame.font.Font(None, 20)


FPS = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                t = SPEED / (IPS * p) if t == 0 else 0
                print("PAUSE") if t == 0 else print("RESUME")

    
    screen.fill(BLACK)
    time += p*t
    
    
    for i in range(len(pendules)):
        pendules[i].update(p)
        pendules[i].draw_lines(COLORS[i])
    
    for i in range(len(pendules)):
        pendules[i].draw_pend(COLORS[0])
    
    pygame.draw.circle(screen, WHITE, (WIDTH/2, HEIGHT/10), 7)
    screen.blit(FONT.render(f"Time : {round(time, 3):.3f}", True, WHITE), (10, 5))
    screen.blit(FONT.render("Press <Escape> to Pause/Resume", True, WHITE), (10, HEIGHT-20))
    pygame.display.flip()
    
    FPS.tick(IPS)
    
pygame.quit()


# graph(pendule1)