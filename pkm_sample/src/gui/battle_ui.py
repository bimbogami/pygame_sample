import pygame

class BattleUI:
    def __init__(self, screen):
        self.screen = screen

    def draw(self):
        pygame.draw.rect(self.screen, (255, 255, 0), (0, self.screen.get_height()-190, 800, 200))