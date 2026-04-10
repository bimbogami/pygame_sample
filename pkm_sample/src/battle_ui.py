import pygame
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
font_path = os.path.join(BASE_DIR, "assets", "fonts", "pokemon-emerald.ttf")
moves_path = os.path.join(BASE_DIR, "assets", "json", "moves.json")
stat_path = os.path.join(BASE_DIR, "assets", "json", "stat.json")

class BattleUI:
    # Colors for each Pokemon type (base, hover)
    TYPE_COLORS = {
        "Normal":   ((168, 168, 120), (200, 200, 160)),
        "Fire":     ((240, 128,  48), (255, 170, 100)),
        "Water":    (( 104, 144, 240), (140, 175, 255)),
        "Grass":    (( 120, 200,  80), (160, 230, 120)),
        "Electric": ((248, 208,  48), (255, 230, 100)),
        "Ice":      ((152, 216, 216), (190, 235, 235)),
        "Fighting": ((192,  48,  40), (230,  90,  80)),
        "Poison":   ((160,  64, 160), (200, 110, 200)),
        "Ground":   ((224, 192, 104), (240, 215, 150)),
        "Flying":   ((168, 144, 240), (200, 180, 255)),
        "Psychic":  ((248,  88, 136), (255, 130, 170)),
        "Bug":      ((168, 184,  32), (200, 210,  80)),
        "Rock":     ((184, 160,  56), (215, 195, 100)),
        "Ghost":    ((112,  88, 152), (150, 125, 190)),
        "Dragon":   ((112,  56, 248), (155, 105, 255)),
        "Dark":     ((112,  88,  72), (155, 130, 110)),
        "Steel":    ((184, 184, 208), (210, 210, 230)),
        "Fairy":    ((238, 153, 172), (255, 190, 205)),
    }

    def __init__(self, screen, player_pokemon, enemy_pokemon):
        self.screen = screen
        self.player_pokemon = player_pokemon
        self.enemy_pokemon = enemy_pokemon
        self.mode = "main"  # "main" or "fight"
        self.custom_message = None
        pygame.font.init()
        self.font = pygame.font.Font(font_path, 40)
        self.small_font = pygame.font.Font(font_path, 24)
        self.hp_font = pygame.font.Font(font_path, 20)
        self.name_font = pygame.font.Font(font_path, 28)

        # Load JSON data
        with open(moves_path, "r", encoding="utf-8") as f:
            self.moves_data = json.load(f)
        with open(stat_path, "r", encoding="utf-8") as f:
            self.stat_data = json.load(f)

        # Calculate HP from stats
        self.player_max_hp = self._calc_max_hp(self.player_pokemon)
        self.player_hp = self.player_max_hp
        self.enemy_max_hp = self._calc_max_hp(self.enemy_pokemon)
        self.enemy_hp = self.enemy_max_hp

        # Stat stage tracking
        self.player_stat_stages = {}
        self.enemy_stat_stages = {}

        # Main menu buttons
        self.main_labels = ["Fight", "Pokémon", "Item", "Run"]
        self.main_colors = [
            (200, 50, 50),
            (50, 180, 50),
            (200, 150, 50),
            (50, 100, 200),
        ]
        self.main_hovers = [
            (255, 100, 100),
            (100, 230, 100),
            (255, 210, 100),
            (100, 150, 255),
        ]

    def _get_rects(self):
        """Build button rects based on current screen height."""
        ui_y = self.screen.get_height() - 190
        return [
            pygame.Rect(420, ui_y + 20, 185, 75),
            pygame.Rect(605, ui_y + 20, 185, 75),
            pygame.Rect(420, ui_y + 95, 185, 75),
            pygame.Rect(605, ui_y + 95, 185, 75),
        ]

    def _get_current_buttons(self):
        """Return (labels, colors, hovers) for the current mode."""
        if self.mode == "fight":
            moves = self.get_moves()
            # Pad to 4 if fewer moves
            while len(moves) < 4:
                moves.append("---")
            colors = []
            hovers = []
            for move_name in moves:
                details = self.get_move_details(move_name)
                mtype = details.get("type", "Normal")
                base, hover = self.TYPE_COLORS.get(mtype, ((168, 168, 120), (200, 200, 160)))
                colors.append(base)
                hovers.append(hover)
            return moves, colors, hovers
        else:
            return self.main_labels, self.main_colors, self.main_hovers

    def handle_event(self, event):
        """Check if a button was clicked. Returns (mode, label) or None."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            labels, _, _ = self._get_current_buttons()
            for label, rect in zip(labels, self._get_rects()):
                if rect.collidepoint(event.pos):
                    if self.mode == "main":
                        if label == "Fight":
                            self.mode = "fight"
                            return None  # just switched mode, no action yet
                        else:
                            return ("main", label)
                    elif self.mode == "fight":
                        if label == "---":
                            return None  # empty slot
                        self.mode = "main"  # go back to main after picking a move
                        return ("fight", label)
        return None

    def _calc_max_hp(self, pokemon_name, level=50):
        """Calculate max HP using the Pokemon formula at a given level."""
        stats = self._get_stats_for(pokemon_name)
        if not stats:
            return 100  # fallback
        base = stats["base_stats"]["hp"]
        iv = stats.get("ivs", {}).get("hp", 0)
        ev = stats.get("evs", {}).get("hp", 0)
        # Pokemon HP formula: ((2*Base + IV + EV/4) * Level / 100) + Level + 10
        hp = int(((2 * base + iv + ev / 4) * level / 100) + level + 10)
        return hp

    def _get_stats_for(self, pokemon_name):
        """Look up a pokemon's stat block by name."""
        for pkmn in self.stat_data.get("pokemon_roster", []):
            if pkmn["name"] == pokemon_name:
                return pkmn
        return None

    def _get_hp_color(self, current, maximum):
        """Return green/yellow/red based on HP percentage."""
        ratio = current / maximum if maximum > 0 else 0
        if ratio > 0.5:
            return (80, 200, 80)    # green
        elif ratio > 0.2:
            return (240, 200, 40)   # yellow
        else:
            return (220, 50, 50)    # red

    def _draw_hp_bar(self, x, y, width, current_hp, max_hp, name, show_hp_text=True, skew=20):
        """Draw a single HP bar inside a parallelogram background."""
        total_height = 55 if not show_hp_text else 75
        bar_height = 12
        bar_bg_color = (40, 40, 40)
        border_color = (80, 80, 80)
        hp_color = self._get_hp_color(current_hp, max_hp)
        ratio = max(0, current_hp / max_hp) if max_hp > 0 else 0
        padding = 12

        # Parallelogram background points
        # skew > 0 = leans right, skew < 0 = leans left
        para_points = [
            (x + skew, y),
            (x + width + skew, y),
            (x + width, y + total_height),
            (x, y + total_height)
        ]

        # Draw parallelogram shadow
        shadow_offset = 3
        shadow_points = [(px + shadow_offset, py + shadow_offset) for px, py in para_points]
        pygame.draw.polygon(self.screen, (20, 20, 20), shadow_points)

        # Draw parallelogram fill
        pygame.draw.polygon(self.screen, (48, 56, 65), para_points)
        # Draw parallelogram border
        pygame.draw.polygon(self.screen, (90, 100, 110), para_points, 3)

        # Inner content positions (offset by padding)
        # To avoid the slanted edge, use max(0, skew) as an offset
        inner_x = x + padding + max(0, skew)

        # Draw name
        name_surf = self.name_font.render(name, True, (255, 255, 255))
        self.screen.blit(name_surf, (inner_x, y + 6))

        bar_y = y + 34

        # "HP" label
        hp_label = self.hp_font.render("HP", True, (255, 210, 80))
        self.screen.blit(hp_label, (inner_x, bar_y - 2))

        bar_x = inner_x + 30
        # The usable width must account for the shape's full horizontal footprint
        bar_width = width - padding * 2 - abs(skew) - 30

        # Background
        pygame.draw.rect(self.screen, bar_bg_color, (bar_x, bar_y, bar_width, bar_height), border_radius=4)
        # Filled portion
        fill_width = int(bar_width * ratio)
        if fill_width > 0:
            pygame.draw.rect(self.screen, hp_color, (bar_x, bar_y, fill_width, bar_height), border_radius=4)
        # Border
        pygame.draw.rect(self.screen, border_color, (bar_x, bar_y, bar_width, bar_height), 2, border_radius=4)

        # HP text (e.g. "145 / 155")
        if show_hp_text:
            hp_text = self.hp_font.render(f"{current_hp} / {max_hp}", True, (220, 220, 220))
            text_rect = hp_text.get_rect(right=bar_x + bar_width, top=bar_y + 16)
            self.screen.blit(hp_text, text_rect)

    def draw_hp_bars(self):
        """Draw both HP bars on the arena."""
        # Enemy HP bar — top-left, parallelogram leans right
        self._draw_hp_bar(20, 30, 280, self.enemy_hp, self.enemy_max_hp, self.enemy_pokemon, show_hp_text=True, skew=25)

        # Player HP bar — right side, same shape as enemy, a bit wider
        ui_y = self.screen.get_height() - 190
        self._draw_hp_bar(460, ui_y - 85, 320, self.player_hp, self.player_max_hp, self.player_pokemon, show_hp_text=True, skew=25)

    def set_message(self, text):
        self.custom_message = text

    def clear_message(self):
        self.custom_message = None

    def _draw_text_wrapped(self, text, x, y, max_width, font, color=(255, 255, 255)):
        """Draw text wrapped to a max width."""
        words = text.split(' ')
        lines = []
        current_line = []
        for word in words:
            test_line = ' '.join(current_line + [word])
            width, _ = font.size(test_line)
            if width <= max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))

        y_offset = y
        for line in lines:
            line_surface = font.render(line, True, color)
            self.screen.blit(line_surface, (x, y_offset))
            y_offset += font.get_height() + 4

    def deal_damage(self, target, amount):
        """Deal damage to 'player' or 'enemy'. Clamps to 0."""
        if target == "player":
            self.player_hp = max(0, self.player_hp - amount)
        elif target == "enemy":
            self.enemy_hp = max(0, self.enemy_hp - amount)

    def apply_stat_change(self, target, changes):
        """Apply temporary stat stage changes."""
        target_dict = self.player_stat_stages if target == "player" else self.enemy_stat_stages
        for stat, stage in changes.items():
            current = target_dict.get(stat, 0)
            target_dict[stat] = max(-6, min(6, current + stage))

    def _draw_single_battery(self, x, y, stat, val):
        short_names = {
            "attack": "ATK", "defense": "DEF", 
            "special_attack": "SPA", "special_defense": "SPD", "speed": "SPE"
        }
        label = short_names.get(stat, stat[:3].upper())
        
        # Draw label
        label_surf = self.hp_font.render(label, True, (0, 0, 0))
        self.screen.blit(label_surf, (x, y))
        
        # Draw battery frame
        box_x = x + 40
        box_y = y + 2
        box_w = 15
        box_h = 15
        
        max_stages = 6
        color = (50, 200, 50) if val > 0 else (200, 50, 50)
        abs_val = abs(val)
        
        for i in range(max_stages):
            bx = box_x + i * (box_w + 2)
            pygame.draw.rect(self.screen, (40, 40, 40), (bx, box_y, box_w, box_h))
            if i < abs_val:
                pygame.draw.rect(self.screen, color, (bx, box_y, box_w, box_h))
            pygame.draw.rect(self.screen, (80, 80, 80), (bx, box_y, box_w, box_h), 1)

    def _draw_stat_bars(self):
        # Enemy (below HP bar)
        e_x, e_y = 60, 100
        for stat, val in self.enemy_stat_stages.items():
            if val != 0:
                self._draw_single_battery(e_x, e_y, stat, val)
                e_y += 20  # stack downwards
                
        # Player (above HP bar)
        ui_y = self.screen.get_height() - 190
        p_x, p_y = 500, ui_y - 115
        for stat, val in self.player_stat_stages.items():
            if val != 0:
                self._draw_single_battery(p_x, p_y, stat, val)
                p_y -= 20  # stack upwards

    def draw(self):
        # Draw HP bars on the arena (before the bottom panel)
        self.draw_hp_bars()
        self._draw_stat_bars()

        screen_h = self.screen.get_height()
        ui_y = screen_h - 190

        self.screen.fill((113, 169, 170), (0, ui_y, 800, 190))

        pygame.draw.rect(self.screen, (212, 85, 68), (10, ui_y + 10, 390, 170), border_radius=8)
        pygame.draw.rect(self.screen, (113, 169, 170), (15, ui_y + 15, 380, 160), border_radius=6)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        rects = self._get_rects()
        labels, colors, hovers = self._get_current_buttons()

        hovered_label = None

        for label, rect, base_col, hover_col in zip(labels, rects, colors, hovers):
            is_hovered = rect.collidepoint(mouse_x, mouse_y)
            color = hover_col if is_hovered else base_col

            pygame.draw.rect(self.screen, color, rect, border_radius=8)

            border_color = (max(0, base_col[0] - 50), max(0, base_col[1] - 50), max(0, base_col[2] - 50))

            if is_hovered:
                hovered_label = label
                pygame.draw.rect(self.screen, (255, 255, 255), rect, 3, border_radius=8)
            else:
                pygame.draw.rect(self.screen, border_color, rect, 3, border_radius=8)

            text_color = (30, 30, 30) if is_hovered else (255, 255, 255)

            if self.mode == "fight" and label != "---":
                # Show move name on top, type info below
                details = self.get_move_details(label)
                mtype = details.get("type", "")


                name_surf = self.small_font.render(label, True, text_color)

                name_rect = name_surf.get_rect(centerx=rect.centerx, centery=rect.centery - 12)

                self.screen.blit(name_surf, name_rect)
            else:
                text_surf = self.font.render(label, True, text_color)
                text_rect = text_surf.get_rect(center=rect.center)
                self.screen.blit(text_surf, text_rect)

        # Draw left placeholder text
        text_x = 30
        text_y = ui_y + 35
        text_w = 350
        
        if self.custom_message:
            self._draw_text_wrapped(self.custom_message, text_x, text_y, text_w, self.name_font)
        elif self.mode == "fight":
            if hovered_label and hovered_label != "---":
                details = self.get_move_details(hovered_label)
                desc = details.get("effects", {}).get("description", "No description available.")
                self._draw_text_wrapped(desc, text_x, text_y, text_w, self.name_font)
            else:
                self._draw_text_wrapped("Choose a move.", text_x, text_y + 20, text_w, self.name_font)
        else:
            self._draw_text_wrapped(f"What will  YOUR {self.player_pokemon} do?", text_x, text_y, text_w, self.font)

    def get_moves(self):
        """Get the move names for the current player pokemon."""
        movesets = self.moves_data.get("pokemon_movesets", {})
        return movesets.get(self.player_pokemon, [])

    def get_move_details(self, move_name):
        """Get full details of a move from the move database."""
        return self.moves_data.get("move_database", {}).get(move_name, {})

    def get_pokemon_stats(self, pokemon_name=None):
        """Get the stat block for a pokemon (defaults to player)."""
        name = pokemon_name or self.player_pokemon
        return self._get_stats_for(name)