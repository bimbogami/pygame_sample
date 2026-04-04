import pygame
from pygame.locals import *
import os 

pygame.init()

class pkmn_anim:
    def __init__(self, pkmn_spri):
        self.pokemon = pkmn_spri
        self.pokemon_idle = [
            pygame.image.load(f"src/assets/sprites/{self.pokemon}/idle/{self.pokemon}_0.png"),
            pygame.image.load(f"src/assets/sprites/{self.pokemon}/idle/{self.pokemon}_1.png"),
            pygame.image.load(f"src/assets/sprites/{self.pokemon}/idle/{self.pokemon}_2.png"),
            pygame.image.load(f"src/assets/sprites/{self.pokemon}/idle/{self.pokemon}_3.png"),
            pygame.image.load(f"src/assets/sprites/{self.pokemon}/idle/{self.pokemon}_4.png"),
            pygame.image.load(f"src/assets/sprites/{self.pokemon}/idle/{self.pokemon}_5.png"),
            pygame.image.load(f"src/assets/sprites/{self.pokemon}/idle/{self.pokemon}_6.png"),
            pygame.image.load(f"src/assets/sprites/{self.pokemon}/idle/{self.pokemon}_7.png"),
            pygame.image.load(f"src/assets/sprites/{self.pokemon}/idle/{self.pokemon}_8.png"),
            pygame.image.load(f"src/assets/sprites/{self.pokemon}/idle/{self.pokemon}_9.png"),
            pygame.image.load(f"src/assets/sprites/{self.pokemon}/idle/{self.pokemon}_10.png"),
        ]
        self.pokemon_act = [
            pygame.image.load(f"src/assets/sprites/{self.pokemon}/act/{self.pokemon}_a_0.png"),
            pygame.image.load(f"src/assets/sprites/{self.pokemon}/act/{self.pokemon}_a_1.png"),
            pygame.image.load(f"src/assets/sprites/{self.pokemon}/act/{self.pokemon}_a_2.png"),
            pygame.image.load(f"src/assets/sprites/{self.pokemon}/act/{self.pokemon}_a_3.png"),
            pygame.image.load(f"src/assets/sprites/{self.pokemon}/act/{self.pokemon}_a_4.png"),
            pygame.image.load(f"src/assets/sprites/{self.pokemon}/act/{self.pokemon}_a_5.png"),
            pygame.image.load(f"src/assets/sprites/{self.pokemon}/act/{self.pokemon}_a_6.png"),
            pygame.image.load(f"src/assets/sprites/{self.pokemon}/act/{self.pokemon}_a_7.png"),
            pygame.image.load(f"src/assets/sprites/{self.pokemon}/act/{self.pokemon}_a_8.png"),
            pygame.image.load(f"src/assets/sprites/{self.pokemon}/act/{self.pokemon}_a_9.png"),
            pygame.image.load(f"src/assets/sprites/{self.pokemon}/act/{self.pokemon}_b_0.png"),
            pygame.image.load(f"src/assets/sprites/{self.pokemon}/act/{self.pokemon}_b_1.png"),
            pygame.image.load(f"src/assets/sprites/{self.pokemon}/act/{self.pokemon}_b_2.png"),
            pygame.image.load(f"src/assets/sprites/{self.pokemon}/act/{self.pokemon}_b_3.png"),
            pygame.image.load(f"src/assets/sprites/{self.pokemon}/act/{self.pokemon}_b_4.png"),
            pygame.image.load(f"src/assets/sprites/{self.pokemon}/act/{self.pokemon}_b_5.png"),
            pygame.image.load(f"src/assets/sprites/{self.pokemon}/act/{self.pokemon}_b_6.png"),
            pygame.image.load(f"src/assets/sprites/{self.pokemon}/act/{self.pokemon}_b_7.png"),
            pygame.image.load(f"src/assets/sprites/{self.pokemon}/act/{self.pokemon}_b_8.png"),
            pygame.image.load(f"src/assets/sprites/{self.pokemon}/act/{self.pokemon}_b_9.png"),
            pygame.image.load(f"src/assets/sprites/{self.pokemon}/act/{self.pokemon}_c_0.png"),
            pygame.image.load(f"src/assets/sprites/{self.pokemon}/act/{self.pokemon}_c_1.png"),
            pygame.image.load(f"src/assets/sprites/{self.pokemon}/act/{self.pokemon}_c_2.png"),
            pygame.image.load(f"src/assets/sprites/{self.pokemon}/act/{self.pokemon}_c_3.png"),
            pygame.image.load(f"src/assets/sprites/{self.pokemon}/act/{self.pokemon}_c_4.png"),
            pygame.image.load(f"src/assets/sprites/{self.pokemon}/act/{self.pokemon}_c_5.png"),
            pygame.image.load(f"src/assets/sprites/{self.pokemon}/act/{self.pokemon}_c_6.png")
        ]

        self.clock = pygame.time.Clock()
        self.state = "idle"
        self.value = 0

    def animate(self, screen, x, y):
        if self.state == "act":
            image = self.pokemon_act[self.value]
            self.value += 1
            if self.value >= len(self.pokemon_act):
                self.state = "idle"
                self.value = 0
        else:
            image = self.pokemon_idle[self.value]
            self.value += 1
            if self.value >= len(self.pokemon_idle):
                self.value = 0
        
        image = pygame.transform.scale(image, (image.get_width() * 2, image.get_height() * 2)).convert_alpha()
        image.set_colorkey((112, 154, 209))
        screen.blit(image, (x + (x - 400), y ))

    def set_state(self, state):
        if self.state != state:
            self.state = state
            self.value = 0



