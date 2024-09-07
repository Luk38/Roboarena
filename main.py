import pygame
from player import Player
from arena import arena
from groups import AllSprites
from sprites import Cannon, Bullet, Healthbar
from enemies import Enemy
from random import choice
from os.path import join
from os import walk


pygame.init()
pygame.mixer.init()

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
game_over_active = False
main_menu_active = False

# Main Menu buttons
start_button_surface = pygame.image.load("img/Menu-images/startbutton.png")
start_button_surface = pygame.transform.scale_by(start_button_surface, 0.5)
settings_button_surface = pygame.image.load(
    "img/Menu-images/settingsbutton.png")
settings_button_surface = pygame.transform.scale_by(
    settings_button_surface, 0.5)
quit_button_surface = pygame.image.load("img/Menu-images/quitbutton.png")
quit_button_surface = pygame.transform.scale_by(quit_button_surface, 0.5)

# Game-Over buttons
play_again_button_surface = pygame.image.load(
    "img/Game Over-images/play_again_button.png"
)
play_again_button_surface = pygame.transform.scale_by(
    play_again_button_surface, 0.5
)
main_menu_button_surface = pygame.image.load(
    "img/Game Over-images/main_menu_button.png"
)
main_menu_button_surface = pygame.transform.scale_by(
    main_menu_button_surface, 0.5
)

# groups
all_sprites = AllSprites()
collision_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()
enemy_bullet_sprites = pygame.sprite.Group()


# load main menu sound
pygame.mixer.music.load(
    "sound_effects/main_menu_2_sound.mp3"
)
# load button sound
button_sound = pygame.mixer.Sound(
    "sound_effects/button_sound.mp3"
)
# load player destroyed sound
player_destroyed_sound = pygame.mixer.Sound(
    "sound_effects/player_destroyed_sound.mp3"
)
# load player shooting sound
player_shoot_sound = pygame.mixer.Sound(
    "sound_effects/player_shoot_sound.mp3"
)
# load player damage sound
player_damage_sound = pygame.mixer.Sound(
    "sound_effects/player_damage_sound.mp3"
)
# load enemy destroyed sound
enemy_destroyed_sound = pygame.mixer.Sound(
    "sound_effects/enemy_destroyed_sound.mp3"
)

# set the music volume
pygame.mixer.music.set_volume(0.5)  # Volume (0.0 bis 1.0)

# set the sound volume
button_sound.set_volume(0.5)
player_destroyed_sound.set_volume(0.5)
player_shoot_sound.set_volume(0.5)
player_damage_sound.set_volume(0.5)
enemy_destroyed_sound.set_volume(0.5)

# Arena
# Wasteland_arena = arena(all_sprites, collision_sprites,
# "Maps/Wasteland_Map/Roboarena_Wasteland.tmx", 32)
# Wasteland_arena.setup()
Wasteland_arena = arena(all_sprites, collision_sprites,
                        "Maps/Toxic_Map/Roboarena_Toxic.tmx", 32)
Wasteland_arena.setup()

# Player
player = Player((1500, 800), (all_sprites, collision_sprites),
                collision_sprites)
player_cannonb = Cannon(
    player, all_sprites, "img/Assets/Gun_07_B.png", 0.25)
player_cannon = Cannon(player, all_sprites, "img/Assets/cannon.png", 0.35)

# Bullet
player_bullet_surf = pygame.image.load("img/Assets/Plasma.png")
player_bullet_surf = pygame.transform.scale_by(player_bullet_surf, 0.3)

# Cannon timer
can_shoot = True
shoot_time = 0
cannon_cooldown = 50
mouse_button_pressed = False

# enemy spawn timer
enemy_event = pygame.event.custom_type()
pygame.time.set_timer(enemy_event, 8000)


def reset_game():
    global game_active, game_over_active, main_menu_active, all_sprites
    global score, score_rect, score_surface, score_sprite
    global collision_sprites, enemy_sprites, bullet_sprites
    global enemy_bullet_sprites, bullet_sprites
    global player, healthbar, player_cannon, player_cannonb

    # Spielzustände zurücksetzen
    game_active = True
    game_over_active = False
    main_menu_active = False
    score = 0

    # Erstelle neue Gruppen
    all_sprites = AllSprites()
    collision_sprites = pygame.sprite.Group()
    enemy_sprites = pygame.sprite.Group()
    bullet_sprites = pygame.sprite.Group()
    enemy_bullet_sprites = pygame.sprite.Group()

    # Arena neu erstellen
    Wasteland_arena = arena(all_sprites, collision_sprites,
                            "Maps/Toxic_Map/Roboarena_Toxic.tmx", 32)
    Wasteland_arena.setup()

    # Spieler und seine Kanonen neu erstellen
    player = Player(
        (1500, 800), (all_sprites, collision_sprites), collision_sprites
    )
    player_cannonb = Cannon(
        player, all_sprites, "img/Assets/Gun_07_B.png", 0.25
    )
    player_cannon = Cannon(
        player, all_sprites, "img/Assets/cannon.png", 0.35
    )

    # Spieler-Score
    score = 0
    score_font = pygame.font.Font(None, 50)
    score_surface = score_font.render(f"Score: {score}", True, "black")
    score_rect = score_surface.get_rect(center=(player.rect.center))

    score_sprite = pygame.sprite.Sprite()
    score_sprite.image = score_surface
    score_sprite.rect = score_rect
    all_sprites.add(score_sprite)

    # Gesundheitsleiste neu erstellen
    healthbar = Healthbar(player, all_sprites)
    all_sprites.add(healthbar)


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

