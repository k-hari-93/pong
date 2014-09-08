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

    paddle_group = pygame.sprite.Group()

    paddle_group.add(l_paddle)
    paddle_group.add(r_paddle)

    l_paddle_x,l_paddle_y = 10,10
    r_paddle_x,r_paddle_y = 780,10
    ball_x,ball_y = 100,100

    move_paddle_r = 0
    move_paddle_l = 0

    score = 0

    speed = 1
    ball_x_speed = 1
    ball_y_speed = 1

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move_paddle_r = -3
                if event.key == pygame.K_DOWN:
                    move_paddle_r = 3
            if event.type == pygame.KEYUP :
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    move_paddle_r = 0

        screen.fill(0x000000)

        ball_y = ball_y+ball_y_speed*2
        ball_x = ball_x+ball_x_speed*2

        if ball_y > 580:
            ball_y_speed = ball_y_speed *-1
        if ball_y < 10:
            ball_y_speed = ball_y_speed *-1


        if l_paddle_y + 30 < ball_y:
            move_paddle_l = speed*3
        elif  l_paddle_y + 30 > ball_y:
            move_paddle_l = -(speed*3)
        else:
            move_paddle_l = 0

        if 10 <= r_paddle_y + move_paddle_r <= 513:
            r_paddle_y += move_paddle_r
        if 10 <= l_paddle_y + move_paddle_l <= 513:
            l_paddle_y += move_paddle_l

        l_paddle.render(screen,l_paddle_x,l_paddle_y)
        r_paddle.render(screen,r_paddle_x,r_paddle_y)
        ball.render(screen,ball_x,ball_y)

        clock.tick(60)
        pygame.display.flip()


        l_paddle.rect = l_paddle.image.get_rect(center = (l_paddle_x,l_paddle_y))
        r_paddle.rect = r_paddle.image.get_rect(center = (r_paddle_x,r_paddle_y))
        ball.rect = ball.image.get_rect(center = (ball_x,ball_y))

        if pygame.sprite.spritecollideany(ball,paddle_group):
            if abs(r_paddle_x-ball_x)<3:
                ball_x_speed = -1*ball_x_speed
                continue
            if abs(l_paddle_x-ball_x)<3:
                ball_x_speed = -1*ball_x_speed

    return 0

if __name__ == "__main__":
    sys.exit(main())
