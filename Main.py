import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()

# Display screen: width, height
screen = pygame.display.set_mode((800, 600))

# Load the backgrounds
backgroundSplash = pygame.image.load("Space background.bmp")
backgroundSpace = pygame.image.load("new.bmp")

# Load the sounds
mixer.music.load('Virtual World.wav')
mixer.music.play(-1)
soundExplosionA = mixer.Sound('Explosion.wav')
soundExplosionB = mixer.Sound('Explosion (2).wav')
laserSound = mixer.Sound('laserSound.wav')

# Title and Icon
pygame.display.set_caption('Lost in Space')
icon = pygame.image.load('UFO.png')
pygame.display.set_icon(icon)

# Game fonts
fontSplash = pygame.font.Font('freesansbold.ttf', 64)
fontScore = pygame.font.Font('freesansbold.ttf', 32)
fontGameOver = pygame.font.Font('freesansbold.ttf', 64)

# Load the laser images
laserImg = pygame.image.load('LASER.png')
laserX = 0
laserY = 480
laserYChange = -8
laserState = "Ready"

laser2Img = pygame.image.load('enemylaser.png')
laser2X = 0
laser2Y = 0
laser2YChange = 4
laser2State = "Ready"

# Player (blit means draw)
playerImg = pygame.image.load('spaceship.png')
playerX = 360
playerY = 490
playerXChange = 0

# Enemy lists
fireEnemy = []
enemyImg = []
enemyX = []
enemyY = []
enemyXChange = []
enemyYChange = []

# Set up the clock
clock = pygame.time.Clock()

def game_start():
    title = fontSplash.render("LOST IN SPACE", True, (255, 255, 255))
    screen.blit(title, (170, 250))
    text = fontScore.render("PRESS SPACE TO START", True, (255, 255, 255))
    screen.blit(text, (220, 350))


def game_over():
    over = True
    while over:
        txt_game_over = fontGameOver.render("GAME OVER", True, (255, 255, 255))
        screen.blit(txt_game_over, (200, 250))
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                over = False
                pygame.quit()
        pygame.display.update()


def fire_laser(x, y, laser_img):
    laserSound.set_volume(0.1)
    laserSound.play()
    screen.blit(laser_img, (x + 20, y))


def is_collision(ship_x, ship_y, laser_x, laser_y, distance_limit):
    distance = math.sqrt((math.pow(ship_x - laser_x, 2)) + (math.pow(ship_y - laser_y, 2)))
    if distance < distance_limit:
        laserSound.stop()
        explosion = random.randint(0, 1)
        if explosion == 1:
            soundExplosionB.play()
        else:
            soundExplosionA.play()
        return True
    else:
        return False


def level_start(level, win_score):
    level_title = fontSplash.render("LEVEL " + str(level), True, (255, 255, 255))
    screen.blit(level_title, (150, 250))
    txt_invite = fontScore.render("SCORE " + str(win_score) + " POINTS TO WIN", True, (255, 255, 255))
    screen.blit(txt_invite, (150, 350))


def level_complete(level):
    txt = fontSplash.render("LEVEL " + str(level) + " COMPLETE", True, (255, 255, 255))
    screen.blit(txt, (75, 250))


def show_score(score):
    score = fontScore.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score, (10, 10))


def move_player(x, y):
    screen.blit(playerImg, (x, y))


def move_enemy(x, y, index):
    screen.blit(enemyImg[index], (x, y))


def game_end():
    title = fontSplash.render("CONGRATULATIONS!", True, (255, 255, 255))
    screen.blit(title, (57, 250))


speedX = 3
speedY = 40
shipDistance = 50
laserDistance = 30

################################################################################################
# Setup for first level
################################################################################################
scoreValue = 0
numberEnemies = 12
maxLevelScore = 30

invite = True
while invite:
    screen.fill((0, 0, 0))
    screen.blit(backgroundSpace, (0, 0))
    game_start()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            invite = False

    pygame.display.update()

for i in range(numberEnemies):
    enemy_type = random.randint(0, 1)
    if enemy_type == 0:
        enemyImg.append(pygame.image.load('space-ship.png'))
    else:
        enemyImg.append(pygame.image.load('ufo (1).png'))
    enemyX.append(random.randint(0, 720))
    enemyY.append(random.randint(25, 100))
    speed = random.randint(-speedX, speedX)
    if speed == 0:
        speed = 1
    enemyXChange.append(speed)
    enemyYChange.append(random.randint(speedY, speedY + 10))


