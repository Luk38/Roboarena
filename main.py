import pygame
import pygame_gui
from player import Player, Player2
from arena import arena
from groups import AllSprites
from sprites import Cannon, Cannon2, Bullet, Healthbar, Score
from enemies import Enemy
from random import choice, randint
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
main_menu_active = True
map_selection_active = False
pause_active = False

# GUI-Manager
manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

# sliders
slider_music = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((500, 250), (350, 35)),  # position and size
    start_value=0.5,
    value_range=(0, 1),
    manager=manager  # GUI-Manager
)

slider_sound = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((500, 350), (350, 35)),  # position and size
    start_value=0.5,
    value_range=(0, 1),
    manager=manager  # GUI-Manager
)

# Main Menu buttons
start_button_surface = pygame.image.load("img/Menu-images/startbutton.png")
start_button_surface = pygame.transform.scale_by(start_button_surface, 0.5)
settings_button_surface = pygame.image.load(
    "img/Menu-images/settingsbutton.png")
settings_button_surface = pygame.transform.scale_by(
    settings_button_surface, 0.5)
quit_button_surface = pygame.image.load("img/Menu-images/quitbutton.png")
quit_button_surface = pygame.transform.scale_by(quit_button_surface, 0.5)

# Map Selection buttons
wasteland_button_surface = pygame.image.load(
    "img/Menu-images/Wastelandbutton.png")
wasteland_button_surface = pygame.transform.scale_by(
    wasteland_button_surface, 0.5)

toxic_button_surface = pygame.image.load("img/Menu-images/Toxicbutton.png")
toxic_button_surface = pygame.transform.scale_by(toxic_button_surface, 0.5)

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

