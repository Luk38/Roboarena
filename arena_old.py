import pygame


class old_arena:
    def __init__(self, height: int, width: int, tileheight: int,
                 tilewidth: int, filename: str):
        self.height = height
        self.width = width
        self.tileheight = tileheight
        self.tilewidth = tilewidth
        self.tiles = self.load_arena(filename)
        print(self.tiles)

    mapping = {"n": pygame.image.load('img/Blue_Brick.png'),
               "g": pygame.image.load('img/purple2.png'),
               "b": pygame.image.load('img/water3.png'),
               "y": pygame.image.load('img/sand.png'),
               "r": pygame.image.load('img/fire.png'),
               "x": pygame.image.load('img/black.png'),
               "o": pygame.image.load('img/orange_fire.png')}

    def draw(self, screen: pygame.Surface):
        for i in range(0, len(self.tiles)):
            for j in range(0, len(self.tiles[i])):
                screen.blit(self.tiles[i][j],
                            (j * self.tilewidth, i * self.tileheight))

    def load_arena(self, filename: str):
        tiles = []
        with open(filename, 'r') as f:
            for line in f:
                tiles.append(list(map(self.mapping.get, list(line.strip()))))
        return tiles
