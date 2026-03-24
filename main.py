import pygame
import sys

# --- Constants (Screen SHITS)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 120

# Colors (Constants)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 50, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)

# Physics part
GRAVITY = 0.2
PLAYER_SPEED = 4
JUMP_FORCE = -12
BULLET_SPEED = 10

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.change_x = 0
        self.change_y = 0
        self.facing_right = True # saan nakaharap si buddy
        self.on_ground = False

    def update(self, platforms):

        self.calc_grav()

        # Movement
        self.rect.x += self.change_x
        
        block_hit_list = pygame.sprite.spritecollide(self, platforms, False)
        for block in block_hit_list:
            if self.change_x > 0: # Moving right
                self.rect.right = block.rect.left
            elif self.change_x < 0: # Moving left
                self.rect.left = block.rect.right


        self.rect.y += self.change_y
        

        self.on_ground = False
        block_hit_list = pygame.sprite.spritecollide(self, platforms, False)
        for block in block_hit_list:
            if self.change_y > 0: 
                self.rect.bottom = block.rect.top
                self.change_y = 0
                self.on_ground = True
            elif self.change_y < 0: 
                self.rect.top = block.rect.bottom
                self.change_y = 0

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += GRAVITY

    def jump(self):
        if self.on_ground:
            self.change_y = JUMP_FORCE

    def go_left(self):
        self.change_x = -PLAYER_SPEED
        self.facing_right = False

    def go_right(self):
        self.change_x = PLAYER_SPEED
        self.facing_right = True

    def stop(self):
        self.change_x = 0

    def shoot(self):
        # generation ng bullet, kung nasaaan si player
        return Bullet(self.rect.centerx, self.rect.centery, self.facing_right)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, facing_right):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        # Bullet Velocity
        if facing_right:
            self.velocity = BULLET_SPEED
        else:
            self.velocity = -BULLET_SPEED

    def update(self):
        self.rect.x += self.velocity
        # Bulelt Cap
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# --- Main Game Setup ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer shooter")
clock = pygame.time.Clock()

# Sprites!!!!
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
bullets = pygame.sprite.Group()

## PLATFORMS
# Ground
plat1 = Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40)
# Floating ledges
plat2 = Platform(200, 490, 150, 20)
plat3 = Platform(500, 350, 150, 20)
plat4 = Platform(100, 250, 150, 20)

platforms.add(plat1, plat2, plat3, plat4)
all_sprites.add(plat1, plat2, plat3, plat4)

# PLAYER
player = Player(50, SCREEN_HEIGHT - 150)
all_sprites.add(player)

# keeping the game going on and on
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.go_left()
            if event.key == pygame.K_RIGHT:
                player.go_right()
            if event.key == pygame.K_UP:
                player.jump()
            if event.key == pygame.K_SPACE: # Shoot with SPACE
                bullet = player.shoot()
                bullets.add(bullet)
                all_sprites.add(bullet)
                

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and player.change_x < 0:
                player.stop()
            if event.key == pygame.K_RIGHT and player.change_x > 0:
                player.stop()

 #LOGIC
    player.update(platforms)
    bullets.update()

    # (TEST) Check if bullets hit platforms
    for bullet in bullets:
        if pygame.sprite.spritecollide(bullet, platforms, False):
            bullet.kill() # Destroy bullet on impact with a wall

    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
sys.exit()