invite = True
while invite:
    screen.fill((0, 0, 0))
    screen.blit(backgroundSplash, (0, 0))
    level_start(1, maxLevelScore)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            invite = False

    pygame.display.update()

gameAlive = True
while gameAlive:
    clock.tick(90)
    # RGB color for the screen
    # screen.fill((115, 115, 115))
    screen.blit(backgroundSplash, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        # Player movement
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                playerXChange = -3

            if event.key == pygame.K_RIGHT:
                playerXChange = 3

            # Makes sure space only works once when the laser is 'ready'
            if event.key == pygame.K_SPACE and laserState == "Ready":
                laserX = playerX
                laserState = "Fire"
                fire_laser(laserX, laserY, laserImg)

        if event.type == pygame.KEYUP and (event.key == pygame.K_LEFT or pygame.K_RIGHT):
            playerXChange = 0

    playerX += playerXChange

    # boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= 740:
        playerX = 740

    for i in range(numberEnemies):
        enemyX[i] += enemyXChange[i]
        # Game over and enemy movement
        # if 440 < enemyY[i] < 600:
        #     for j in range(numberEnemies):
        #         enemyY[j] = 2000
        #         print("Game over")
        #         numberEnemies = 0
        #         game_over()
        collisionShip: bool = is_collision(enemyX[i], enemyY[i], playerX, playerY, shipDistance)
        if collisionShip:
            game_over()

        if enemyX[i] >= 730 or 0 >= enemyX[i]:
            enemyXChange[i] *= -1
            enemyY[i] += enemyYChange[i]

        # Collision
        if laserState == 'Fire':
            collisionFire: bool  = is_collision(enemyX[i], enemyY[i], laserX, laserY, laserDistance)
            if collisionFire:
                laserY = 480
                laserState = 'Ready'
                scoreValue += 1
                enemyX[i] = random.randint(0, 720)
                enemyY[i] = random.randint(25, 100)

        move_enemy(enemyX[i], enemyY[i], i)

    # Laser Movement
    if laserY <= 0:
        laserY = 480
        laserState = 'Ready'
    if laserState == "Fire":
        fire_laser(laserX, laserY, laserImg)
        laserY += laserYChange

    move_player(playerX, playerY)
    show_score(scoreValue)

    if scoreValue >= maxLevelScore:
        gameAlive = False

    pygame.display.update()

invite = True
while invite:
    screen.blit(backgroundSplash, (0, 0))
    level_complete(1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            invite = False

    pygame.display.update()

################################################################################################
# Setup for second level
################################################################################################

scoreValue = 0
numberEnemies = 50
maxLevelScore = 50

enemyImg.clear()
enemyX.clear()
enemyY.clear()
enemyXChange.clear()
enemyYChange.clear()

for i in range(numberEnemies):
    enemyImg.append(pygame.image.load('space-ship.png'))
    enemyX.append(random.randint(0, 720))
    enemyY.append(random.randint(25, 100))
    speed = random.randint(-speedX, speedX)
    if speed == 0:
        speed = 1
    enemyXChange.append(speed)
    enemyYChange.append(random.randint(speedY, speedY + 10))

invite = True
while invite:
    screen.blit(backgroundSplash, (0, 0))
    level_start(2, maxLevelScore)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            invite = False

    pygame.display.update()

gameAlive = True
while gameAlive:
    clock.tick(90)
    # RGB color for the screen
    # screen.fill((115, 115, 115))
    screen.blit(backgroundSplash, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        # Player movement
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                playerXChange = -3

            if event.key == pygame.K_RIGHT:
                playerXChange = 3

            if event.key == pygame.K_SPACE and laserState == "Ready":
                laserX = playerX
                laserState = "Fire"
                fire_laser(laserX, laserY, laserImg)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                playerXChange = 0

    playerX += playerXChange

    # boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= 740:
        playerX = 740

    for i in range(numberEnemies):
        enemyX[i] += enemyXChange[i]
        collisionShip: bool = is_collision(enemyX[i], enemyY[i], playerX, playerY, shipDistance)
        if collisionShip:
            game_over()

        if enemyX[i] >= 730 or enemyX[i] <= 0:
            enemyXChange[i] *= -1
            enemyY[i] += enemyYChange[i]

        # Collision
        collision = is_collision(enemyX[i], enemyY[i], laserX, laserY, laserDistance)
        if collision:
            laserY = 480
            laserState = 'Ready'
            scoreValue += 1

            enemyX[i] = random.randint(0, 720)
            enemyY[i] = random.randint(2000, 5000)

        move_enemy(enemyX[i], enemyY[i], i)

    # Laser Movement
    if laserY <= 0:
        laserY = 480
        laserState = 'Ready'
    if laserState == "Fire":
        fire_laser(laserX, laserY, laserImg)
        laserY += laserYChange

    move_player(playerX, playerY)
    show_score(scoreValue)

    if scoreValue >= maxLevelScore:
        gameAlive = False

    pygame.display.update()

invite = True
while invite:
    screen.blit(backgroundSplash, (0, 0))
    level_complete(2)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            invite = False

    pygame.display.update()

################################################################################################
# Setup for third level
################################################################################################

scoreValue = 0
numberEnemies = 25
maxLevelScore = 25

enemyImg.clear()
enemyX.clear()
enemyY.clear()
enemyXChange.clear()
enemyYChange.clear()

for i in range(numberEnemies):
    enemyImg.append(pygame.image.load('ufo (1).png'))
    enemyX.append(random.randint(0, 720))
    enemyY.append(random.randint(25, 100))
    speed = random.randint(-speedX, speedX)
    if speed == 0:
        speed = 1
    enemyXChange.append(speed)
    enemyYChange.append(random.randint(speedY, speedY + 10))

invite = True
while invite:
    screen.blit(backgroundSplash, (0, 0))
    level_start(3, maxLevelScore)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            invite = False

    pygame.display.update()
end = 0
timer = 0
gameAlive = True
while gameAlive:
    clock.tick(90)
    screen.blit(backgroundSplash, (0, 0))
    timer += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        # Player movement
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                playerXChange = -3

            if event.key == pygame.K_RIGHT:
                playerXChange = 3

            if event.key == pygame.K_SPACE and laserState == "Ready":
                laserX = playerX
                laserState = "Fire"
                fire_laser(laserX, laserY, laserImg)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                playerXChange = 0

    playerX += playerXChange

    # boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= 740:
        playerX = 740

    for i in range(numberEnemies):
        enemyX[i] += enemyXChange[i]
        collisionShip: bool = is_collision(enemyX[i], enemyY[i], playerX, playerY, shipDistance)
        if collisionShip:
            game_over()

        if enemyX[i] >= 730 or enemyX[i] <= 0:
            enemyXChange[i] *= -1
            enemyY[i] += enemyYChange[i]

        # Collision
        collision = is_collision(enemyX[i], enemyY[i], laserX, laserY, laserDistance)
        if collision:
            laserY = 480
            laserState = 'Ready'
            scoreValue += 1
            enemyX[i] = random.randint(0, 720)
            enemyY[i] = random.randint(2000, 5000)

        move_enemy(enemyX[i], enemyY[i], i)

    if laserY <= 0:
        laserY = 530
        laserState = 'Ready'
    if laserState == "Fire":
        fire_laser(laserX, laserY, laserImg)
        laserY += laserYChange

    if timer > 80 and laser2State == "Ready":
        timer = 0
        enemyFireIndex = random.randint(1, numberEnemies - 1)
        laser2X = enemyX[enemyFireIndex]
        laser2Y = enemyY[enemyFireIndex]
        laser2State = "Fire"
        fire_laser(laser2X, laser2Y, laser2Img)
        laserY += laserYChange

    if laser2Y >= 480:
        laser2Y = 0
        laser2State = 'Ready'

    if laser2State == 'Fire':
        fire_laser(laser2X, laser2Y, laser2Img)
        laser2Y += laser2YChange

        # Collision
        collision = is_collision(playerX, playerY, laser2X, laser2Y, laserDistance)
        if collision:
            end = 1

    move_player(playerX, playerY)
    show_score(scoreValue)

    if scoreValue >= maxLevelScore:
        gameAlive = False

    if end == 1:
        game_over()
        break
    pygame.display.update()

invite = True
while invite:
    screen.fill((0, 0, 0))
    screen.blit(backgroundSpace, (0, 0))
    game_end()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            invite = False

    pygame.display.update()
