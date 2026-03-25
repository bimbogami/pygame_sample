import pygame
from gui.battle_ui import BattleUI
from assets.animation import pkmn_anim 
from animation_func import SimpleAnimator, OverlayAnimator 
#from assets.animation import brendanbat

pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pokemon_sample")

# Create animation object ONCE before the loop
rayquaza = SimpleAnimator("rayquaza")
overlay = OverlayAnimator(screen)
#brendan = brendanbat()

clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()  # Record when the game starts
has_played_intro = False  # Track if the intro "act" has been triggered

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #if event.type == attack:
          #rayquaza.set_state("act")

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                overlay.stats_change("UP")
                
            if event.key == pygame.K_DOWN:
                overlay.stats_change("DOWN")
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                rayquaza.set_state("act")

    # Trigger "act" animation 10ms after appearing on screen
    if not has_played_intro and pygame.time.get_ticks() - start_time >= 20:
        pygame.time.delay(1000)
        enemy_x =+ 100
        enemy_y =+ 100
        rayquaza.set_state("act")
        
        has_played_intro = True

    # Drawing
    screen.fill(WHITE)  # Fill the screen with white
    BattleUI(screen).draw()
    enemy_x = SCREEN_WIDTH - 400
    enemy_y = SCREEN_HEIGHT - 400
    cur_img, cur_x, cur_y = rayquaza.animate(screen, enemy_x, enemy_y)
    
    # Draw stat change overlay precisely cut to the sprite's silhouette
    if cur_img:
        overlay.draw(screen, cur_img, cur_x, cur_y)

    # Update the display

    pygame.display.flip()
    clock.tick(14)  

# Quit Pygame
pygame.quit()