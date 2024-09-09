import pygame
from random import choice

from sprites import Bullet


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, player, collision_sprites,
                 bullet_sprites, key):
        super().__init__(*groups)

        self.player = player
        self.enemy_sprites = groups[1]
        self.all_sprites = groups[0]
        self.bullet_sprites = bullet_sprites
        self.clock = pygame.time.Clock()
        self.pos = pos
        self.key = key

        # image
        self.frames, self.frame_index = frames, 0
        self.image = self.frames[self.frame_index]
        self.state = ""
        self.idle_frames_right = frames
        self.idle_frames_left = []
        self.animation_speed = 0.08
        self.shooting_frames_right = []
        self.shooting_frames_left = []

        for frame in self.idle_frames_right:
            self.idle_frames_left.append(pygame.transform.flip(frame, True,
                                                               False))

        # load shoot animation imgs
        if self.key == "enemy_1":
            self.shooting_frames_right.append(pygame.image.load
                                              ("img/shot/1/1.png")
                                              .convert_alpha())
            self.shooting_frames_right.append(pygame.image.load
                                              ("img/shot/1/2.png")
                                              .convert_alpha())
        elif self.key == "enemy_2":
            self.shooting_frames_right.append(pygame.image.load
                                              ("img/shot/2/1.png")
                                              .convert_alpha())
            self.shooting_frames_right.append(pygame.image.load
                                              ("img/shot/2/2.png")
                                              .convert_alpha())

        for frame in self.shooting_frames_right:
            self.shooting_frames_left.append(pygame.transform.flip(frame, True,
                                                                   False))

        # rect
        self.rect = self.image.get_rect(center=pos)
        self.hitbox_rect = self.rect.inflate(-80, -100)
        self.collision_sprites = collision_sprites

        # move
        self.vel = 2
        self.dir = pygame.math.Vector2(0, 0)
        self.change_dir_time = pygame.time.get_ticks() + 1000

        # shooting
        self.shooting_dir = pygame.math.Vector2()
        self.last_shot_time = pygame.time.get_ticks()
        self.shoot_cooldown = 2500

        # Bullet
        self.bullet_surf = pygame.image.load("img/Assets/enemy_bullet.png")
        self.bullet_surf = pygame.transform.rotate(self.bullet_surf, 90)
        self.bullet_surf = pygame.transform.scale_by(self.bullet_surf, 1.25)

    def animate(self):
        self.frame_index += self.animation_speed
        self.image = pygame.transform.scale_by(self.
                                               frames[int(self.frame_index) %
                                                      len(self.frames)], 0.75)

    def move(self):
        player_pos = pygame.Vector2(self.player.rect.center)
        enemy_pos = pygame.Vector2(self.rect.center)
        self.pos = enemy_pos
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

    def shoot(self,):
        self.shooting_dir = (pygame.Vector2(self.player.rect.center)
                             - pygame.Vector2(self.rect.center)).normalize()
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.shoot_cooldown:
            pos = self.rect.center
            self.animation_speed = 0.005
            if self.state == "right":
                self.frames = self.shooting_frames_right
            else:
                self.frames = self.shooting_frames_left
            Bullet(self.bullet_surf, pos,
                   self.shooting_dir,
                   (self.all_sprites, self.bullet_sprites))
            self.last_shot_time = current_time

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

        if self.player.hitbox_rect.colliderect(self.hitbox_rect):
            if (direction == "horizontal"):
                if self.dir.x > 0:
                    self.hitbox_rect.right = self.player.hitbox_rect.left
                elif self.dir.x < 0:
                    self.hitbox_rect.left = self.player.hitbox_rect.right
                self.dir.x = 0
            else:
                if self.dir.y < 0:
                    self.hitbox_rect.top = self.player.hitbox_rect.bottom
                elif self.dir.y > 0:
                    self.hitbox_rect.bottom = self.player.hitbox_rect.top
                self.dir.y = 0

    def destroy(self):
        # kill the enemy
        self.kill

    def update(self):
        if self.player.rect.center[0] > self.rect.center[0]:
            self.state = "right"
        else:
            self.state = "left"
        if (pygame.time.get_ticks() > self.last_shot_time + 200 and
                self.state == "right"):
            self.frames = self.idle_frames_right
        elif (pygame.time.get_ticks() > self.last_shot_time + 200 and
                self.state == "left"):
            self.frames = self.idle_frames_left
        self.move()
        self.animate()
        self.shoot()
