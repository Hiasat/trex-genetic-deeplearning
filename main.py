import os
import pygame
import random
import numpy as np
import time as ti
import constant
import brain
from pygame import *

pygame.init()
pygame.font.init()

gameScreen = pygame.display.set_mode(constant.SCREEN_SIZE)
clock = pygame.time.Clock()
pygame.display.set_caption("T-Rex Genetic Deep learning")

FONT = pygame.font.SysFont('Comic Sans MS', 22)
START_FONT = pygame.font.SysFont('Comic Sans MS', 48)
def load_image(name,sizex=-1,sizey=-1,colorkey=None,):
    fullname = os.path.join('sprites', name)
    image = pygame.image.load(fullname)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    if sizex != -1 or sizey != -1:
        image = pygame.transform.scale(image, (sizex, sizey))
    return (image, image.get_rect())

def load_sprite_sheet(sheetname,nx,ny,scalex = -1,scaley = -1,colorkey = None,):
    fullname = os.path.join('sprites',sheetname)
    sheet = pygame.image.load(fullname)
    sheet = sheet.convert()
    sheet_rect = sheet.get_rect()
    sprites = []
    sizex = sheet_rect.width/nx
    sizey = sheet_rect.height/ny
    for i in range(0,ny):
        for j in range(0,nx):
            rect = pygame.Rect((j*sizex,i*sizey,sizex,sizey))
            image = pygame.Surface(rect.size)
            image = image.convert()
            image.blit(sheet,(0,0),rect)
            if colorkey is not None:
                if colorkey is -1:
                    colorkey = image.get_at((0,0))
                image.set_colorkey(colorkey,RLEACCEL)
            if scalex != -1 or scaley != -1:
                image = pygame.transform.scale(image,(scalex,scaley))
            sprites.append(image)
    sprite_rect = sprites[0].get_rect()
    return sprites,sprite_rect


class Dino():
    def __init__(self):
        self.images,self.rect = load_sprite_sheet('dino.png',5,1,constant.DINO_SIZE_X,constant.DINO_SIZE_Y,-1)
        self.rect.bottom = int(constant.GROUND_HEIGHT)
        self.rect.left = constant.WIDTH / 15
        self.image = self.images[0]
        self.isJumping = False
        self.isDead = False
        self.score = 0
        self.index = 0
        self.counter = 0
        self.jumps = 0
        self.jumpedOver = 0
        self.realScore = 0
        self.realIdx = 0
        self.movement = [0,0]
        self.jumpSpeed = 11.5
        self.stand_pos_width = self.rect.width
    def draw(self):
        gameScreen.blit(self.image, self.rect)
    def checkbounds(self):
        if self.rect.bottom > constant.GROUND_HEIGHT:
            self.rect.bottom = constant.GROUND_HEIGHT
            self.isJumping = False
    def update(self):
        if self.isJumping:
            self.movement[1] = self.movement[1] + constant.GRAVITY
        if self.isJumping:
            self.index = 0
        if self.counter % 5 == 0:
            self.index = (self.index + 1)%2 + 2
        if self.isDead:
            self.index = 4

        self.image = self.images[self.index]
        self.rect.width = self.stand_pos_width

        self.rect = self.rect.move(self.movement)
        self.checkbounds()

        if not self.isDead and self.counter % 7 == 6:
            self.score += 1
        self.counter = (self.counter + 1)
class Ground():
    def __init__(self,speed=-5):
        self.image,self.rect = load_image('ground.png',-1,-1,-1)
        self.image1,self.rect1 = load_image('ground.png',-1,-1,-1)
        self.rect.bottom = constant.HEIGHT
        self.rect1.bottom = constant.HEIGHT
        self.rect1.left = self.rect.right
        self.speed = speed

    def draw(self):
        gameScreen.blit(self.image,self.rect)
        gameScreen.blit(self.image1,self.rect1)

    def update(self):
        self.rect.left += self.speed
        self.rect1.left += self.speed
        if self.rect.right < 0:
            self.rect.left = self.rect1.right
        if self.rect1.right < 0:
            self.rect1.left = self.rect.right
