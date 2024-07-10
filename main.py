import pygame
from player import Player
# from arena_old import old_arena
from arena import arena
from BasicRobot import Cannon
from groups import AllSprites
from enemies import Enemy
from random import choice
from os.path import join
from os import walk


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

# groups
all_sprites = AllSprites()
collision_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()

# Arena
# Old_arena = old_arena(1000, 1000, 50, 50, "map_Lvl_1.txt")
# Wasteland_arena = arena(all_sprites, collision_sprites,
# "Maps/Wasteland_Map/Roboarena_Wasteland.tmx", 32)
# Wasteland_arena.setup()

Wasteland_arena = arena(all_sprites, collision_sprites,
                        "Maps/Toxic_Map/Roboarena_Toxic.tmx", 32)
Wasteland_arena.setup()

# Player
player = Player((1500, 800), (all_sprites, collision_sprites),
                collision_sprites)
PlayerCannon = Cannon(player.rect.x, player.rect.y)

# enemy spawn timer
enemy_event = pygame.event.custom_type()
pygame.time.set_timer(enemy_event, 8000)


# load enemy images
def load_images():
    folders = list(walk(join('img', 'enemies')))[0][1]
    enemy_frames = {}
    for folder in folders:
        for folder_path, _, file_names in walk(join('img', 'enemies', folder)):
            enemy_frames[folder] = []
            for file_name in sorted(file_names,
                                    key=lambda name: int(name.split('.')[0])):
                full_path = join(folder_path, file_name)
                surf = pygame.image.load(full_path).convert_alpha()
                enemy_frames[folder].append(surf)
    return enemy_frames


enemy_frames = load_images()

# Movement directions
x_dir = 0
y_dir = 0

while True:
    # Process player inputs. Event handler
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
        # handler for enemy spawn event
        if event.type == enemy_event:
            Enemy(choice(Wasteland_arena.spawn_positions),
                  choice(list(enemy_frames.values())),
                  (all_sprites, enemy_sprites, collision_sprites),
                  player, collision_sprites)

    if game_active:
        # Do logical updates here.
        # ...
        pygame.display.set_caption("Roboarena")
        screen.fill("light yellow")  # Fill the display with a solid color
        # update
        all_sprites.update()
        load_images()
        # Render the graphics here.
        # ...
        # Old_arena.draw(screen)

        # draw player and cannon
        all_sprites.draw(player.rect.center)
        PlayerCannon.playercannon(SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                                  screen)

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

    pygame.display.flip()  # Refresh on-screen display
    clock.tick(120)  # wait until next frame (at 60 FPS)
