import pygame
from pygame.locals import *
import time

class Pipe:
    def __init__(self,parent_screen):
        self.image = pygame.image.load("resources/pipe.png")
        self.image = pygame.transform.scale(self.image,(52,510))
        self.parent_screen = parent_screen

    def draw(self,x,y):
        self.parent_screen.blit(self.image,(x,y))
        reverseImg=pygame.transform.flip(self.image,False,True)
        self.parent_screen.blit(reverseImg,(x,y+640))
        pygame.display.update()


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Flappy Bird Game");
        self.surface = pygame.display.set_mode((580,850))
        self.surface.fill((0,0,0))
        self.pipe = Pipe(self.surface)
        
        

    def render_background(self):
        bg= pygame.image.load("resources/bg.png")
        bg= pygame.transform.scale(bg,(580,850))
        self.surface.blit(bg,(0,0))

    def render_base(self):
        base = pygame.image.load("resources/base.png")
        base= pygame.transform.scale(base,(580,170))
        self.surface.blit(base,(0,680))

    def play(self):
        self.render_background()
        self.pipe.draw(240,0);
        self.pipe.draw(320,-460)
        self.render_base()
        pygame.display.update()

    def show_game_over(self):
        self.render_background()
        pygame.display.update()

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type== QUIT:
                    running=False

            try:
                if not pause:
                    self.play()
                    pause=True
            except Exception as e:
                print(e)
                pause= True


if __name__=="__main__":
    game= Game()
    game.run()