import pygame
import math
from typing import Type


class BasicRobot:
    def __init__(self, color: str, x: int, y: int, r: int, alpha: int):
        self.color = color
        self.x = x
        self.y = y
        self.r = r
        self.alpha = math.radians(alpha)

        # movement attributes
        self.a = 0.1
        self.a_alpha = 0.001
        self.v = 0
        self.v_alpha = 0

        self.a_max = 10
        self.a_alpha_max = 0.01

    # Draw Robot on the screen
    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)
        pygame.draw.circle(screen, "black", (self.x, self.y), self.r, width=1)

    def update(self, screen: pygame.Surface, player: Type["BasicRobot"]):

        # update speed
        self.v += self.a

        # speed limit
        self.v = max(-self.a_max, min(self.v, self.a_max))

        # update turning speed
        self.v_alpha += self.a_alpha

        # turning speed limit
        self.v_alpha = max(-self.a_alpha_max, min(self.v_alpha,
                                                  self.a_alpha_max))

        # User Input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.x > self.r:
                self.x -= self.v  # move left
        elif keys[pygame.K_RIGHT]:
            if self.x < 1000 - self.r:
                self.x += self.v   # move right
        elif keys[pygame.K_UP]:
            if self.y > self.r:
                self.y -= self.v  # move up
        elif keys[pygame.K_DOWN]:
            if self.y < 720 - self.r:
                self.y += self.v  # move down
        elif keys[pygame.K_u]:
            self.a_alpha += 0.001
        elif keys[pygame.K_j]:
            self.a_alpha -= 0.001
        elif keys[pygame.K_i]:
            self.a += 0.001
        elif keys[pygame.K_k]:
            self.a -= 0.001

        # Vektor vom Objekt zur Maus
        dx = player.rect.centerx - self.x
        dy = player.rect.centery - self.y

        # Winkel berechnen
        angle_rad = math.atan2(dy, dx)
        # angle_deg = math.degrees(angle_rad)

        if angle_rad - self.alpha > 0.01:
            self.alpha += self.v_alpha
        elif angle_rad - self.alpha < -0.01:
            self.alpha -= self.v_alpha
        else:
            self.alpha += 0

        # Cannon for a Robot
        self.Cannon = Cannon(self.x, self.y)
        self.Cannon.update(self.alpha, screen)


class Cannon:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.image = pygame.image.load("img/Assets/cannon.png")
        self.image = pygame.transform.scale(
            self.image, (14, 120)
        )  # Skaliere das Bild auf eine geeignete Größe
        self.image = pygame.transform.scale_by(self.image, 0.65)
        self.image_rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self, alpha: int, screen: pygame.Surface):
        angle = math.degrees(alpha)
        rotated_image = pygame.transform.rotate(self.image, -angle - 90)
        rotated_rect = rotated_image.get_rect(center=(self.x, self.y))
        screen.blit(rotated_image, rotated_rect.topleft)

    def playercannon(self, x: int, y: int, screen: pygame.Surface):
        # Mausposition abrufen
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Vektor vom Objekt zur Maus
        dx = mouse_x - x
        dy = mouse_y - y

        # Winkel berechnen
        angle_rad = math.atan2(dy, dx)
        angle_deg = math.degrees(angle_rad)

        # Bild rotieren
        rotated_image = pygame.transform.rotate(self.image, -angle_deg - 90)
        rotated_rect = rotated_image.get_rect(center=(x, y))
        screen.blit(rotated_image, rotated_rect.topleft)
