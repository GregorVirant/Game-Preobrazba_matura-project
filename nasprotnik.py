import pygame
#ti podatki so v tabelah zato, ker je več tipov nasprotnikov
slikeNasprotniki = [pygame.image.load("slike/nasprotniki/duh4.png"),pygame.image.load("slike/nasprotniki/duh8.png")]
hitrostNasprotniki = [4,3]
zivljenjeNasprotniki = [50,70]

class Nasprotnik():
    def __init__(self,tip,sredinax,spodaj,maxPremik):
        self.slika = slikeNasprotniki[tip]
        self.slika =pygame.transform.flip(self.slika,True,False) #obrne sliko okoli y osi ker hocem da prvo v levo obrnjen
        self.sredinax = sredinax
        self.rect = self.slika.get_rect(centerx = sredinax,bottom=spodaj)
        self.maxZivljenje=zivljenjeNasprotniki[tip]
        self.zivljenje = zivljenjeNasprotniki[tip]
        self.premikx = 0
        self.premikaDesno = -1*hitrostNasprotniki[tip]  #prvo se premnika v levo zato *1
        self.maxPremik = maxPremik #najvecji premik za katerega se lahko nasprotnik premakne
        #da so bolj prozorni
        self.slika.fill((255, 255, 255, 130), None, pygame.BLEND_RGBA_MULT)

    def skoda(self,st):
        self.zivljenje-=st
    def draw(self,ekran,x,y):
        #narise sliko nasprotnika
        ekran.blit(self.slika,((self.rect.left-x,self.rect.top-y),self.rect.size))  
    def premik(self):
        #ce nima hitrosti 0 se premakne preveri tudi ce more zamenjat smer
        if self.maxPremik == 0:
            return
        if abs(self.premikx + self.premikaDesno)>self.maxPremik:
            #se obrne
            self.premikaDesno=-self.premikaDesno
            self.slika =pygame.transform.flip(self.slika,True,False)
        self.premikx+=self.premikaDesno
        self.rect.centerx = self.sredinax + self.premikx
