import pygame

pygame.init()

# Define Screen and Colors
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PURPLE = (128, 0, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()

# Variable if game active
game_active = False

# Button
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 100
BUTTON_COLOR = "white"
BUTTON_TEXT = "Start Game"
BUTTON_TEXT_COLOR = "purple"

# Font
font = pygame.font.Font(None, 36)
text_surface = font.render(BUTTON_TEXT, True, BUTTON_TEXT_COLOR)
text_rect = (
    text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

while True:
    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                print("w")
                # add movement
            elif event.key == pygame.K_a:
                print("a")
                # add movement
            elif event.key == pygame.K_s:
                print("s")
                # add movement
            elif event.key == pygame.K_d:
                print("d")
                # add movement
        # add Mouse movement
        if event.type == pygame.MOUSEMOTION:
            print(event.pos)
        # handler for mouse button
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("Mouse Button pressed")
            if text_rect.collidepoint(event.pos):
                game_active = True

    if game_active:
        # Do logical updates here.
        # ...

        screen.fill("light blue")  # Fill the display with a solid color

        # Render the graphics here.
        # ...
        
    else:    
        # Do logical updates here.
        # ...

        screen.fill("purple")  # Fill the display with a solid color

        # Render the graphics here.
        # ...

        # Draw Start-Button
        pygame.draw.rect(screen, BUTTON_COLOR,
                        (SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2,
                        SCREEN_HEIGHT // 2 - BUTTON_HEIGHT // 2,
                        BUTTON_WIDTH, BUTTON_HEIGHT))
        screen.blit(text_surface, text_rect)

    pygame.display.flip()  # Refresh on-screen display
    clock.tick(60)         # wait until next frame (at 60 FPS)
