import pygame
from battle_ui import BattleUI
from animation_func import SimpleAnimator, OverlayAnimator 
#from assets.animation import brendanbat

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pokemon_sample")

rayquaza = SimpleAnimator("rayquaza")
sceptile = SimpleAnimator("sceptile")
overlay = OverlayAnimator(screen)
#brendan = brendanbat()

clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()  
enemy_intro_played = False  
player_intro_played = False

running = True
while running:
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
                sceptile.set_state("act")

    current_time = pygame.time.get_ticks()
    if not enemy_intro_played and current_time - start_time >= 1000:
        rayquaza.set_state("act")
        enemy_intro_played = True

    if not player_intro_played and current_time - start_time >= 2500:
        sceptile.set_state("act")
        player_intro_played = True

    screen.blit(pygame.transform.scale(pygame.image.load("src/assets/sprites/battle_ui/arena/00.png"), (SCREEN_WIDTH, SCREEN_HEIGHT - 190)), (0,0))  # Fill the screen with white
    
    enemy_x = SCREEN_WIDTH - 410
    enemy_y = SCREEN_HEIGHT - 620

    playermon_x = SCREEN_WIDTH - 570
    playermon_y = SCREEN_HEIGHT - 350
    playermon, cur_x, cur_y = sceptile.animate(screen, playermon_x, playermon_y)
    enemymon, cur_x2, cur_y2 = rayquaza.animate(screen, enemy_x, enemy_y)

    if playermon:
        overlay.draw(screen, playermon, cur_x, cur_y)
    if enemymon:
        overlay.draw(screen, enemymon, cur_x2, cur_y2)

    BattleUI(screen).draw()


    pygame.display.flip()
    clock.tick(14)  

pygame.quit()