import pygame
import priprava
#za gumbe na meniju
class Gumb():
    def __init__(self,x,y,slika):             
        self.slika = slika
        self.rect = self.slika.get_rect()
        self.rect.center = (x,y)
    def draw(self,scr):
        #narise
        scr.blit(self.slika,self.rect)
    def pritisnjen(self):
        #preveri ce gumb pritisnjen
        pos = pygame.mouse.get_pos()
        #pac preveri ce se pozicija miske stika z gumbom sam mora bit ta pozicija se prej pomnozena z razmerjem velikosti povrsine ekran in velikosti zaslona
        if self.rect.collidepoint((pos[0]*priprava.ekranSirina/priprava.screen_width,pos[1]*priprava.ekranVisina/priprava.screen_height)) and  pygame.mouse.get_pressed()[0] == 1:
            return True
        return False
