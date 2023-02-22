import pygame
from pygame.locals import *
import time
import random

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
    GAP = 200
    VEL= 5
    PIPE_IMG = pygame.transform.scale2x(pygame.image.load("resources/pipe.png"))

    def __init__(self,parent_screen,x):
        self.PIPE_TOP= pygame.transform.flip(self.PIPE_IMG,False,True);
        self.PIPE_BOTTOM = self.PIPE_IMG
        self.parent_screen = parent_screen
        self.x= x
        self.height= 0
        self.top = 0
        self.bottom=0
        self.passed = False
        self.set_height();
        
    def set_height(self):
        self.height = random.randrange(50,450);
        self.top = self.height- self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP;
    
    def move(self):
        self.x -= self.VEL

    def draw(self):
        self.parent_screen.blit(self.PIPE_TOP,(self.x,self.top))
        self.parent_screen.blit(self.PIPE_BOTTOM,(self.x,self.bottom))

    def collide(self,bird):
        bird_mask = bird.get_mask();
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        top_offset = (self.x-bird.x,self.top-round(bird.y))
        bottom_offset = (self.x-bird.x,self.bottom-round(bird.y))

        b_point = bird_mask.overlap(bottom_mask,bottom_offset)
        t_point = bird_mask.overlap(top_mask,top_offset)

        if b_point or t_point:
            return True
        
        return False
    
class Base:
    VEL = 5
    IMG= pygame.image.load("resources/base.png")
    WIDTH= IMG.get_width()

    def __init__(self,parent_screen,y):
        self.y= y
        self.x1 = 0
        self.x2 = self.WIDTH
        self.parent_screen = parent_screen

    def move(self):
        self.x1-= self.VEL
        self.x2-=self.VEL
        if self.x1 + self.WIDTH<0:
            self.x1=self.x2 + self.WIDTH

        if self.x2 + self.WIDTH<0:
            self.x2=self.x1 + self.WIDTH

    def draw(self):
        self.parent_screen(self.IMG,(self.x1,self.y))
        self.parent_screen(self.IMG,(self.x2,self.y))

def blitRotateCenter(surf,image,topleft,angle):
    rotated_image = pygame.transform.rotate(image,angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft= topleft).center)
    surf.blit(rotated_image,new_rect.topleft)

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