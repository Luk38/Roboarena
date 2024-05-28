import pygame


class arena:
    def __init__(self, height, width, tileheight, tilewidth, filename):
        self.height = height
        self.width = width
        self.tileheight = tileheight
        self.tilewidth = tilewidth
        self.tiles = self.load_arena(filename)
        print(self.tiles)


    mapping = {"n": pygame.Color('lightyellow'),
               "g": pygame.Color('purple'),
               "b": pygame.Color('blue'),
               "y": pygame.Color('yellow'),
               "r": pygame.Color('red'),
               "x": pygame.Color('black'),
               "o": pygame.Color('orange')}


    def draw(self, screen):
        for i in range(0, len(self.tiles)):
            for j in range(0, len(self.tiles[i])):
                pygame.draw.rect(screen, self.tiles[i][j],
                                 (j * self.tileheight,
                                  i * self.tilewidth,
                                  self.tilewidth,
                                  self.tileheight))


    def load_arena(self, filename):
        tiles = []
        with open(filename, 'r') as f:
            for line in f:
                tiles.append(list(map(self.mapping.get, list(line.strip()))))
        return tiles
