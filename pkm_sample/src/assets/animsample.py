# Importing the pygame module
import pygame
from pygame.locals import *

# Initiate pygame and give permission
# to use pygame's functionality
pygame.init()

# Create a display surface object
# of specific dimension
window = pygame.display.set_mode((900, 600))

pokemon = "rayquaza"
# Create a list of different sprites
# that you want to use in the animation
pokemon_idle = [pygame.image.load(f"assets/sprites/{pokemon}/idle/{pokemon}_idle-0.png"),
                pygame.image.load(f"assets/sprites/{pokemon}/idle/{pokemon}_idle-1.png"),
                pygame.image.load(f"assets/sprites/{pokemon}/idle/{pokemon}_idle-2.png"),
                pygame.image.load(f"assets/sprites/{pokemon}/idle/{pokemon}_idle-3.png"),
                pygame.image.load(f"assets/sprites/{pokemon}/idle/{pokemon}_idle-4.png"),
                pygame.image.load(f"assets/sprites/{pokemon}/idle/{pokemon}_idle-5.png"),
                pygame.image.load(f"assets/sprites/{pokemon}/idle/{pokemon}_idle-6.png"),
                pygame.image.load(f"assets/sprites/{pokemon}/idle/{pokemon}_idle-7.png"),
                pygame.image.load(f"assets/sprites/{pokemon}/idle/{pokemon}_idle-8.png"),
                pygame.image.load(f"assets/sprites/{pokemon}/idle/{pokemon}_idle-9.png")
                ]

pokemon_act = [ pygame.image.load(f"assets/sprites/{pokemon}/act/{pokemon}_act-0.png"),
                pygame.image.load(f"assets/sprites/{pokemon}/act/{pokemon}_act-1.png"),
                pygame.image.load(f"assets/sprites/{pokemon}/act/{pokemon}_act-2.png"),
                pygame.image.load(f"assets/sprites/{pokemon}/act/{pokemon}_act-3.png"),
                pygame.image.load(f"assets/sprites/{pokemon}/act/{pokemon}_act-4.png"),
                pygame.image.load(f"assets/sprites/{pokemon}/act/{pokemon}_act-5.png"),
                pygame.image.load(f"assets/sprites/{pokemon}/act/{pokemon}_act-6.png"),
                pygame.image.load(f"assets/sprites/{pokemon}/act/{pokemon}_act-7.png"),
                pygame.image.load(f"assets/sprites/{pokemon}/act/{pokemon}_act-8.png"),
                pygame.image.load(f"assets/sprites/{pokemon}/act/{pokemon}_act-9.png"),
                pygame.image.load(f"assets/sprites/{pokemon}/act/{pokemon}_act2-0.png"),
                pygame.image.load(f"assets/sprites/{pokemon}/act/{pokemon}_act2-1.png"),
                pygame.image.load(f"assets/sprites/{pokemon}/act/{pokemon}_act2-2.png"),
                pygame.image.load(f"assets/sprites/{pokemon}/act/{pokemon}_act2-3.png"),
                pygame.image.load(f"assets/sprites/{pokemon}/act/{pokemon}_act2-4.png"),
                pygame.image.load(f"assets/sprites/{pokemon}/act/{pokemon}_act2-5.png"),
                pygame.image.load(f"assets/sprites/{pokemon}/act/{pokemon}_act2-6.png"),
                pygame.image.load(f"assets/sprites/{pokemon}/act/{pokemon}_act2-7.png"),
                pygame.image.load(f"assets/sprites/{pokemon}/act/{pokemon}_act2-8.png"),
                pygame.image.load(f"assets/sprites/{pokemon}/act/{pokemon}_act2-9.png"),
                pygame.image.load(f"assets/sprites/{pokemon}/act/{pokemon}_act3-0.png"),
                pygame.image.load(f"assets/sprites/{pokemon}/act/{pokemon}_act3-1.png"),
                pygame.image.load(f"assets/sprites/{pokemon}/act/{pokemon}_act3-2.png"),
                pygame.image.load(f"assets/sprites/{pokemon}/act/{pokemon}_act3-3.png"),
                pygame.image.load(f"assets/sprites/{pokemon}/act/{pokemon}_act3-4.png"),
                pygame.image.load(f"assets/sprites/{pokemon}/act/{pokemon}_act3-5.png"),
                pygame.image.load(f"assets/sprites/{pokemon}/act/{pokemon}_act3-6.png")]
clock = pygame.time.Clock()

# Animation state: "idle" or "act"
state = "idle"
# Frame index for the current animation
value = 0

run = True

# Coordinates of the sprite
x = 100
y = 150

while run:

    # Setting the framerate to 10fps just
    # to see the result properly
    clock.tick(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()

        # When Space is pressed, switch to "act" animation
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if state != "act":        # avoid restarting mid-animation
                    state = "act"
                    value = 0             # start act from frame 0

    # Pick the right sprite list based on state
    if state == "act":
        image = pokemon_act[value]
        value += 1
        # Once act animation finishes, go back to idle
        if value >= len(pokemon_act):
            state = "idle"
            value = 0
    else:
        image = pokemon_idle[value]
        value += 1
        # Loop idle animation
        if value >= len(pokemon_idle):
            value = 0

    # Scale, remove background color, and draw
    image = pygame.transform.scale(image, (image.get_width() * 2, image.get_height() * 2)).convert_alpha()
    image.set_colorkey((112, 154, 209))
    window.fill((91, 189, 140))
    window.blit(image, (x, y))
    pygame.display.update()