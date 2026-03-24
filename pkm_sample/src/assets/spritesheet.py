import pygame

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert_alpha()

    def get_image(self, x, y, width, height):
        spritesheet = pygame.Surface((width, height)).convert_alpha()
        spritesheet.blit(self.sheet, (0, 0), (x, y, width, height))
        return spritesheet