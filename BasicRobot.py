import pygame
import math


class BasicRobot:
    def __init__(self, color, x, y, r, alpha):
        self.color = color
        self.x = x
        self.y = y
        self.r = r
        self.alpha = math.radians(alpha)

        # movement attributes
        self.a = 0
        self.a_alpha = 0
        self.v = 0
        self.v_alpha = 0

        self.a_max = 5
        self.a_alpha_max = 2

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)
        pygame.draw.circle(screen, "black", (self.x, self.y), self.r, width=1)

    def update(self, screen):
        # update speed
        self.v += self.a

        # speed limit
        self.v = max(-self.a_max, min(self.v, self.a_max))

        # update turning speed
        self.v_alpha += self.a_alpha

        # turning speed limit
        self.v_alpha = max(-self.a_alpha_max, min(self.v_alpha, self.a_alpha_max))

        # update position
        self.x += self.v * math.cos(math.radians(self.alpha))
        self.y += self.v * math.sin(math.radians(self.alpha))
        self.alpha += self.v_alpha

        # handle reaching the edges of the screen
        if self.x < self.r or self.x > 1000 - self.r:
            self.v = 0
            self.a *= -1
        if self.y < self.r or self.y > 720 - self.r:
            self.v = 0
            self.a *= -1

        self.handle_user_input()

        self.Cannon = Cannon(self.x, self.y)
        self.Cannon.update(self.alpha, screen)

    def handle_user_input(self):
        # Based on the input, modify the acceleration (a) and rotational acceleration (a_alpha) of the robots
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.a_alpha = -0.2  # Set negative acceleration to move left
        elif keys[pygame.K_RIGHT]:
            self.a = 0.2
        elif keys[pygame.K_UP]:
            self.a = 0.5
        elif keys[pygame.K_DOWN]:
            self.a_alpha = 0.2  # Set positive


class Cannon:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("img/Assets/cannon.png")
        self.image = pygame.transform.scale(
            self.image, (28, 240)
        )  # Skaliere das Bild auf eine geeignete Größe
        self.image_rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self, alpha, screen):
        angle = math.degrees(alpha)
        rotated_image = pygame.transform.rotate(self.image, -angle - 90)
        rotated_rect = rotated_image.get_rect(center=(self.x, self.y))
        screen.blit(rotated_image, rotated_rect.topleft)

    def playercannon(self, x, y, screen):
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
