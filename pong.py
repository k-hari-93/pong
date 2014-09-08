import pygame
import time
import os
import sys

class Image(pygame.sprite.Sprite):
    def __init__(self, image):
        super(Image,self).__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()

    def render(self,screen,x,y):
        screen.blit(self.image,(x,y))

def main():

    pygame.init()
    size = (800,600)

    pos_x = 1366/2 - size[0]/2
    pos_y = 768 - 700

    os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (pos_x,pos_y)
    os.environ['SDL_VIDEO_CENTERED'] = '0'

    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Pong")

    clock = pygame.time.Clock()

    ball = Image("ball.png")
    l_paddle = Image("paddle.png")
    r_paddle = Image("paddle.png")

    l_paddle_x,l_paddle_y = 10,250
    r_paddle_x,r_paddle_y = 780,250
    ball_x,ball_y = 100,100

    move_paddle_r = 0
    move_paddle_l = 0

    score_pc = 0
    score_player = 0

    speed = 1
    ball_x_speed = 1
    ball_y_speed = 1

    font = pygame.font.SysFont("Times New Roman",20,False,False)

    ball_x,ball_y = setup_screen(screen,font,ball,l_paddle,r_paddle,score_pc,score_player)

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move_paddle_r = -6
                if event.key == pygame.K_DOWN:
                    move_paddle_r = 6
            if event.type == pygame.KEYUP :
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    move_paddle_r = 0

        screen.fill(0x000000,(0,90,800,600))
        blit_scores(screen,font,score_pc,score_player)

        ball_y = ball_y+ball_y_speed*2
        ball_x = ball_x+ball_x_speed*2

        if ball_y > 580:
            ball_y_speed = ball_y_speed *-1
        if ball_y < 100:
            ball_y_speed = ball_y_speed *-1

        if l_paddle_y + 30 < ball_y:
            move_paddle_l = speed*3
        elif  l_paddle_y + 30 > ball_y:
            move_paddle_l = -(speed*3)
        else:
            move_paddle_l = 0

        if 100 <= r_paddle_y + move_paddle_r <= 513:
            r_paddle_y += move_paddle_r

        if 100 <= l_paddle_y + move_paddle_l <= 513:
            l_paddle_y += move_paddle_l

        l_paddle.render(screen,l_paddle_x,l_paddle_y)
        r_paddle.render(screen,r_paddle_x,r_paddle_y)
        ball.render(screen,ball_x,ball_y)

        clock.tick(60)
        pygame.display.flip()

        if 770<ball_x<790 and r_paddle_y < ball_y and ball_y+64<r_paddle_y+128:
            ball_x_speed = -1*ball_x_speed

        elif 0<ball_x<20 and l_paddle_y < ball_y and ball_y+64<l_paddle_y+128:
            ball_x_speed = -1*ball_x_speed

        if ball_x >= 800:
            score_pc += 1
            ball_x,ball_y = setup_screen(screen,font,ball,l_paddle,r_paddle,score_pc,score_player)

        if ball_x <= 0 :
            score_player += 1
            ball_x,ball_y = setup_screen(screen,font,ball,l_paddle,r_paddle,score_pc,score_player)

    return 0

def blit_scores(screen,font,score_pc,score_player):
    text = font.render(str(score_pc),True,(200,0,100))
    screen.blit(text,(157,60))
    text2 = font.render(str(score_player),True,(200,0,100))
    screen.blit(text2,(530,60))

def setup_screen(screen,font,ball,l_paddle,r_paddle,score_pc,score_player):
    x,y = 800/2-32/2, 600/2-50/2
    screen.fill((165,200,207),[0,0,800,100])
    screen.fill((0,0,0),[0,90,800,600])
    blit_scores(screen,font,score_pc,score_player)
    ball.render(screen,x,y)
    l_paddle.render(screen,10,250)
    r_paddle.render(screen,780,250)
    name = font.render("PLAYER",True,(200,0,100))
    pc = font.render("PC",True,(200,0,100))
    screen.blit(pc,(150,10))
    screen.blit(name,(500,10))
    pygame.display.flip()
    return x,y

if __name__ == "__main__":
    sys.exit(main())
