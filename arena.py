import pygame
from sprites import Sprite, CollisionSprite
from pytmx.util_pygame import load_pygame


class arena:
    def __init__(self, all_sprites, collision_sprites, map, tile_size):
        self.map = map
        self.tilesize = tile_size
        self.all_sprites = all_sprites
        self.collision_sprites = collision_sprites

    def setup(self):
        map = load_pygame('Maps/Wasteland_Map/Roboarena_Wasteland.tmx')
        for x, y, image in map.get_layer_by_name('Kachelebene').tiles():
            Sprite((x * self.tilesize, y * self.tilesize),
                   image, self.all_sprites)
        for x, y, image in map.get_layer_by_name('Deko').tiles():
            Sprite((x * self.tilesize, y * self.tilesize),
                   image, self.all_sprites)
        for obj in map.get_layer_by_name('Objektebene'):
            CollisionSprite((obj.x, obj.y),
                            pygame.Surface((obj.width, obj.height)),
                            self.collision_sprites)
