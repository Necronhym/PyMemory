import pygame
from sys import exit
import random
from pygame import mixer

pygame.init()

#Window settings:
width = 600
height = 400
screen = pygame.display.set_mode((width, height))
screen.fill((255,235,255))
pygame.display.set_caption('Memory Game')

#Hide OG Mouse:
pygame.mouse.set_visible(False);

#Time stuff:
clock = pygame.time.Clock()
framerate = 60;

#Audio
#TODO This later
mixer.init()
card_sound = mixer.Sound("card.wav")


#Load assests and stuff:

#Mouse Pointer
mouse_surface = pygame.image.load('cursor.gif')
mouse_rect = mouse_surface.get_rect(topleft = (64,64))

#Cards:

cardf_surface = pygame.image.load('front.png')
cardf_surface = pygame.transform.scale(cardf_surface, (50, 80))
cardf_rect = cardf_surface.get_rect(topleft = (64,64))

cardb_surface = pygame.image.load('back.png')
cardb_surface = pygame.transform.scale(cardb_surface, (50, 80))
cardb_rect = cardb_surface.get_rect(topleft = (64,64))

#Table Pointer
table_surface = pygame.image.load('wood.jpg')
table_surface = pygame.transform.scale(table_surface, (600, 400))
table_rect = pygame.Rect(0, 0, width, height);

#Font
font = pygame.font.Font('symbols.ttf', 50)

class Card:
    w = 50
    h = 80

    flipped = False
    visible = True

    def __init__(self):
        self.card_rect = cardf_surface.get_rect(topleft = (0, 0))
   
    def getValue(self):
        return self.value

    def getRect(self):
        return self.card_rect

    def setValue(self, value):
        self.value = value
        self.icon = font.render(str(value), True, 'black')

    def setPos(self, x, y):
        self.x = x
        self.y = y
        self.card_rect.left = x
        self.card_rect.top = y

    def remove(self):
        if(self.visible):
            self.visible = False;

    def render(self):
        if(self.visible):
            if(self.flipped):
                screen.blit(cardf_surface, self.card_rect);
                screen.blit(self.icon, (self.x+10, self.y+14))
            else:
                screen.blit(cardb_surface, self.card_rect);

#Initialize cards
Cards = [];

z = 50
for j in range(3):
    for i in range(10):
        Cards.append(Card())
        Cards[-1].setPos((i)*55+25, z)
    z+=110

#Create array of paired values and randomize it
arr = []
for i in range(15):
        arr.append(i)  
        arr.append(i)
random.shuffle(arr)

#Map symbols to cards:
smb = 'acghmnopqrstuvwxyABCDEFGJKLNOPQRSTUVWXYZ'
for i, C in enumerate(Cards):
    C.setValue(smb[arr[i]])

#Keep track of flips:
flips = 0;
cmp = []
while True:

    #Update events:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONUP:
            for C in Cards:
                if pygame.Rect.collidepoint(C.getRect(), pygame.mouse.get_pos()) and not C.flipped and C.visible:
                    flips += 1
                    cmp.append(C)
                    if flips > 2:
                        if(cmp[0].value == cmp[1].value):
                            for Cb in Cards:
                                if Cb.value == cmp[0].value:
                                    Cb.visible = 0
                        for Ce in Cards:
                            Ce.flipped = False;
                            flips = 1
                        cmp = [];
                        cmp.append(C)
                    C.flipped = True;
                    card_sound.play()
    
    #GetMousePos
    mouse_rect.left, mouse_rect.top = pygame.mouse.get_pos();

    

    #Render elements
    

    #Draw table
    screen.blit(table_surface, table_rect);
    
    #Draw Cards:
    for C in Cards:
        C.render(); 
    

    #Draw Mouse
    screen.blit(mouse_surface, mouse_rect);
    
    #Update elements
    pygame.display.update()

    #Time
    clock.tick(framerate);
    
