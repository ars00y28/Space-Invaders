import pygame
from pygame import mixer
import random
import math 

pygame.init()


# create a screen
screen = pygame.display.set_mode((800, 600))

# title and logo
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# background image 
BackgroundImg = pygame.image.load('space.jpeg')


# player space ship
PlayerShip = pygame.image.load('spaceship.png')
NewSize = (64, 64)
ResizedPlayerShip = pygame.transform.scale(PlayerShip, NewSize)
PlayerX = 380
PlayerY = 480
PlayerX_Change = 0


def player(x, y):
    screen.blit(ResizedPlayerShip, (x, y))


# bullet
BulletImg = pygame.transform.scale((pygame.image.load('bullet.png')), (20, 20))
Bullet_FireState = False
BulletX = 380
BulletY = 480
BulletY_Change = 10




def FireBullet(x, y):
    global Bullet_FireState
    Bullet_FireState = True
    screen.blit(BulletImg, (x+16, y+10))


# enemy space ship
ResizedEnemyShip = []
EnemyX = []
EnemyY = []
EnemyX_Change = []
EnemyY_Change = []
EnemyNumber = 6

for i in range(EnemyNumber):
    ResizedEnemyShip.append(pygame.transform.scale(pygame.image.load('enemy.png'), (42,42))) 
    EnemyX.append(random.randint(0, 730))
    EnemyY.append(random.randint(50, 150)) 
    EnemyX_Change.append(0.5) 
    EnemyY_Change.append(40)

def enemy(x, y,i):
    screen.blit(ResizedEnemyShip[i], (x, y))

 
def IsCollision(EnemyX,EnemyY,BulletX,BulletY,):
    distance = math.sqrt((math.pow(EnemyX - BulletX,2))+(math.pow(EnemyY - BulletY,2)))
    if distance < 25:
        return True
    return False

# score 
ScoreValue = 0 
font = pygame.font.Font('freesansbold.ttf',32)
TextX = 10
TextY = 10

def ShowScore(x,y):
    global ScoreValue
    score = font.render('Score: '+ str(ScoreValue),True,(255,255,255))
    screen.blit(score,(x,y))

# game over 
GameOverFont = pygame.font.Font('freesansbold.ttf',64)

def GameOver():
    GameOverText = font.render(' GAME OVER !!! ',True,(255,255,255))
    screen.blit(GameOverText,(250,250))

# game loop
running = True
while running:
    screen.blit(BackgroundImg,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:  # key pressed
            # player movement
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                PlayerX_Change = -2
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                PlayerX_Change = 2
            # bullet
            if event.key == pygame.K_SPACE:
                if not Bullet_FireState:
                    BulletX = PlayerX
                    BulletY = PlayerY
                    FireBullet(BulletX, BulletY)
                    # bullet sound
                    BulletSound = mixer.music.load('laser.wav')
                    mixer.music.play()

        if event.type == pygame.KEYUP:  # key released
            PlayerX_Change = 0



    # enemy
    for i in range(EnemyNumber):
        # Game over 
        if EnemyY[i] > 480:
            for j in range(EnemyNumber):
                EnemyY[j] = 2000
                GameOver()
            break

        EnemyX[i] = EnemyX[i] + EnemyX_Change[i]
        if EnemyX[i] <= 0:
            EnemyX_Change[i] = 0.5
            EnemyY[i] = EnemyY[i] + EnemyY_Change[i]
        elif EnemyX[i] >= 738:
            EnemyX_Change[i] = -0.5
            EnemyY[i] = EnemyY[i] + EnemyY_Change[i]
        
            # check for collision 
        collision = IsCollision(EnemyX[i],EnemyY[i],BulletX,BulletY)
        if collision:
            CollisionSound = mixer.music.load('explosion.wav')
            mixer.music.play()
            ScoreValue += 1
            Bullet_FireState = False
            BulletY = 480
            EnemyX[i] = random.randint(0, 730)
            EnemyY[i] = random.randint(50, 150)
        
        enemy(EnemyX[i], EnemyY[i],i)

        # player
    PlayerX = PlayerX + PlayerX_Change
    if PlayerX <= 0:
        PlayerX = 0
    elif PlayerX >= 738:
        PlayerX = 738

        # bullet
    if BulletY <= 0:
        BulletY = 480
        Bullet_FireState = False

    if Bullet_FireState:
        FireBullet(BulletX, BulletY)
        BulletY -= BulletY_Change
    
    ShowScore(TextX,TextY)
    player(PlayerX, PlayerY)
    
    pygame.display.update()


