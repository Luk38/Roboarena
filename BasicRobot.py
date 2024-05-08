import pygame

class BasicRobot:
    def __init__(self, color, x, y, r, alpha):
        self.color = color
        self.x = x
        self.y = y
        self.r = r
        self.alpha = alpha
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)