class Cloud(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image,self.rect = load_image('cloud.png',int(90*30/42),30,-1)
        self.speed = 1
        self.rect.left = x
        self.rect.top = y
        self.movement = [-1*self.speed,0]

    def draw(self):
        gameScreen.blit(self.image,self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)
        if self.rect.right < 0:
            self.kill()

class Cactus(pygame.sprite.Sprite):
    def __init__(self,speed=5,sizex=-1,sizey=-1):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.images,self.rect = load_sprite_sheet('cacti-small.png',3,1,sizex,sizey,-1)
        self.rect.bottom = constant.GROUND_HEIGHT
        self.rect.left = constant.WIDTH + self.rect.width
        self.image = self.images[random.randrange(0,3)]
        self.movement = [-1*speed,0]

    def draw(self):
        gameScreen.blit(self.image,self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)
        if self.rect.right < 0:
            self.kill()

def jump_player(dino):
    if dino.rect.bottom == constant.GROUND_HEIGHT:
        dino.isJumping = True
        dino.jumps = dino.jumps + 1;
        dino.movement[1] = -1 * dino.jumpSpeed

def get_distance_to_next_obstacle(cacti):
    for c in cacti:
        return c.rect.left
    return 1000
def get_gap_of_next_obstacle(cacti):
    if len(cacti) < 2:
        return 1000
    prev = 0
    diff = 0
    for c in cacti:
        diff = c.rect.left-prev
        prev = c.rect.right
    return diff

def gameplay():
    global gamespeed
    global playersDino
    global highScore
    global startTime
    while True:
        gamespeed = 4
        gameOver = False
        playersDino = []
        for i in range(0, constant.NUMBER_OF_DINO):
            playersDino.append(Dino())
            playersDino[i].realIdx = i
        new_ground = Ground(-1 * gamespeed)
        counter = 0
        catc = pygame.sprite.Group()
        clouds = pygame.sprite.Group()
        Cactus.containers = catc
        Cloud.containers = clouds
        last_obstacle = pygame.sprite.Group()
        while not gameOver:
            ########################
            for player_index in range(0, constant.NUMBER_OF_DINO):
                player = playersDino[player_index]
                if player.isDead:
                    continue
                # obs_high = get_height_of_next_obstacle(cacti)
                # bird_heigh = 0  # 1000
                # y_pos = get_player_ypos(player)/100
                # obs_gap = get_gap_of_next_obstacle(cacti) / 500
                speed = gamespeed / 5
                obs_distance = get_distance_to_next_obstacle(catc) / 500
                network_input = np.array([[obs_distance, speed]])
                if (brain.jump(player_index, network_input)):
                    jump_player(player)
            ########################
            for c in catc:
                c.movement[0] = -1 * gamespeed
                for i in range(0, constant.NUMBER_OF_DINO):
                    if pygame.sprite.collide_mask(playersDino[i], c) and playersDino[i].isDead == False:
                        playersDino[i].isDead = True
            ########################
            if len(clouds) < 5 and random.randrange(0, 300) == 10:
                Cloud(constant.WIDTH, random.randrange(constant.HEIGHT / 5, constant.HEIGHT / 2))
            if len(catc) < 2:
                if len(catc) == 0:
                    last_obstacle.empty()
                    last_obstacle.add(Cactus(gamespeed, 40, 40))
                else:
                    for l in last_obstacle:
                        if l.rect.right < constant.WIDTH * 0.53 and random.randrange(0, 50) == 10:
                            for i in range(0, constant.NUMBER_OF_DINO):
                                if playersDino[i].isDead == False:
                                    playersDino[i].jumpedOver = playersDino[i].jumpedOver + 1
                            last_obstacle.empty()
                            last_obstacle.add(Cactus(gamespeed, 40, 40))
            ########################
            for i in range(0, constant.NUMBER_OF_DINO):
                playersDino[i].update()
            new_ground.update()
            catc.update()
            clouds.update()
            ####################
            gameScreen.fill(constant.BACKGROUND_COLOR)
            clouds.draw(gameScreen)
            new_ground.draw()
            catc.draw(gameScreen)
            for i in range(0, constant.NUMBER_OF_DINO):
                if playersDino[i].isDead == False:
                    playersDino[i].draw()
            #######################################
            currentScore = 0
            for i in range(0, constant.NUMBER_OF_DINO):
                if (playersDino[i].score > currentScore):
                    currentScore = playersDino[i].score
            currentScore = str(currentScore)
            currentScore = currentScore.rjust(6, '0')
            textsurface = FONT.render('Score: ' + currentScore, False, (0, 0, 0))
            gameScreen.blit(textsurface, (constant.WIDTH - 130, 10))
            textsurface = FONT.render('Hi-Score: ' + str(highScore), False, (0, 0, 0))
            gameScreen.blit(textsurface, (constant.WIDTH - 130, 25))
            textsurface = FONT.render('Generation: ' + str(brain.generation), False, (0, 0, 0))
            gameScreen.blit(textsurface, (constant.WIDTH - 130, 40))
            textsurface = FONT.render('Game Speed: ' + str(gamespeed), False, (0, 0, 0))
            gameScreen.blit(textsurface, (constant.WIDTH - 130, 55))
            current_time = ti.time() - startTime
            textsurface = FONT.render('Time: ' + ti.strftime('%H:%M:%S', ti.gmtime(current_time)), False, (0, 0, 0))
            gameScreen.blit(textsurface, (5, 5))
            dlft = 0
            for p in playersDino:
                if p.isDead == False:
                    dlft = dlft + 1
            textsurface = FONT.render('Dinosaur: ' + str(dlft) + "/" + str(constant.NUMBER_OF_DINO), False, (0, 0, 0))
            gameScreen.blit(textsurface, (5, 20))
            ####################

            pygame.display.update()
            restart_game = True
            for p in playersDino:
                if p.isDead == False:
                    restart_game = False
            if restart_game:
                gameOver = True
            if counter % 700 == 699 and gamespeed < 12:
                new_ground.speed -= 1
                gamespeed += 1
                # print("Increased game speed ", gamespeed)
            clock.tick(constant.FPS)
            counter = (counter + 1)
        if gameOver:
            currentScore = 0
            for i in range(0, constant.NUMBER_OF_DINO):
                if (playersDino[i].score > currentScore):
                    currentScore = playersDino[i].score
            if currentScore > highScore:
                highScore = currentScore
            brain.produce_new_generation(playersDino)

def introscreen():
    global highScore
    highScore = 0
    gameStart = False
    while not gameStart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    global startTime
                    startTime = ti.time()
                    gameStart = True
        gameScreen.fill(constant.BACKGROUND_COLOR)
        textsurface = START_FONT.render("PRESS SPACE TO START", False, (0, 0, 0))
        gameScreen.blit(textsurface, (100,constant.HEIGHT/2-10))
        pygame.display.update()
        clock.tick(constant.FPS)

def main():
    brain.init()
    isGameQuit = introscreen()
    if not isGameQuit:
        gameplay()


main()
