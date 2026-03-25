import pygame
import os
import re
import math

class SimpleAnimator:
    def __init__(self, pkmn_name):
        self.pokemon = pkmn_name
        self.state = "idle"
        self.value = 0
        self.stat_update_state = None
        self.stat_anim_start_time = 0
        
        # Load frames dynamically
        self.pokemon_idle = self._load_frames(f"src/assets/sprites/{self.pokemon}/idle")
        self.pokemon_act = self._load_frames(f"src/assets/sprites/{self.pokemon}/act")

    def _natural_sort_key(self, s):
        # Sort files naturally (so rayquaza_10.png comes after rayquaza_2.png)
        return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

    def _load_frames(self, folder_path):
        frames = []
        try:
            if not os.path.exists(folder_path):
                print(f"Warning: Directory {folder_path} not found.")
                return frames
                
            filenames = [f for f in os.listdir(folder_path) if f.endswith('.png')]
            filenames.sort(key=self._natural_sort_key)
            
            for filename in filenames:
                file_path = os.path.join(folder_path, filename)
                image = pygame.image.load(file_path)
                frames.append(image)
        except Exception as e:
            print(f"Error loading frames from {folder_path}: {e}")
            
        return frames

    def animate(self, screen, x, y):
        # Handle "act" state
        if self.state == "act":
            if not self.pokemon_act:
                image = self.pokemon_idle[self.value] if self.pokemon_idle else None
            else:
                image = self.pokemon_act[self.value]
                self.value += 1
                if self.value >= len(self.pokemon_act):
                    self.state = "idle"
                    self.value = 0
        # Handle "idle" state
        else:
            if self.pokemon_idle:
                image = self.pokemon_idle[self.value]
                self.value += 1
                if self.value >= len(self.pokemon_idle):
                    self.value = 0
            else:
                image = None
        
        # Calculate bobbing if stat change is active
        bobbing_offset = 0
        if self.stat_update_state:
            t = pygame.time.get_ticks()
            # Run the bobbing animation for 1.5 seconds
            if t - self.stat_anim_start_time < 1500:
                if self.stat_update_state == "UP":
                    bobbing_offset = math.sin(t * 0.015) * 10
                elif self.stat_update_state == "DOWN":
                    bobbing_offset = -math.sin(t * 0.015) * 10
            else:
                self.stat_update_state = None

        # Draw the image
        if image:
            image = pygame.transform.scale(image, (image.get_width() * 2, image.get_height() * 2)).convert_alpha()
            image.set_colorkey((112, 154, 209))
            
            draw_x = x + (x - 400)
            draw_y = y + bobbing_offset
            
            screen.blit(image, (draw_x, draw_y))
            return image, draw_x, draw_y
            
        return None, 0, 0

    def draw(self, screen, x, y):
        # Alias for animate so older code still functions
        self.animate(screen, x, y)

    def set_state(self, state):
        if self.state != state:
            self.state = state
            self.value = 0


class OverlayAnimator:
    def __init__(self, screen=None):
        self.stat_update_state = None
        self.stat_anim_start_time = 0
        self.duration = 1500 # match SimpleAnimator duration
        
        self.img_up = None
        self.img_down = None
        try:
            self.img_up = pygame.image.load(os.path.join("src", "assets", "sprites", "StatUp.png")).convert_alpha()
        except Exception:
            pass
        try:
            self.img_down = pygame.image.load(os.path.join("src", "assets", "sprites", "StatDown.png")).convert_alpha()
        except Exception:
            pass

    def stats_change(self, stat_update):
        self.stat_update_state = stat_update
        self.stat_anim_start_time = pygame.time.get_ticks()

    def draw(self, screen, target_image, draw_x, draw_y):
        if not self.stat_update_state or not target_image:
            return

        t = pygame.time.get_ticks()
        elapsed = t - self.stat_anim_start_time
        if elapsed > self.duration:
            self.stat_update_state = None
            return

        # Calculate animation progress (0.0 to 1.0)
        progress = elapsed / self.duration
        
        # Smooth fade in and out for opacity (max ~200 so it looks like an overlay)
        alpha = int(200 * math.sin(progress * math.pi))

        overlay_img = self.img_up if self.stat_update_state == "UP" else self.img_down
        direction = -1 if self.stat_update_state == "UP" else 1

        width = target_image.get_width()
        height = target_image.get_height()

        # Create a temporary surface to hold the scrolling texture
        overlay_surf = pygame.Surface((width, height), pygame.SRCALPHA)

        if overlay_img:
            img_w = overlay_img.get_width()
            img_h = overlay_img.get_height()
            
            # Scale roughly to fit width
            scale_factor = width / img_w if img_w > 0 else 1
            new_h = int(img_h * scale_factor)
            
            if new_h > 0:
                scaled_img = pygame.transform.scale(overlay_img, (int(width), new_h))
                
                # Scroll it vertically 3 times over the duration
                cycles = 3
                if direction == -1: # Scroll UP -> y goes from positive to negative
                    y_offset = (1.0 - (progress * cycles) % 1.0) * new_h
                else: # Scroll DOWN -> y goes from negative to positive
                    y_offset = -new_h + ((progress * cycles) % 1.0) * new_h
                
                # Tile vertically to fill the sprite's box
                for tile_y in range(int(y_offset) - new_h, height, new_h):
                    overlay_surf.blit(scaled_img, (0, tile_y))

        # Use Pygame Mask to cut the overlay to EXACTLY the sprite's silhouette
        sprite_mask = pygame.mask.from_surface(target_image)
        # Create a silhouette shape that matches the target_image's content, containing our alpha fade
        mask_surf = sprite_mask.to_surface(setcolor=(255, 255, 255, alpha), unsetcolor=(0, 0, 0, 0))
        
        # Finally, map our moving overlay_surf ONLY onto the solid white sprite silhouette
        mask_surf.blit(overlay_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        # Draw the perfectly masked and tinted overlay exactly over the sprite!
        screen.blit(mask_surf, (draw_x, draw_y))
