import pygame
import random
from math import sqrt

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

# Player (SpaceShip)
playerImg = pygame.image.load('player.png')
playerX = 368
playerY = 400
player_width = 64
player_height = 64
playerX_change = 0
playerY_change = 0
player_rate = 2

# Enemy
enemyImg = pygame.image.load('enemy1.png')
enemy_width = 64
enemy_height = 64
enemyX = 0
enemyY = 0
enemyX_change = 2
enemyY_change = 25

# Bullet
# Ready - bullet is not visible
# Fire - bullet is visible and moving
bulletImg = pygame.image.load('bullet.png')
bullet_width = 32
bullet_height = 32
bulletX = 368
bulletY = 400
bulletX_change = 0  # Not goona use
bulletY_change = 5
bullet_state = 'ready'

score = 0

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y):
    screen.blit(enemyImg, (enemyX, enemyY))

# Spawn an enemy at a random location
def enemy_spawn():
    global enemyX
    global enemyY
    enemyX = random.randint(0, width - enemy_width)
    enemyY = random.randint(0, 100)


def fire(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y))


def is_collided(enemyX, enemyY, bulletX, bulletY):
    distance = sqrt((enemyX - bulletX) ** 2 + (enemyY - bulletY) ** 2)
    if distance < 27:
        return True
    return False


# Game loop
running = True
enemy_spawn()
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
                if bullet_state is 'ready':
                    bulletX = playerX
                    bulletY = playerY
                    fire(bulletX, playerY)
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
    if bulletY <= 0:
        bullet_state = 'ready'
    if bullet_state is 'fire':
        fire(bulletX, bulletY)
        bulletY -= bulletY_change

    # Collision detection
    collision = is_collided(enemyX, enemyY, bulletX, bulletY)
    if collision:
        bullet_state = 'ready'
        score += 1
        enemy_spawn()
        print(score)

    # Drawing the player and enemy on the screen
    player(playerX, playerY)
    enemy(enemyX, enemyY)

    # Update screen
    pygame.display.update()
