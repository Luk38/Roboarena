import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.image.load("img/Assets/player.png")
        self.image = pygame.transform.scale_by(self.image, 0.5)
        self.rect = self.image.get_rect(center=pos)
        self.hitbox_rect = self.rect.inflate(-20, 0)

        # movement
        self.vel = 1
        self.dir = pygame.Vector2()
        self.collision_sprites = collision_sprites

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
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

    def input(self):
        keys = pygame.key.get_pressed()
        self.dir.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.dir.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])

    def movement(self):
        self.hitbox_rect.x += self.dir.x * self.vel
        self.collision("horizontal")
        self.hitbox_rect.y += self.dir.y * self.vel
        self.collision("vertical")
        self.rect.center = self.hitbox_rect.center

    def update(self):
        self.input()
        self.movement()
