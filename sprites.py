import pygame
from math import atan2, degrees


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)


class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)


class Cannon(pygame.sprite.Sprite):
    def __init__(self, player, groups, image, scale):
        # player connection
        self.player = player
        self.player_direction = pygame.Vector2(1, 0)
        self.SCREEN_WIDTH = 1000
        self.SCREEN_HEIGHT = 720

        # sprite setup
        super().__init__(groups)
        self.cannon_surf = pygame.image.load(image)
        self.cannon_surf = pygame.transform.scale_by(self.cannon_surf, scale)
        self.image = self.cannon_surf
        self.rect = self.image.get_rect(
            center=self.player.rect.center)

    def get_direction(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        player_pos = pygame.Vector2(self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/2)
        self.player_direction = (mouse_pos - player_pos).normalize()

    def rotate_cannon(self):
        angle = degrees(atan2(
            self.player_direction.x, self.player_direction.y))
        self.rotated_image = pygame.transform.rotate(
            self.cannon_surf, angle - 180)
        self.rotated_rect = self.rotated_image.get_rect(
            center=(self.player.rect.center))

    def update(self):
        self.get_direction()
        self.rotate_cannon()
        self.image = self.rotated_image
        self.rect.topleft = self.rotated_rect.topleft


class Bullet(pygame.sprite.Sprite):
    def __init__(self, surf, pos, direction, groups):
        super().__init__(groups)
        self.surf = surf
        self.image = self.surf
        self.rect = self.image.get_rect(center=pos)
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 2100

        self.direction = direction
        self.speed = 10

    def rotate_bullet(self):
        angle = degrees(atan2(
            self.direction.x, self.direction.y))
        self.rotated_image = pygame.transform.rotate(
            self.surf, angle - 180)

    def update(self):
        self.rect.center += self.direction * self.speed
        self.rotate_bullet()
        self.image = self.rotated_image

        if pygame.time.get_ticks() - self.spawn_time >= self.lifetime:
            self.kill()
