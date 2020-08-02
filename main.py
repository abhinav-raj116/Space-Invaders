import pygame
import random
from math import sqrt
from pygame import mixer

# Intialize the pygame
pygame.init()

# Create the Screen
width = 800
height = 600
screen = pygame.display.set_mode((width, height))

# Load background image
bg = pygame.image.load('background.png')

# Background Music
mixer.music.load('background.wav')
mixer.music.play(-1)

# Explosion and Bullet Sound
explosion_sound = mixer.Sound('explosion.wav')
bullet_sound = mixer.Sound('laser.wav')

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
player_rate = 5

# Enemy
num_of_enemies = 6
enemy_width = 64
enemy_height = 64
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy1.png'))
    enemyX.append(random.randint(0, width - enemy_width))
    enemyY.append(random.randint(0, 100))
    enemyX_change.append(3)
    enemyY_change.append(25)

# Bullet
# 'ready' - bullet is not visible
# 'fire' - bullet is visible and moving
bulletImg = pygame.image.load('bullet.png')
bullet_width = 32
bullet_height = 32
bulletX = 368
bulletY = 400
# bulletX_change = 0
bulletY_change = 5
bullet_state = 'ready'

# Score
score = 0
scoreX = 10
scoreY = 10
font = pygame.font.Font('freesansbold.ttf', 32)

# GAME OVER
game_state = 'playing'
game_overX = 250
game_overY = 250
game_over_font = pygame.font.Font('freesansbold.ttf', 64)


def view_score(x, y):
    score_value = font.render(f'Score : {score}', True, (255, 255, 255))
    screen.blit(score_value, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, j):
    screen.blit(enemyImg[j], (x, y))


def fire(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y))


def is_collided(enemyX, enemyY, bulletX, bulletY, collision_distance=27):
    distance = sqrt((enemyX - bulletX) ** 2 + (enemyY - bulletY) ** 2)
    if distance < collision_distance:
        explosion_sound.play()
        return True
    return False


def game_over(x, y):
    game_over_text = game_over_font.render("GAME OVER!", True, (255, 255, 255))
    screen.blit(game_over_text, (x, y))


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

        # **************** SpaceShip Movement Detection ****************
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

            # ************************ Fire Bullet ******************************
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bulletX = playerX
                    bulletY = playerY
                    bullet_sound.play()
                    fire(bulletX, playerY)

        # Key release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    # ******************************* Moving spaceship *******************************
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

    # ****************************** Enemy Movement **********************************
    if game_state is 'playing':
        for i in range(num_of_enemies):
            # Moving enemy
            enemyX[i] += enemyX_change[i]

            # Defining boundary to avoid the ENEMY from moving out of the screen
            if (enemyX[i] <= 0) or (enemyX[i] >= (width - enemy_width)):
                enemyX_change[i] *= -1
                enemyY[i] += enemyY_change[i]
            # Respawn enemy if enemy moves beyond screen height
            if enemyY[i] >= height:
                enemyX[i] = random.randint(0, width - enemy_width)
                enemyY[i] = random.randint(0, 100)

            # ************************ Collision detection between bullet and enemy ***************************
            collision = is_collided(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision and bullet_state is 'fire':
                bullet_state = 'ready'
                score += 1
                bulletY = playerY
                enemyX[i] = random.randint(0, width - enemy_width)
                enemyY[i] = random.randint(0, 100)
                print(score)

            enemy(enemyX[i], enemyY[i], i)

            # ********************************** Game Over ****************************************
            spaceship_collision = is_collided(enemyX[i], enemyY[i], playerX, playerY, 50)
            if spaceship_collision:
                game_state = 'game over'
                for j in range(num_of_enemies):
                    enemyX_change[j] = 0
                    enemyY_change[j] = 0
                game_over(game_overX, game_overY)
                break

    # ************************** Moving Bullet ********************************
    if bulletY <= 0:
        bullet_state = 'ready'
    if bullet_state is 'fire':
        fire(bulletX, bulletY)
        bulletY -= bulletY_change

    # Drawing the player on the screen
    player(playerX, playerY)

    # Drawing score on the screen
    view_score(scoreX, scoreY)

    # Game Over
    if game_state is 'game over':
        for i in range(num_of_enemies):
            enemy(enemyX[i], enemyY[i], i)
        game_over(game_overX, game_overY)


    # Update screen
    pygame.display.update()
