import pygame
from arena import arena
from BasicRobot import BasicRobot, Cannon

pygame.init()

# Define Screen and Colors
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 720
PURPLE = (128, 0, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("RoboArena")

clock = pygame.time.Clock()

# Variable if game active
game_active = False
settings_active = False

# load buttons
start_button_surface = pygame.image.load("img/Menu-images/startbutton.png")
start_button_surface = pygame.transform.scale_by(start_button_surface, 0.5)
settings_button_surface = pygame.image.load(
    "img/Menu-images/settingsbutton.png")
settings_button_surface = pygame.transform.scale_by(
    settings_button_surface, 0.5)
quit_button_surface = pygame.image.load("img/Menu-images/quitbutton.png")
quit_button_surface = pygame.transform.scale_by(quit_button_surface, 0.5)

# Arena
Arena = arena(1000, 1000, 50, 50, "map_Lvl_1.txt")

# Player
Player = BasicRobot("lightblue", 640, 500, 30, 45)
PlayerCannon = Cannon(Player.x, Player.y)

# Robots
Robot1 = BasicRobot("yellow", 100, 50, 30, 0)
Robot2 = BasicRobot("red", 190, 200, 30, 0)
Robot3 = BasicRobot("darkred", 270, 600, 30, 0)
Robot4 = BasicRobot("black", 360, 60, 30, 0)

# Movement directions
x_dir = 0
y_dir = 0

while True:
    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                y_dir = -1
            elif event.key == pygame.K_a:
                x_dir = -1
            elif event.key == pygame.K_s:
                y_dir = 1
            elif event.key == pygame.K_d:
                x_dir = 1
            elif event.key == pygame.K_ESCAPE:
                game_active = False
                settings_active = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                y_dir = 0
            elif event.key == pygame.K_a:
                x_dir = 0
            elif event.key == pygame.K_s:
                y_dir = 0
            elif event.key == pygame.K_d:
                x_dir = 0
        # add Mouse movement
        if event.type == pygame.MOUSEMOTION:
            print(event.pos)
        # handler for mouse button
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("Mouse Button pressed")

    if game_active:
        # Do logical updates here.
        # ...
        pygame.display.set_caption("Roboarena")
        screen.fill("light yellow")  # Fill the display with a solid color
        Arena.draw(screen)
        # Render the graphics here.
        # ...
        Player.draw(screen)
        PlayerCannon.playercannon(Player.x, Player.y, screen)

        Robot1.draw(screen)
        Robot2.draw(screen)
        Robot3.draw(screen)
        Robot4.draw(screen)
        Robot1.update(screen, Player)
        Robot2.update(screen, Player)
        Robot3.update(screen, Player)
        Robot4.update(screen, Player)
    elif settings_active:
        pygame.display.set_caption("Settings")
        screen.fill("black")
    elif not game_active and not settings_active:
        # Do logical updates here.
        # ...
        pygame.display.set_caption("Main Menu")
        # Render the graphics here.
        # ...
        screen.fill("grey")  # Fill the display with a solid color

        text_font = pygame.font.Font(None, 100)
        text_surface = text_font.render("Main Menu", True, "black")
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2,
                                          SCREEN_HEIGHT // 6))
        screen.blit(text_surface, text_rect)

        start_button_rect = start_button_surface.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        screen.blit(start_button_surface, start_button_rect)
        settings_button_rect = settings_button_surface.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(settings_button_surface, settings_button_rect)
        quit_button_rect = quit_button_surface.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5))
        screen.blit(quit_button_surface, quit_button_rect)
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("Mouse Button pressed")
            if start_button_rect.collidepoint(event.pos):
                game_active = True
            elif settings_button_rect.collidepoint(event.pos):
                settings_active = True
            elif quit_button_rect.collidepoint(event.pos):
                pygame.quit()

    Player.x += 5 * x_dir
    Player.y += 5 * y_dir

    pygame.display.flip()  # Refresh on-screen display
    clock.tick(60)  # wait until next frame (at 60 FPS)