# Pause buttons
continue_button_surface = pygame.image.load(
    "img/Menu-images/continuebutton.png"
)
continue_button_surface = pygame.transform.scale_by(
    continue_button_surface, 0.5
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
selected_map = ""

# Player
player = Player((1500, 800), all_sprites,
                collision_sprites, enemy_sprites)
player_cannonb = Cannon(
    player, all_sprites, "img/Assets/Gun_07_B.png", 0.25)
player_cannon = Cannon(player, all_sprites, "img/Assets/cannon.png", 0.35)

player2 = Player2((1600, 800), all_sprites,
                  collision_sprites, enemy_sprites)
player_cannonb2 = Cannon2(
    player2, all_sprites, "img/Assets/Gun_07_B.png", 0.25)
player_cannon2 = Cannon2(player2, all_sprites, "img/Assets/cannon.png", 0.35)


# Bullet
player_bullet_surf = pygame.image.load("img/Assets/Plasma.png")
player_bullet_surf = pygame.transform.scale_by(player_bullet_surf, 0.3)

# Cannon timer
can_shoot = True
shoot_time = 0
cannon_cooldown = 50
mouse_button_pressed = False

# enemy spawn timer
enemy_spawn_time = 4000
enemy_event = pygame.event.custom_type()
pygame.time.set_timer(enemy_event, enemy_spawn_time)

# enemy shoot timer
enemy_shoot_cooldown = 2000


def reset_game(selected_map):
    global game_active, game_over_active, main_menu_active, all_sprites
    global score, pause_active, player2, player_cannon2, player_cannonb2
    global collision_sprites, enemy_sprites, bullet_sprites
    global enemy_bullet_sprites, game_map
    global player, healthbar, player_cannon, player_cannonb

    # Spielzustände zurücksetzen
    score = 0

    # Erstelle neue Gruppen
    all_sprites = AllSprites()
    collision_sprites = pygame.sprite.Group()
    enemy_sprites = pygame.sprite.Group()
    bullet_sprites = pygame.sprite.Group()
    enemy_bullet_sprites = pygame.sprite.Group()

    # Re-create the arena with the selected map
    game_map = arena(all_sprites, collision_sprites, selected_map, 32)
    game_map.setup()

    # Spieler und seine Kanonen neu erstellen
    player = Player(
        (1500, 800), all_sprites, collision_sprites,
        enemy_sprites
    )
    player_cannonb = Cannon(
        player, all_sprites, "img/Assets/Gun_07_B.png", 0.25
    )
    player_cannon = Cannon(
        player, all_sprites, "img/Assets/cannon.png", 0.35
    )

    player2 = Player2((1600, 800), all_sprites,
                      collision_sprites, enemy_sprites)
    player_cannonb2 = Cannon2(
        player2, all_sprites, "img/Assets/Gun_07_B.png", 0.25)
    player_cannon2 = Cannon2(
        player2, all_sprites, "img/Assets/cannon.png", 0.35)

    # Spieler-Score
    score = Score(player, all_sprites)
    all_sprites.add(score)

    # Gesundheitsleiste neu erstellen
    healthbar = Healthbar(player, all_sprites)
    all_sprites.add(healthbar)

    return game_map


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
enemy_type = list(enemy_frames.keys())
frames_list = list(enemy_frames.values())

# Score
score = Score(player, all_sprites)
all_sprites.add(score)

# Healthbar
healthbar = Healthbar(player, all_sprites)
all_sprites.add(healthbar)

while True:
    # Process player inputs. Event handler
    time_delta = clock.tick(1000)  # time between frames

    # Process player inputs. Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game_active:
                    game_active = False
                    pause_active = True
                else:
                    game_active = False
                    settings_active = False
                    game_over_active = False
                    main_menu_active = True
                    map_selection_active = False
                    pause_active = False

        # handler for enemy spawn event
        if event.type == enemy_event:
            if game_active:
                index = randint(0, 1)
                Enemy(choice(game_map.spawn_positions),
                      frames_list[index],
                      (all_sprites, enemy_sprites),
                      player, collision_sprites, enemy_bullet_sprites,
                      enemy_type[index], enemy_shoot_cooldown)

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pos2 = (player_cannonb2.rect.center +
                            player_cannon2.player_direction * 30)
                    print(player2.rect.center)
                    Bullet(player_bullet_surf, pos2,
                           player_cannon2.player_direction,
                           (all_sprites, bullet_sprites))

    if game_active:
        pygame.display.set_caption("Roboarena")
        screen.fill("light yellow")  # Fill the display with a solid color

        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)

        # bullet collisions
        if bullet_sprites:
            for bullet in bullet_sprites:
                hit_sprites = pygame.sprite.spritecollide(
                    bullet, enemy_sprites, dokill=True,
                    collided=pygame.sprite.collide_mask)
                if hit_sprites:
                    for sprite in hit_sprites:
                        sprite.destroy()
                        enemy_sprites.remove(sprite)  # Remove from group
                        bullet.kill()  # Remove the bullet
                        score.score += 1
                        enemy_destroyed_sound.play()
                    if score.score % 10 == 0:
                        if enemy_shoot_cooldown > 100:
                            enemy_shoot_cooldown -= 100
                        if enemy_spawn_time > 200:
                            enemy_spawn_time -= 200
                            enemy_event = pygame.event.custom_type()
                            pygame.time.set_timer(
                                enemy_event, enemy_spawn_time)

                obj_hit_sprites = pygame.sprite.spritecollide(
                    bullet, collision_sprites, dokill=False,
                    collided=pygame.sprite.collide_mask)
                if obj_hit_sprites:
                    bullet.kill()

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
            for bullet in enemy_bullet_sprites:
                obj_hit = pygame.sprite.spritecollide(
                        bullet, collision_sprites, dokill=False,
                        collided=pygame.sprite.collide_mask)
                if obj_hit:
                    bullet.kill()

        # update all sprites
        all_sprites.update()
        # update GUI-Manager
        manager.update(time_delta)
        # load_images()
        # Render the graphics here.
        # ...

        # draw all sprites
        all_sprites.draw(player.rect.center)

    elif map_selection_active:
        pygame.display.set_caption("Map Selection")
        screen.fill("grey")

        # Render the map selection text
        text_font = pygame.font.Font(None, 80)
        text_surface = text_font.render("Choose a Map", True, "black")
        text_rect = text_surface.get_rect(center=(
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6))
        screen.blit(text_surface, text_rect)

        # Display Wasteland and Toxic map buttons
        wasteland_button_rect = wasteland_button_surface.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.5))
        screen.blit(wasteland_button_surface, wasteland_button_rect)

        toxic_button_rect = toxic_button_surface.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5))
        screen.blit(toxic_button_surface, toxic_button_rect)

        # Check for button clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (event.type == pygame.MOUSEBUTTONDOWN
               and not mouse_button_pressed):
                mouse_button_pressed = True
                if wasteland_button_rect.collidepoint(event.pos):
                    # Set Wasteland arena
                    selected_map = "Maps/Wasteland_Map/Roboarena_Wasteland.tmx"
                    reset_game(selected_map)
                    # Start game with Wasteland map
                    game_active = True
                    map_selection_active = False
                    button_sound.play()
                    pygame.mixer.music.stop()  # Stop the background music

                elif toxic_button_rect.collidepoint(event.pos):
                    # Set Toxic arena
                    selected_map = "Maps/Toxic_Map/Roboarena_Toxic.tmx"
                    reset_game(selected_map)
                    # Start game with Toxic map
                    game_active = True
                    map_selection_active = False
                    button_sound.play()
                    pygame.mixer.music.stop()
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_button_pressed = False

    elif pause_active:
        pygame.display.set_caption("Pause")
        screen.fill("grey")

        # Pause Text
        pause_text_font = pygame.font.Font(None, 100)
        pause_text_surface = pause_text_font.render(
            "Pause", True, "black"
        )
        pause_text_rect = pause_text_surface.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6)
        )
        screen.blit(pause_text_surface, pause_text_rect)

        # Score Text
        score_text_font = pygame.font.Font(None, 70)
        score_text_surface = score_text_font.render(
            f"Score: {score.score}", True, "black"
        )
        score_text_rect = score_text_surface.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.5)
        )
        screen.blit(score_text_surface, score_text_rect)

        # Game Over buttons
        main_menu_button_rect = main_menu_button_surface.get_rect(
            center=(SCREEN_WIDTH // 1.5, SCREEN_HEIGHT // 1.5))
        screen.blit(main_menu_button_surface, main_menu_button_rect)
        continue_button_rect = continue_button_surface.get_rect(
            center=(SCREEN_WIDTH // 3, SCREEN_HEIGHT // 1.5))
        screen.blit(continue_button_surface, continue_button_rect)
        if event.type == pygame.MOUSEBUTTONDOWN and not mouse_button_pressed:
            mouse_button_pressed = True
            if continue_button_rect.collidepoint(event.pos):
                button_sound.play()
                game_active = True
                pause_active = False
            if main_menu_button_rect.collidepoint(event.pos):
                reset_game(selected_map)
                settings_active = False
                game_active = False
                pause_active = False
                main_menu_active = True
                button_sound.play()
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_button_pressed = False

    elif settings_active:
        # passes events to GUI-Manager
        manager.process_events(event)
        pygame.display.set_caption("Settings")
        screen.fill("grey")

        # Settings Text
        settings_text_font = pygame.font.Font(None, 100)
        settings_text_surface = settings_text_font.render(
            "Settings", True, "black"
        )
        settings_text_rect = settings_text_surface.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6)
        )
        screen.blit(settings_text_surface, settings_text_rect)

        # Music volume Text
        music_volume_text_font = pygame.font.Font(None, 50)
        music_volume_text_surface = music_volume_text_font.render(
            "music volume", True, "black"
        )
        music_volume_text_rect = music_volume_text_surface.get_rect(
            center=(SCREEN_WIDTH // 7.2, 267)
        )
        screen.blit(music_volume_text_surface, music_volume_text_rect)

        # sound effects volume Text
        sound_effects_volume_text_font = pygame.font.Font(None, 50)
        sound_effects_volume_text_surface = (
            sound_effects_volume_text_font.render(
                "sound effects volume", True, "black"))
        sound_effects_volume_text_rect = (
            sound_effects_volume_text_surface.get_rect(
                center=(SCREEN_WIDTH // 5, 367)))
        screen.blit(
            sound_effects_volume_text_surface, sound_effects_volume_text_rect
        )

        # slider
        manager.update(time_delta)
        manager.draw_ui(screen)

        # set main music volume
        pygame.mixer.music.set_volume(slider_music.get_current_value())

        # set sound effects volume
        button_sound.set_volume(slider_sound.get_current_value())
        player_destroyed_sound.set_volume(slider_sound.get_current_value())
        player_shoot_sound.set_volume(slider_sound.get_current_value())
        player_damage_sound.set_volume(slider_sound.get_current_value())
        enemy_destroyed_sound.set_volume(slider_sound.get_current_value())

        main_menu_button_rect = main_menu_button_surface.get_rect(
            center=(SCREEN_WIDTH // 1.47, 500))
        screen.blit(main_menu_button_surface, main_menu_button_rect)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not mouse_button_pressed:
                mouse_button_pressed = True
                if main_menu_button_rect.collidepoint(event.pos):
                    settings_active = False
                    game_over_active = False
                    game_active = False
                    main_menu_active = True
                    button_sound.play()

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_button_pressed = False

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
            f"Score: {score.score}", True, "white"
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
        if event.type == pygame.MOUSEBUTTONDOWN and not mouse_button_pressed:
            mouse_button_pressed = True
            if play_again_button_rect.collidepoint(event.pos):
                reset_game(selected_map)
                button_sound.play()
                map_selection_active = True
                game_over_active = False
                game_active = False
                main_menu_active = False
            if main_menu_button_rect.collidepoint(event.pos):
                reset_game(selected_map)
                settings_active = False
                game_over_active = False
                game_active = False
                main_menu_active = True
                button_sound.play()
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_button_pressed = False

    elif main_menu_active:
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
        if event.type == pygame.MOUSEBUTTONDOWN and not mouse_button_pressed:
            mouse_button_pressed = True
            if start_button_rect.collidepoint(event.pos):
                main_menu_active = False
                map_selection_active = True
                pygame.mixer.music.stop()  # stop the backround music
                button_sound.play()
            elif settings_button_rect.collidepoint(event.pos):
                main_menu_active = False
                settings_active = True
                button_sound.play()
            elif quit_button_rect.collidepoint(event.pos):
                pygame.quit()
                raise SystemExit
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_button_pressed = False
    pygame.display.flip()  # Refresh on-screen display
    clock.tick(60)  # wait until next frame (at 60 FPS)