#class brendanbat:
#    def __init__(self):
#        self.frames = [
#            pygame.image.load("src/assets/sprites/brendan/start_battle/brendan_battle0.png"),
#            pygame.image.load("src/assets/sprites/brendan/start_battle/brendan_battle0.png"),
#            pygame.image.load("src/assets/sprites/brendan/start_battle/brendan_battle0.png"),
#            pygame.image.load("src/assets/sprites/brendan/start_battle/brendan_battle0.png"),
#            pygame.image.load("src/assets/sprites/brendan/start_battle/brendan_battle0.png"),
#            pygame.image.load("src/assets/sprites/brendan/start_battle/brendan_battle1.png"),
#            pygame.image.load("src/assets/sprites/brendan/start_battle/brendan_battle2.png"),
#            pygame.image.load("src/assets/sprites/brendan/start_battle/brendan_battle3.png"),
#            pygame.image.load("src/assets/sprites/brendan/start_battle/brendan_battle4.png"),
#            pygame.image.load("src/assets/sprites/brendan/start_battle/brendan_battle5.png"),
#            pygame.image.load("src/assets/sprites/brendan/start_battle/brendan_battle6.png"),
#            pygame.image.load("src/assets/sprites/brendan/start_battle/brendan_battle7.png"),
#            pygame.image.load("src/assets/sprites/brendan/start_battle/brendan_battle8.png"),
#            pygame.image.load("src/assets/sprites/brendan/start_battle/brendan_battle9.png"),
#            pygame.image.load("src/assets/sprites/brendan/start_battle/brendan_battle10.png")
#        ]
#        self.value = 0
#        self.last_update = pygame.time.get_ticks()
#        self.frame_delay = 150  # milliseconds per frame (increase to slow down)
        
        # Keep track of how much the character has moved
#        self.offset_x = 0 

        
#    def animate(self, screen, x, y):
#
#       
#        now = pygame.time.get_ticks()
        
        # Optional: For smooth movement every single tick (e.g. 2 pixels per frame), uncomment the line below
#        self.offset_x -= 3
        
#        if now - self.last_update >= self.frame_delay:
#            self.last_update = now
#            self.value += 1
#            if self.value == len(self.frames):
#                self.value = 0
                
#            self.offset_x -= 15

#        image = self.frames[self.value]
        
#        image = pygame.transform.scale(image, (image.get_width() * 2, image.get_height() * 2)).convert_alpha()
#        image.set_colorkey((255, 0, 228))
        
#        # Apply the offset to the base x position when drawing
#        screen.blit(image, (x + self.offset_x, y))