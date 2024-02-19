import numpy as np
import pygame

from numpy import cos, sin
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT




WIDTH, HEIGHT = 1800, 720
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (150, 150, 0)


class System:
    def __init__(self, l):
        self.l = l
        self.center = (WIDTH / 4, 95 * HEIGHT / 100)
        self.center2 = (3 * WIDTH / 4, self.center[1])
        self.x, self.y = 0, 1.41
        self.xa, self.ya = -.71, .71
        self.xb, self.yb = .71, .71
        self.a1 = np.radians(45)
        self.a2 = np.radians(45)
        
        self.Points = []
    
    def zeros(self, func, dfunc, x0, epsilon, nbiter):
        xk = x0
        count = 0
        while np.linalg.norm(func(xk)) > epsilon and count < nbiter:
            temp = xk - func(xk) / dfunc(xk)
            if -self.l <= temp and temp <= self.l:
                xk = temp
            else:
                return -1
            count += 1
            
        return xk
    
    
    def f(self, xa):
        return self.x**2 + self.y**2 - 2 * self.x * xa - 2 * self.y * np.sqrt(self.l**2 - xa**2)
    
    def df(self, xa):
        return -2 * self.x + 2 * self.y * xa / np.sqrt(self.l**2 - xa**2)
    
    def solve(self, M):
        epsilon = 1e-8
        N = 100
        
        self.x, self.y = M[0], M[1]
        # print("({}, {})".format(int(self.x), int(self.y)))
        
        self.xa = self.zeros(self.f, self.df, -(self.l - 1e-5), epsilon, N)
        self.ya = np.sqrt(self.l**2 - self.xa**2)
        # print("({}, {}) - ({}, {})".format(int(self.xa), int(self.ya), int(self.xb), int(self.yb)))
        
        self.xb = self.zeros(self.f, self.df, (self.l - 1e-5), epsilon, N)
        self.yb = np.sqrt(self.l**2 - self.xb**2)
            
        
    def trace(self):
        arm_thickness = 4
        # --- Zone de définition ---
        pygame.draw.circle(screen, YELLOW, (self.center2[0], self.center2[1]), self.l*2)
        pygame.draw.circle(screen, BLACK, (self.center2[0] - self.l, self.center2[1]), self.l)
        pygame.draw.circle(screen, BLACK, (self.center2[0] + self.l, self.center2[1]), self.l)
        
        # --- Dessin du système ---
        M = (self.x + self.center[0], self.center[1] - self.y)
        A = (self.xa + self.center[0], self.center[1] - self.ya)
        B = (self.xb + self.center[0], self.center[1] - self.yb)
        if self.xa != -1:
            self.Points.append(M)
        
        pygame.draw.line(screen, WHITE, self.center, A, arm_thickness)
        pygame.draw.line(screen, WHITE, self.center, B, arm_thickness)
        
        pygame.draw.line(screen, WHITE, A, M, arm_thickness)
        pygame.draw.line(screen, WHITE, B, M, arm_thickness)
        
        pygame.draw.circle(screen, WHITE, self.center, 15)
        pygame.draw.circle(screen, WHITE, M, 15)
        
        n = 2000
        if len(self.Points) > 1:
            if len(self.Points) > n:
                pygame.draw.lines(screen, GREEN, False, self.Points[len(self.Points) - n :], 2)
            else:
                pygame.draw.lines(screen, GREEN, False, self.Points, 2)
        
        
    def text(self):
        if self.xa != 0:
            alpha1 = np.arctan(self.ya / -self.xa) if self.xa < 0 else np.arctan(self.ya / -self.xa) + np.pi
        else:
            alpha1 = np.pi / 2
            
        if self.xb != 0:
            alpha2 = np.arctan(self.yb / self.xb) + np.pi if self.xb < 0 else np.arctan(self.yb / self.xb)
        else:
            alpha2 = np.pi / 2
            
        FONT = pygame.font.Font(None, 25)
        # control
        text0 = FONT.render("alpha 1 = {}".format(int(np.degrees(alpha1))), True, WHITE)
        text1 = FONT.render("alpha 2 = {}".format(int(np.degrees(alpha2))), True, WHITE)
        
        consigne = FONT.render("Écrire dans la zone jaune en maintenant le click", True, WHITE)
        
        screen.blit(text0, (10, 5))
        screen.blit(text1, (10, 25))
        screen.blit(consigne, (WIDTH * 3 / 4 - 200, HEIGHT / 5))



# ---------------GAME----------------------
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pendule double')


sys = System(200)


FPS = pygame.time.Clock()
# pos = (WIDTH / 2, HEIGHT / 2)

click = False

running = True
while running:

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN or click:
            click = True
            
            pos = pygame.mouse.get_pos()
            x, y = pos[0] - sys.center2[0], sys.center2[1] - pos[1]
            sys.solve((x, y))
        if event.type == pygame.MOUSEBUTTONUP:
            click = False
            sys.Points = []
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                print("escape")
                sys.draw_circle()
            

    
    screen.fill(BLACK)
    
    sys.trace()
    sys.text()
    # sys.trace((WIDTH / 2, HEIGHT / 2))
    pygame.display.flip()
    
    FPS.tick(60)
    
pygame.quit()
