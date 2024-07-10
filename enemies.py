import pygame
from random import choice


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, player, collision_sprites):
        super().__init__(groups)
        self.player = player
        self.enemy_sprites = groups[1]

        # image
        self.frames, self.frame_index = frames, 0
        self.image = self.frames[self.frame_index]
        self.animation_speed = 0.2

        # rect
        self.rect = self.image.get_rect(center=pos)
        self.hitbox_rect = self.rect.inflate(-20, -40)
        self.collision_sprites = collision_sprites

        # move
        self.vel = 2
        self.dir = pygame.math.Vector2(0, 0)
        self.change_dir_time = pygame.time.get_ticks() + 1000

    def animate(self):
        self.frame_index += self.animation_speed
        self.image = pygame.transform.scale_by(self.
                                               frames[int(self.frame_index)
                                                      % len(self.frames)], 0.5)

    def move(self):
        player_pos = pygame.Vector2(self.player.rect.center)
        enemy_pos = pygame.Vector2(self.rect.center)
        if pygame.time.get_ticks() > self.change_dir_time:
            self.dir = choice((pygame.math.Vector2(0, 0),
                               pygame.math.Vector2(1, 0),
                               pygame.math.Vector2(-1, 0),
                               pygame.math.Vector2(0, 1),
                               pygame.math.Vector2(0, -1),
                               pygame.math.Vector2(1, 1).normalize(),
                               pygame.math.Vector2(-1, 1).normalize(),
                               pygame.math.Vector2(1, -1).normalize(),
                               pygame.math.Vector2(1, 1).normalize(),
                               pygame.math.Vector2(player_pos -
                                                   enemy_pos).normalize(),
                               pygame.math.Vector2(player_pos -
                                                   enemy_pos).normalize(),
                               pygame.math.Vector2(player_pos -
                                                   enemy_pos).normalize(),))
            self.change_dir_time = pygame.time.get_ticks() + choice(
                (700, 800, 900, 1000, 1100, 1200, 1300, 1400))

        self.hitbox_rect.x += self.dir.x * self.vel
        self.collision('horizontal')
        self.hitbox_rect.y += self.dir.y * self.vel
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite != self and sprite.rect.colliderect(self.hitbox_rect):
                if (direction == "horizontal"):
                    if self.dir.x > 0:
                        self.hitbox_rect.right = sprite.rect.left
                    elif self.dir.x < 0:
                        self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.dir.y < 0:
                        self.hitbox_rect.top = sprite.rect.bottom
                    elif self.dir.y > 0:
                        self.hitbox_rect.bottom = sprite.rect.top

        for enemy in self.enemy_sprites:
            if enemy != self and enemy.rect.colliderect(self.hitbox_rect):
                if (direction == "horizontal"):
                    if self.dir.x > 0:
                        self.hitbox_rect.right = enemy.hitbox_rect.left
                    elif self.dir.x < 0:
                        self.hitbox_rect.left = enemy.hitbox_rect.right
                    self.dir.x = 0
                else:
                    if self.dir.y < 0:
                        self.hitbox_rect.top = enemy.hitbox_rect.bottom
                    elif self.dir.y > 0:
                        self.hitbox_rect.bottom = enemy.hitbox_rect.top
                    self.dir.y = 0

    def update(self):
        self.move()
        self.animate()
