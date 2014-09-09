import pygame
import time
import os
import sys
import random


pygame.init()
size = (800,600)

pos_x = 1366/2 - size[0]/2
pos_y = 768 - 700

os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (pos_x,pos_y)
os.environ['SDL_VIDEO_CENTERED'] = '0'

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong")

font = pygame.font.SysFont("Press Start 2P",30,False,False)

clock = pygame.time.Clock()


class SFX():
    def __init__(self):
        self.contact = pygame.mixer.Sound("contact.wav")
        self.out = pygame.mixer.Sound("out.ogg")
        self.gloom = pygame.mixer.Sound("gloom.wav")
        self.gloat = pygame.mixer.Sound("gloat.wav")
        self.cheer = pygame.mixer.Sound("cheer.wav")

class Image(pygame.sprite.Sprite):
    def __init__(self, image,x,y):
        super(Image,self).__init__()
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.x_speed = 1
        self.y_speed = 1
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def render(self):
        screen.blit(self.image,(self.x+self.dx,self.y+self.dy))


ball = Image("ball.png",0,0)
l_paddle = Image("paddle.png",10,250)
r_paddle = Image("paddle.png",780,250)
sfx = SFX()

def main():

    score_pc = 0
    score_player = 0

    setup_screen(score_pc,score_player)

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    r_paddle.dy = -6
                if event.key == pygame.K_DOWN:
                    r_paddle.dy = 6
            if event.type == pygame.KEYUP :
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    r_paddle.dy = 0

        screen.fill(0x000000,(0,90,800,600))
        blit_scores(score_pc,score_player)

        if ball.y > 580:
            sfx.contact.play(loops=0,maxtime=0)
            time.sleep(0.04)
            ball.y_speed = ball.y_speed *-1
        if ball.y < 100:
            sfx.contact.play(loops=0,maxtime=0)
            time.sleep(0.04)
            ball.y_speed = ball.y_speed *-1

        if l_paddle.y + 30 < ball.y:
            l_paddle.dy = l_paddle.y_speed*3
        elif  l_paddle.y + 30 > ball.y:
            l_paddle.dy = -(l_paddle.y_speed*3)
        else:
            l_paddle.dy = 0

        if 100 <= r_paddle.y + r_paddle.dy <= 513:
            r_paddle.y += r_paddle.dy

        if 100 <= l_paddle.y + l_paddle.dy <= 513:
            l_paddle.y += l_paddle.dy

        l_paddle.render()
        r_paddle.render()
        ball.render()

        clock.tick(100)
        pygame.display.flip()

        x2,y2 = ball.x - l_paddle.x, ball.y - l_paddle.y
        x1,y1 = ball.x - r_paddle.x, ball.y - r_paddle.y


        if ball.x > r_paddle.x:
            sfx.out.play(loops=0,maxtime=0)
            score_pc += 1
            setup_screen(score_pc,score_player)

        elif ball.x < l_paddle.x:
            sfx.out.play(loops=0,maxtime=0)
            time.sleep(0.04)
            score_player += 1
            setup_screen(score_pc,score_player)

        elif r_paddle.mask.overlap(ball.mask,(x1,y1)):
            sfx.contact.play(loops=0,maxtime=0)
            time.sleep(0.04)
            ball.x_speed = -1*ball.x_speed
            ball.dy = random.random()+random.randrange(-3,3)

        elif l_paddle.mask.overlap(ball.mask,(x2,y2)):
            sfx.contact.play(loops=0,maxtime=0)
            ball.x_speed = -1*ball.x_speed
            ball.dy = random.random()+random.randrange(-3,3)

        ball.y = ball.y+ball.y_speed*2
        ball.x = ball.x+ball.x_speed*2


    return 0

def blit_scores(score_pc,score_player):
    text = font.render(str(score_pc),True,(200,0,100))
    screen.blit(text,(157,60))
    text2 = font.render(str(score_player),True,(200,0,100))
    screen.blit(text2,(530,60))

def setup_screen(score_pc,score_player):
    ball.x,ball.y = 800/2-32/2, 600/2-50/2
    if notOver(score_pc, score_player):
        screen.fill((165,200,207),[0,0,800,100])
        screen.fill((0,0,0),[0,90,800,600])
        blit_scores(score_pc,score_player)
        ball.render()
        l_paddle.render()
        r_paddle.render()
        name = font.render("PLAYER",True,(200,0,100))
        pc = font.render("PC",True,(200,0,100))
        screen.blit(pc,(150,10))
        screen.blit(name,(500,10))
        pygame.display.flip()
        time.sleep(1)

def notOver(score_pc, score_player):
    if score_pc == 10:
        pass

    return True

if __name__ == "__main__":
    sys.exit(main())
