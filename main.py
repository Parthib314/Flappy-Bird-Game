import pygame
from pygame.locals import *
import time

class Bird:

    MAX_ROTATION = 25
    ANIMATION_TIME = 5
    ROT_VEL = 20
    IMGS=[pygame.transform.scale2x(pygame.image.load("resources/bird1.png")),
          pygame.transform.scale2x(pygame.image.load("resources/bird2.png")),
          pygame.transform.scale2x(pygame.image.load("resources/bird3.png"))]

    def __init__(self,parent_screen,x,y):
        self.parent_screen = parent_screen
        self.x=x
        self.y=y
        self.tilt= 0 #Degrees to tilt
        self.tick_count = 0
        self.vel = 0 
        self.height = self.y
        self.img_count  = 0
        self.img = self.IMGS[1]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        # For Downword Acceleration
        displacement = self.vel*(self.tick_count) + 0.5*(3)*(self.tick_count)**2 #Calculate Displacement

        # Terminal velocity
        if displacement >= 16:
            displacement = (displacement/abs(displacement)) * 16

        if displacement < 0:
            displacement -=2

        self.y = self.y + displacement

        if displacement<0 or self.y<self.height + 50:  #tilt up
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
            else:  #tilt down
                if self.tilt > -90:
                    self.tilt -= self.ROT_VEL

    def draw(self,x,y):
        self.img_count+=1
        
        if self.img_count <=self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count <= self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count<=self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count<=self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count==self.ANIMATION_TIME*4 + 1:
            self.img= self.IMGS[0]
            self.img_count =0

        # so when the bird is nose diving it isn't flapping:
        if self.tilt<=-80:
            self.img= self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2


        # Tilt the Bird
        blitRotateCenter(self.parent_screen,self.img,(self.x,self.y),self.tilt)

    def get_mask(self):
        #Gets the mask for the current image of the bird
        return pygame.mask.from_surface(self.img)  

class Pipe:
    def __init__(self,parent_screen):
        self.image = pygame.image.load("resources/pipe.png")
        self.image = pygame.transform.scale(self.image,(70,510))
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
        self.bird = Bird(self.surface)
        
        

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
        self.bird.draw(100,240)
        # self.pipe.draw(320,-460)
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