# Score
score = 0
score_font = pygame.font.Font(None, 50)
score_surface = score_font.render(f"Score: {score}", True, "black")
score_rect = score_surface.get_rect(center=(player.rect.center))

score_sprite = pygame.sprite.Sprite()
score_sprite.image = score_surface
score_sprite.rect = score_rect
all_sprites.add(score_sprite)

# Healthbar
healthbar = Healthbar(player, all_sprites)
all_sprites.add(healthbar)

while True:
    # Process player inputs. Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_active = False
                settings_active = False
        # handler for enemy spawn event
        if event.type == enemy_event:
            Enemy(choice(Wasteland_arena.spawn_positions),
                  choice(list(enemy_frames.values())),
                  (all_sprites, enemy_sprites, collision_sprites),
                  player, collision_sprites, enemy_bullet_sprites)

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not mouse_button_pressed:
                    mouse_button_pressed = True
                    pos = (player_cannonb.rect.center +
                           player_cannon.player_direction * 30)
                    Bullet(player_bullet_surf, pos,
                           player_cannon.player_direction,
                           (all_sprites, bullet_sprites))
                    player_shoot_sound.play()  # shooting sound
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_button_pressed = False

    if game_active:
        # Do logical updates here.
        # ...
        pygame.display.set_caption("Roboarena")
        screen.fill("light yellow")  # Fill the display with a solid color

        # bullet collisions
        if bullet_sprites:
            for bullet in bullet_sprites:
                collision_sprites = pygame.sprite.spritecollide(
                    bullet, enemy_sprites, dokill=True,
                    collided=pygame.sprite.collide_mask)
                if collision_sprites:
                    for sprite in collision_sprites:
                        sprite.destroy()
                        enemy_sprites.remove(sprite)  # Remove from group
                        bullet.kill()  # Remove the bullet
                        score += 1
                        enemy_destroyed_sound.play()


        if enemy_bullet_sprites:
            # check if player is hit by enemy bullet
            player_hit = pygame.sprite.spritecollide(
                player, enemy_bullet_sprites,
                dokill=True, collided=pygame.sprite.collide_mask
                )
            if player_hit:
                for sprite in player_hit:
                    sprite.kill()
                    # Reduce player's lives
                    player.lives -= 1
                    # update the healthbar
                    healthbar.decrease_health()
                    player_damage_sound.play()
                    if player.lives <= 0:
                        # Destroy the player if no lives left
                        game_active = False
                        game_over_active = True
                        player_destroyed_sound.play()

        # update the score
        score_surface = score_font.render(f"Score: {score}", True, BLACK)
        score_sprite.image = score_surface
        score_sprite.rect.center = player.rect.center + pygame.Vector2(
            SCREEN_WIDTH / 2.5, - SCREEN_HEIGHT / 2.2)

        # update all sprites
        all_sprites.update()
        # load_images()
        # Render the graphics here.
        # ...

        # draw all sprites
        all_sprites.draw(player.rect.center)

    elif settings_active:
        pygame.display.set_caption("Settings")
        screen.fill("black")


    elif game_over_active:
        pygame.display.set_caption("Game Over")
        screen.fill("black")

        # Game Over Text
        game_over_text_font = pygame.font.Font(None, 100)
        game_over_text_surface = game_over_text_font.render(
            "Game Over", True, "red"
        )
        game_over_text_rect = game_over_text_surface.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6)
        )
        screen.blit(game_over_text_surface, game_over_text_rect)

        # Score Text
        score_text_font = pygame.font.Font(None, 70)
        score_text_surface = score_text_font.render(
            f"Score: {score}", True, "white"
        )
        score_text_rect = score_text_surface.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.5)
        )
        screen.blit(score_text_surface, score_text_rect)

        # Game Over buttons
        main_menu_button_rect = main_menu_button_surface.get_rect(
            center=(SCREEN_WIDTH // 1.5, SCREEN_HEIGHT // 1.5))
        screen.blit(main_menu_button_surface, main_menu_button_rect)
        play_again_button_rect = play_again_button_surface.get_rect(
            center=(SCREEN_WIDTH // 3, SCREEN_HEIGHT // 1.5))
        screen.blit(play_again_button_surface, play_again_button_rect)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_again_button_rect.collidepoint(event.pos):
                reset_game()
                button_sound.play()
            if main_menu_button_rect.collidepoint(event.pos):
                settings_active = False
                game_over_active = False
                game_active = False
                button_sound.play()

    elif not game_active and not settings_active:
        # Do logical updates here.
        # backround music
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)  # -1 loop the music

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
            if start_button_rect.collidepoint(event.pos):
                game_active = True
                pygame.mixer.music.stop()  # stop the backround music
                button_sound.play()
            elif settings_button_rect.collidepoint(event.pos):
                settings_active = True
                pygame.mixer.music.stop()  # stop the backround music
                button_sound.play()
            elif quit_button_rect.collidepoint(event.pos):
                pygame.quit()

    pygame.display.flip()  # Refresh on-screen display
    clock.tick(60)  # wait until next frame (at 60 FPS)
