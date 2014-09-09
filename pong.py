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

font = pygame.font.SysFont("Times New Roman",30,False,False)
w_font = pygame.font.SysFont("Times New Roman",40,True,False)

welcome = w_font.render("@@@PONG@@@", True, (255,0,0))

difficulty = font.render("Select difficulty level...",True,(255,255,255))
beginner = font.render("Beginner",True,(255,255,255))
intermediate = font.render("Intermediate",True,(255,255,255))
advanced = font.render("Advanced",True,(255,255,255))

esc = font.render("Hit Esc To Quit......",True,(255,255,255))

name = font.render("PLAYER",True,(200,0,100))
pc = font.render("PC",True,(200,0,100))

winner_pc = w_font.render("PC Wins!!! Hit Return To Continue.....",True,(255,255,255))
winner_player = w_font.render("You Win!!! Hit Return To Continue.....",True,(255,255,255))

clock = pygame.time.Clock()


class SFX():
    def __init__(self):
        self.contact = pygame.mixer.Sound("contact.wav")
        self.out = pygame.mixer.Sound("out.ogg")
        self.gloom = pygame.mixer.Sound("gloom.wav")
        self.cheer = pygame.mixer.Sound("cheer.wav")
        self.intro = pygame.mixer.Sound("intro.wav")

class Image(pygame.sprite.Sprite):
    def __init__(self, image,x,y):
        super(Image,self).__init__()
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.x_speed = 1
        self.y_speed = 3
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def render(self,screen):
        screen.blit(self.image,(self.x+self.dx,self.y+self.dy))


ball = Image("ball.png",0,0)
l_paddle = Image("paddle.png",10,250)
r_paddle = Image("paddle.png",780,250)
sfx = SFX()

def main():

    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Pong")

    l_flag = 1
    r_flag = 1
    t_flag = 1
    b_flag = 1

    score_pc = 0
    score_player = 0

    display_start_screen(screen)

    setup_screen(screen,score_pc,score_player)

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    r_paddle.dy = -6
                if event.key == pygame.K_DOWN:
                    r_paddle.dy = 6
            if event.type == pygame.KEYUP :
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    r_paddle.dy = 0

        screen.fill(0x000000,(0,90,800,600))
        blit_scores(screen,score_pc,score_player)

        if ball.y > 580:
            if b_flag:
                b_flag = 0
                l_flag = 1
                r_flag = 1
                t_flag = 1
                sfx.contact.play(loops=0,maxtime=0)
                time.sleep(0.04)
                ball.y_speed = ball.y_speed *-1
        if ball.y < 100:
            if t_flag:
                l_flag = 1
                r_flag = 1
                t_flag = 0
                b_flag = 1
                sfx.contact.play(loops=0,maxtime=0)
                time.sleep(0.04)
                ball.y_speed = ball.y_speed *-1

        if l_paddle.y < ball.y :
            l_paddle.y_speed = 1
        elif l_paddle.y > ball.y :
            l_paddle.y_speed = -1

        if 100 <= l_paddle.y + l_paddle.dy*l_paddle.y_speed <= 523:
            l_paddle.y += l_paddle.dy*l_paddle.y_speed

        if 100 <= r_paddle.y + r_paddle.dy <= 523:
            r_paddle.y += r_paddle.dy

        ball.y = ball.y+ball.y_speed*2
        ball.x = ball.x+ball.x_speed*2

        l_paddle.render(screen)
        r_paddle.render(screen)
        ball.render(screen)

        x1,y1 = int(ball.x - r_paddle.x), int(ball.y - r_paddle.y)
        x2,y2 = int(ball.x - l_paddle.x), int(ball.y - l_paddle.y)

        if ball.x > r_paddle.x:
            r_paddle.dy = 0
            sfx.out.play(loops=0,maxtime=0)
            score_pc += 1
            blit_scores(screen,score_pc,score_player)
            if not_over(screen,score_pc,score_player):
                setup_screen(screen,score_pc,score_player)
            l_flag = 1
            r_flag = 1

        elif ball.x < l_paddle.x:
            sfx.out.play(loops=0,maxtime=0)
            time.sleep(0.04)
            score_player += 1
            blit_scores(screen,score_pc,score_player)
            if not_over(screen,score_pc,score_player):
                setup_screen(screen,score_pc,score_player)
            l_flag = 1
            r_flag = 1

        elif r_paddle.mask.overlap(ball.mask,(x1,y1)):
            if r_flag:
                r_flag = 0
                l_flag = 1
                ball.dx = 0
                ball.dy = 0
                sfx.contact.play(loops=0,maxtime=0)
                time.sleep(0.04)
                ball.x_speed = -1*ball.x_speed
                ball.dy = random.randrange(0,3)

        elif l_paddle.mask.overlap(ball.mask,(x2,y2)):
            if l_flag:
                l_flag = 0
                r_flag = 1
                ball.dx = 0
                ball.dy = 0
                sfx.contact.play(loops=0,maxtime=0)
                ball.x_speed = -1*ball.x_speed
                ball.dy = random.randrange(0,3)

        clock.tick(60)
        pygame.display.flip()

    return 0

def blit_scores(screen,score_pc,score_player):
    text = font.render(str(score_pc),True,(200,0,100))
    text2 = font.render(str(score_player),True,(200,0,100))
    screen.fill((165,200,207),[0,0,800,100])
    screen.fill((0,0,0),[0,90,800,600])
    screen.blit(pc,(150,10))
    screen.blit(name,(500,10))
    screen.blit(text,(157,60))
    screen.blit(text2,(530,60))

def setup_screen(screen,score_pc,score_player):
    ball.x,ball.y = 800/2-32/2, 600/2-50/2+30
    l_paddle.x,l_paddle.y = 10, 250
    r_paddle.x,r_paddle.y = 780,250
    blit_scores(screen,score_pc,score_player)
    ball.render(screen)
    l_paddle.render(screen)
    r_paddle.render(screen)
    pygame.display.flip()
    time.sleep(1)

def not_over(screen,score_pc, score_player):
    if score_pc == 10:
        game_over(screen,winner_pc,0)
        return False
    elif score_player == 10:
        game_over(screen,winner_player,1)
        return False
    else:
        return True

def game_over(screen,winner,flag):
    screen.fill((0,0,0))
    screen.blit(winner,(50,200))
    if flag:
        sfx.cheer.play()
    else:
        sfx.gloom.play()

    pygame.display.flip()
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    done = True

    if flag:
        sfx.cheer.stop()
    else:
        sfx.gloom.stop()

    main()
def display_start_screen(screen):
    sfx.intro.play(loops = -1)
    screen.fill((0,0,0))
    screen.blit(welcome,(250,20))
    screen.blit(difficulty,(20,300))
    screen.blit(beginner,(50,350))
    screen.blit(intermediate,(50,400))
    screen.blit(advanced,(50,450))
    screen.blit(esc,(500,550))
    pygame.display.flip()

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()

                if 50<=x<=160 and 353<=y<=383:
                    ball.x_speed = ball.y_speed = 2
                    l_paddle.dy = 3
                elif 50<=x<=196 and 405<=y<=429:
                    ball.x_speed = ball.y_speed = 3
                    l_paddle.dy = 5.5
                elif 50<=x<=168 and 453<=y<=479:
                    ball.x_speed = ball.y_speed = 4.5
                    l_paddle.dy = 8

                done = True
                sfx.intro.stop()

if __name__ == "__main__":
    main()
