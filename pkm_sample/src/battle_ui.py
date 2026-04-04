import pygame
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
font_path = os.path.join(BASE_DIR, "assets", "fonts", "pokemon-emerald.ttf")

class BattleUI:
    def __init__(self, screen):
        self.screen = screen
        pygame.font.init()
        self.font = pygame.font.Font(font_path, 40)

    def draw(self):
        screen_h = self.screen.get_height()
        ui_y = screen_h - 190
        
        self.screen.fill((113, 169, 170), (0, ui_y, 800, 190))

        pygame.draw.rect(self.screen, (212, 85, 68), (10, ui_y + 10, 390, 170), border_radius=8)
        pygame.draw.rect(self.screen, (113, 169, 170), (15, ui_y + 15, 380, 160), border_radius=6)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        labels = ["Fight", "Pokémon", "Item", "Run"]
        rects = [
            pygame.Rect(420, ui_y + 20, 185, 75),
            pygame.Rect(605, ui_y + 20, 185, 75),
            pygame.Rect(420, ui_y + 95, 185, 75),
            pygame.Rect(605, ui_y + 95, 185, 75),
        ]
        colors = [
            (200, 50, 50),
            (50, 180, 50),
            (200, 150, 50),
            (50, 100, 200),
        ]
        hovers = [
            (255, 100, 100),
            (100, 230, 100),
            (255, 210, 100),
            (100, 150, 255),
        ]

        for label, rect, base_col, hover_col in zip(labels, rects, colors, hovers):
            is_hovered = rect.collidepoint(mouse_x, mouse_y)
            color = hover_col if is_hovered else base_col
            
            pygame.draw.rect(self.screen, color, rect, border_radius=8)
            
            border_color = (max(0, base_col[0] - 50), max(0, base_col[1] - 50), max(0, base_col[2] - 50))
            
            if is_hovered:
                pygame.draw.rect(self.screen, (255, 255, 255), rect, 3, border_radius=8)
            else:
                pygame.draw.rect(self.screen, border_color, rect, 3, border_radius=8)

            text_color = (30, 30, 30) if is_hovered else (255, 255, 255)
            text_surf = self.font.render(label, True, text_color)
            
            text_rect = text_surf.get_rect(center=rect.center)
            self.screen.blit(text_surf, text_rect)