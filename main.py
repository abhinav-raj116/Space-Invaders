import pygame
import random

# Intialize the pygame
pygame.init()

# Create the Screen
width = 800
height = 600
screen = pygame.display.set_mode((width, height))

# Title and Icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# PLayer (SpaceShip)
playerImg = pygame.image.load('player.png')
playerX = 368
playerY = 400
player_width = 64
player_height = 64
playerX_change = 0
playerY_change = 0
player_rate = 0.3

# Enemy
enemyImg = pygame.image.load('enemy1.png')
enemy_width = 64
enemy_height = 64
# Allow enemy to appear at random position
enemyX = random.randint(0, width - enemy_width)
enemyY = random.randint(0, 100)
enemyX_change = 0
enemyY_change = 0
enemy_rate = 0.3


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y):
    screen.blit(enemyImg, (enemyX, enemyY))


def boundary(x, y):
    if x <= 0:
        x = 0
    elif x >= (width - player_width):
        x = width - player_width
    if y <= 0:
        y = 0
    elif y >= (height - player_height):
        y = height - player_height


# Game loop
running = True
while running:
    # Background color
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # SpaceShip Movement
        # Key press
        if event.type == pygame.KEYDOWN:
            # UP arrow key
            if event.key == pygame.K_UP:
                playerY_change = -player_rate
            # DOWN arrow key
            elif event.key == pygame.K_DOWN:
                playerY_change = player_rate
            # LEFT arrow key
            if event.key == pygame.K_LEFT:
                playerX_change = -player_rate
            # RIGHT arrow key
            elif event.key == pygame.K_RIGHT:
                playerX_change = player_rate
        # Key release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    # Moving spaceship
    playerX += playerX_change
    playerY += playerY_change

    # Defining Boundary to avoid the spaceship from moving out of the screen
    if playerX <= 0:
        playerX = 0
    elif playerX >= (width - player_width):
        playerX = width - player_width
    if playerY <= 0:
        playerY = 0
    elif playerY >= (height - player_height):
        playerY = height - player_height

    # Drawing the player and enemy on the screen
    player(playerX, playerY)
    enemy(enemyX, enemyY)

    # Update screen
    pygame.display.update()
