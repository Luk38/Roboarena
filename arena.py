import pygame


class arena:
    def __init__(self, height, width, tileheight, tilewidth):
        self.height = height
        self.width = width
        self.tileheight = tileheight
        self.tilewidth = tilewidth

    n = pygame.Color('lightyellow')
    g = pygame.Color('purple')
    b = pygame.Color('blue')
    y = pygame.Color('yellow')
    r = pygame.Color('red')
    x = pygame.Color('black')
    o = pygame.Color('orange')
    Tiles = [[b, b, b, y, y, n, n, n, n, n, n, n, n, n, r, o, r, r, r, r],
             [b, b, y, y, n, n, n, n, n, n, n, n, n, n, n, r, o, r, r, r],
             [y, y, y, n, n, n, n, n, n, n, n, n, n, n, n, n, r, o, r, r],
             [n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, r, o, r],
             [n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, r, o],
             [n, x, x, x, x, x, x, n, n, x, x, n, n, n, n, n, n, n, n, r],
             [n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n],
             [n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n],
             [n, n, n, n, n, n, n, x, x, x, n, n, n, n, n, n, n, n, n, n],
             [n, n, n, n, n, n, n, n, n, n, n, n, n, n, x, x, x, x, x, x],
             [n, g, n, g, n, g, n, g, n, g, n, g, n, n, x, x, x, x, x, x],
             [n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n],
             [n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n],
             [n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n],
             [n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n],
             [n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n],
             [n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n],
             [n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n]]

    def draw(self, screen):
        for i in range(0, len(self.Tiles)):
            for j in range(0, len(self.Tiles[i])):
                pygame.draw.rect(screen, self.Tiles[i][j], 
                                 (j*self.tileheight, 
                                  i*self.tilewidth, 
                                  self.tilewidth, 
                                  self.tileheight))
