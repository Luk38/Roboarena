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


# Farben
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)


class Healthbar(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__()
        # Positionierung der Healthbar:
        self.player = player
        self.pos = player.pos
        self.total_health = player.lives
        self.current_health = player.lives
        self.bar_width = 200
        self.bar_height = 30
        self.cell_width = self.bar_width // self.total_health
        self.cell_height = self.bar_height
        self.image = pygame.Surface((self.bar_width, self.bar_height))
        self.rect = self.image.get_rect()
        self.update()

    def update(self):
        # Position the healthbar relative to the player
        offset = pygame.Vector2(-380, 320)
        self.rect.center = self.player.rect.center + offset
        for i in range(self.total_health):
            cell_x = i * self.cell_width
            if i < self.current_health:
                if self.current_health >= 6:
                    color = GREEN
                elif self.current_health >= 3:
                    # turn healthbar-color orange if the current health under 6
                    color = ORANGE
                else:
                    color = RED
                    # turn healthbar-color red if the current health under 3
            else:
                color = BLACK

            pygame.draw.rect(self.image, color, (cell_x, 0, self.cell_width,
                                                 self.cell_height))
            pygame.draw.rect(self.image, BLACK, (cell_x, 0, self.cell_width,
                                                 self.cell_height), 1)

        # Zeichne den Text 'HP'
        font = pygame.font.SysFont(None, 35)
        text = font.render('HP', True, BLACK)
        self.image.blit(text, (self.bar_width + 10, 0))

    def decrease_health(self):
        if self.current_health > 0:
            self.current_health -= 1
            self.update()

    def increase_health(self):
        if self.current_health < self.total_health:
            self.current_health += 1
            self.update()
