import pygame
import random

# Intialize the pygame
pygame.init()

# Create the Screen
width = 800
height = 600
screen = pygame.display.set_mode((width, height))

# Load background image
bg = pygame.image.load('background.png')

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
player_rate = 3

# Enemy
enemyImg = pygame.image.load('enemy1.png')
enemy_width = 64
enemy_height = 64
enemyX = random.randint(0, width - enemy_width)  # Allow enemy to appear at random position
enemyY = random.randint(0, 100)
enemyX_change = 2
enemyY_change = 25

# Bullet
# Ready - bullet is not visible
# Fire - bullet is visible and moving
bulletImg = pygame.image.load('bullet.png')
bullet_width = 32
bullet_height = 32
bulletX = 0
bulletY = 400
bulletX_change = 0
bulletY_change = 10
bullet_state = 'ready'


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y):
    screen.blit(enemyImg, (enemyX, enemyY))


def fire(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y))


# Game loop
running = True
while running:
    # Background color
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(bg, (0, 0))
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
            if event.key == pygame.K_DOWN:
                playerY_change = player_rate
            # LEFT arrow key
            if event.key == pygame.K_LEFT:
                playerX_change = -player_rate
            # RIGHT arrow key
            if event.key == pygame.K_RIGHT:
                playerX_change = player_rate
            # Fire Bullet
            if event.key == pygame.K_SPACE:
                fire(playerX, playerY)
        # Key release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    # Moving spaceship
    playerX += playerX_change
    playerY += playerY_change

    # Defining boundary to avoid the SPACESHIP from moving out of the screen
    if playerX <= 0:
        playerX = 0
    elif playerX >= (width - player_width):
        playerX = width - player_width
    if playerY <= 0:
        playerY = 0
    elif playerY >= (height - player_height):
        playerY = height - player_height

    # Moving enemy
    enemyX += enemyX_change

    # Defining boundary to avoid the ENEMY from moving out of the screen
    if enemyX <= 0:
        enemyX_change *= -1
        enemyY += enemyY_change
    elif enemyX >= (width - enemy_width):
        enemyX_change *= -1
        enemyY += enemyY_change

    # Moving Bullet
    if bullet_state is 'fire':
        fire(playerX, bulletY)
        bulletY -= bulletY_change

    # Drawing the player and enemy on the screen
    player(playerX, playerY)
    enemy(enemyX, enemyY)

    # Update screen
    pygame.display.update()
