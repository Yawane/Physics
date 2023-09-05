import numpy as np
import pygame
import matplotlib.pyplot as plt

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

ARCENCIEL = []

for i in range(255):
    ARCENCIEL.append((255, i, 0))

for i in range(255):
    ARCENCIEL.append((255-i-1, 255, 0))

for i in range(255):
    ARCENCIEL.append((0, 255, i))

for i in range(255):
    ARCENCIEL.append((0, 255-i-1, 255))


for i in range(255):
    ARCENCIEL.append((i, 0, 255))
    
    
for i in range(255):
    ARCENCIEL.append((255, 0, 255-i-1))





g = 9.81
IPS = 60
spend = .5
p = 1
SPEED = 1
t = SPEED / (IPS * p)
time = 0

SCALE = 140

class Pendule:
    def __init__(self, t1=0, t2=0):
        super(Pendule, self).__init__()
        
        self.l = 1
        self.m = 1
        
        self.x0, self.y0 = WIDTH/2, HEIGHT / 2
        self.theta1, self.theta2 = np.radians(t1), np.radians(t2)

        self.wp1, self.wp2 = 0, 0
        self.w1, self.w2 = 0, 0


        self.x1, self.y1 = self.x0 + self.l*SCALE * sin(self.theta1), self.y0 + self.l*SCALE * cos(self.theta1)
        self.x2, self.y2 = self.x1 + self.l*SCALE * sin(self.theta2), self.y1 + self.l*SCALE * cos(self.theta2)
        
        self.pos2 = []
        self.T = []
        self.V = []
        self.Em = []
        
    
    def update(self, n):
        for i in range(n):
            delta = self.theta1 - self.theta2
            deltap = self.w1 - self.w2
            self.wp1 = (-cos(delta) * (self.w1*sin(delta)*(deltap + self.w2) - g/self.l*sin(self.theta2)) + self.w2*deltap*sin(delta) - self.w1*self.w2*sin(delta) - 2*g/self.l*sin(self.theta1)) / (2 - cos(delta)**2)
            self.wp2 = -self.wp1*cos(delta) + self.w1 ** 2 * sin(delta) - g / self.l * sin(self.theta2)
            
            self.w1 += (self.wp1 * t)
            self.w2 += (self.wp2 * t)
            
            self.theta1 += (self.w1 * t)
            self.theta2 += (self.w2 * t)
        
        # print(self.theta.shape)
        self.x1, self.y1 = self.x0 + self.l*SCALE * sin(self.theta1), self.y0 + self.l*SCALE * cos(self.theta1)
        self.x2, self.y2 = self.x1 + self.l*SCALE * sin(self.theta2), self.y1 + self.l*SCALE * cos(self.theta2)
        
        if t != 0:
            self.pos2.append((self.x2, self.y2))
            self.T.append(self.m * self.l ** 2 * (self.w1**2 + .5 * self.w2**2 + self.w1 * self.w2 * cos(delta)))
            self.V.append(-self.m * self.l * g * (2*cos(self.theta1) + cos(self.theta2)))
            self.Em.append(self.T[-1] + self.V[-1])
    
    
            
    
    def draw_lines(self, color):
        
        color1, color2, color3 = color
        if min(color1, color2, color3) < 20:
            if min(color1, color2, color3) < 10:
                color_back = color
            else:
                color_back = (color1-10, color2-10, color3-10)
        else:
            color_back = (color1-20, color2-20, color3-20)
        
        if len(self.pos2) > 1:
            if len(self.pos2) >= int(IPS * spend / SPEED):
                pygame.draw.lines(screen, (color1/2, color2/2, color3/2), False, self.pos2[-int(IPS*spend/SPEED):-1])
            else:
                pygame.draw.lines(screen, (color1/2, color2/2, color3/2), False, self.pos2)
    
    
    
    def draw_pend(self, color):
        
        pygame.draw.circle(screen, color, (self.x1, self.y1), 8)
        pygame.draw.circle(screen, color, (self.x2, self.y2), 8)
        pygame.draw.lines(screen, color, False, [(self.x0, self.y0), (self.x1, self.y1), (self.x2, self.y2)], width=3)
            
        
            
        
def graph(pendule):
    size = len(pendule.T)
    
    plt.plot(np.linspace(0, time, len(pendule.T)), pendule.T[:size], label='Ec')
    plt.plot(np.linspace(0, time, len(pendule.V)), pendule.V[:size], label='Ep')
    plt.plot(np.linspace(0, time, len(pendule.Em)), pendule.Em[:size], label='Em')
    
    plt.legend()
    plt.xlabel("Temps (s)")
    plt.ylabel("Energie (J)")
    
        
        

# ---------------GAME----------------------

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pendule double')

# pendule1 = Pendule(180, 180.1)
pendules = []

for i in range(1, len(ARCENCIEL), 2):
    pendules.append(Pendule(180, 180 + i/1000))

print(len(pendules))

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
    
    pressed_keys = pygame.key.get_pressed()
    pos = pygame.mouse.get_pos()
    
    for i in range(len(pendules)):
        pendules[i].update(p)
        pendules[i].draw_lines(ARCENCIEL[i])
    
    for i in range(len(pendules)):
        pendules[i].draw_pend(ARCENCIEL[i*2])
    
    pygame.draw.circle(screen, WHITE, (WIDTH/2, HEIGHT/2), 10)
    screen.blit(FONT.render(f"Time : {round(time, 3):.3f}", True, WHITE), (10, 5))
    screen.blit(FONT.render("Press <Escape> to Pause/Resume", True, WHITE), (10, HEIGHT-20))
    pygame.display.flip()
    
    FPS.tick(IPS)
    
pygame.quit()


# graph(pendule1)