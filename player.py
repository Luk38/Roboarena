import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.image.load("img/Assets/player.png")
        self.rect = self.image.get_rect(center=pos)
        self.hitbox_rect = self.rect.inflate(-40, 0)

        # movement
        self.vel = 5
        self.dir = pygame.Vector2()
        self.collision_sprites = collision_sprites

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if (direction == "horizontal"):
                    if self.dir.x > 0:
                        self.rect.right = sprite.rect.left
                    elif self.dir.x < 0:
                        self.rect.left = sprite.rect.right
                else:
                    if self.dir.y < 0:
                        self.rect.top = sprite.rect.bottom
                    elif self.dir.y > 0:
                        self.rect.bottom = sprite.rect.top

    def input(self):
        keys = pygame.key.get_pressed()
        self.dir.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.dir.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.dir = self.dir.normalize() if self.dir else self.dir

    def movement(self):
        self.rect.x += self.dir.x * self.vel
        self.collision("horizontal")
        self.rect.y += self.dir.y * self.vel
        self.collision("vertical")

    def update(self):
        self.input()
        self.movement()
