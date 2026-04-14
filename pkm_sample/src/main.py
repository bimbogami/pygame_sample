import pygame
from battle_ui import BattleUI
from animation_func import SimpleAnimator, OverlayAnimator 
#from assets.animation import brendanbat

#dagdag

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pokemon_sample")

# --- Change these to swap pokemon ---
PLAYER_POKEMON = "Sceptile"
ENEMY_POKEMON = "Rayquaza"

rayquaza = SimpleAnimator(ENEMY_POKEMON.lower())
sceptile = SimpleAnimator(PLAYER_POKEMON.lower())
overlay = OverlayAnimator(screen)
battle_ui = BattleUI(screen, PLAYER_POKEMON, ENEMY_POKEMON)
#brendan = brendanbat()

clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()  
enemy_intro_played = False  
player_intro_played = False
message_timer = 0
message_duration = 2000

bgmusic = pygame.mixer.music.load("src/assets/sounds/battle!.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.2)

running = True
while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        choice = battle_ui.handle_event(event)

        # Only process choices if we aren't currently showing an attack message
        if choice and not battle_ui.custom_message:
            mode, label = choice
            if mode == "fight":
                # Check PP first
                if battle_ui.current_pp.get(label, 0) <= 0:
                    battle_ui.set_message("There's no PP left for this move!")
                    message_timer = pygame.time.get_ticks()
                    continue

                # Decrease PP and start the attack sequence
                battle_ui.reduce_pp(label)
                battle_ui.set_message(f"{PLAYER_POKEMON} used {label}!")
                sceptile.set_state("act")
                message_timer = pygame.time.get_ticks()
                
                # Apply move effects (stat changes)
                move_data = battle_ui.get_move_details(label)
                effects = move_data.get("effects", {})
                
                stat_changes = effects.get("stat_changes")
                self_changes = effects.get("self_stat_changes")
                
                # Apply target stat changes
                if stat_changes:
                    ttarget = "player" if effects.get("target") == "self" else "enemy"
                    battle_ui.apply_stat_change(ttarget, stat_changes)
                    # Trigger overlay animation
                    for val in stat_changes.values():
                        if val > 0:
                            overlay.stats_change(ttarget, "UP")
                            if ttarget == "player": 
                                sceptile.stats_change("UP")
                                pygame.mixer.Sound("src/assets/sounds/atk_sounds/stat_up.mp3").play()
                            else: 
                                rayquaza.stats_change("UP")
                                pygame.mixer.Sound("src/assets/sounds/atk_sounds/stat_up.mp3").play()
                        elif val < 0:
                            overlay.stats_change(ttarget, "DOWN")
                            if ttarget == "player": 
                                sceptile.stats_change("DOWN")
                                pygame.mixer.Sound("src/assets/sounds/atk_sounds/stat_down.mp3").play()
                            else: 
                                rayquaza.stats_change("DOWN")
                                pygame.mixer.Sound("src/assets/sounds/atk_sounds/stat_down.mp3").play()
                            
                # Apply self stat changes
                if self_changes:
                    battle_ui.apply_stat_change("player", self_changes)
                    for val in self_changes.values():
                        if val > 0:
                            overlay.stats_change("player", "UP")
                            sceptile.stats_change("UP")
                        elif val < 0:
                            overlay.stats_change("player", "DOWN")
                            sceptile.stats_change("DOWN")
            elif mode == "main":
                if label == "Pokémon":
                    print("Pokemon is Pressed")
                elif label == "Item":
                    print("Item is Pressed")
                elif label == "Run":
                    print("Run is Pressed")
                    running = False



        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:

                overlay.stats_change("player", "UP")
                overlay.stats_change("enemy", "UP")
                sceptile.stats_change("UP")
                rayquaza.stats_change("UP")
                
            if event.key == pygame.K_DOWN:
                overlay.stats_change("player", "DOWN")
                overlay.stats_change("enemy", "DOWN")
                sceptile.stats_change("DOWN")
                rayquaza.stats_change("DOWN")
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                rayquaza.set_state("act")
                sceptile.set_state("act")

    current_time = pygame.time.get_ticks()

    # Clear custom messages after duration
    if battle_ui.custom_message and current_time - message_timer >= message_duration:
        battle_ui.clear_message()

    if not enemy_intro_played and current_time - start_time >= 1000:
        rayquaza.set_state("act")
        pygame.mixer.Sound("src/assets/sounds/pokemon_sounds/rayquaza.ogg").play()
        enemy_intro_played = True

    if not player_intro_played and current_time - start_time >= 2500:
        sceptile.set_state("act")
        pygame.mixer.Sound("src/assets/sounds/pokemon_sounds/sceptile.ogg").play()
        player_intro_played = True

    screen.blit(pygame.transform.scale(pygame.image.load("src/assets/sprites/battle_ui/arena/00.png"), (SCREEN_WIDTH, SCREEN_HEIGHT - 190)), (0,0))  # Fill the screen with white
    
    enemy_x = SCREEN_WIDTH - 410
    enemy_y = SCREEN_HEIGHT - 620

    playermon_x = SCREEN_WIDTH - 570
    playermon_y = SCREEN_HEIGHT - 350
    playermon, cur_x, cur_y = sceptile.animate(screen, playermon_x, playermon_y)
    enemymon, cur_x2, cur_y2 = rayquaza.animate(screen, enemy_x, enemy_y)

    if playermon:
        overlay.draw("player", screen, playermon, cur_x, cur_y)
    if enemymon:
        overlay.draw("enemy", screen, enemymon, cur_x2, cur_y2)

    battle_ui.draw()


    pygame.display.flip()
    clock.tick(14)  

pygame.quit()