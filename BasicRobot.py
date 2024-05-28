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

    def update(self):
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
