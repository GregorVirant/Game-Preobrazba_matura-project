from turtle import width
import time
import pygame, os
from pygame.locals import *
import nasprotnik
from barve import *
import csv

#za glavno zanko 
teci = True
#PRIPRAVA GLAVNEGA EKRANA
pygame.init()
info = pygame.display.Info() 
screen_width,screen_height = info.current_w,info.current_h
ekranGlavni = pygame.display.set_mode((screen_width,screen_height),pygame.FULLSCREEN)
pygame.display.set_caption("Preobrazba")
pygame.mouse.set_visible(False)
#PRIPRAVA POVRSINE EKRAN
ekranVelikost = (1440,810)
ekranSirina,ekranVisina=ekranVelikost
ekran=pygame.Surface(ekranVelikost)
#NALAGANJE SLIK in PRIPRAVA NJIHOVIH PRAVOKOTNIKOV
nebo = pygame.image.load("slike/ozadje1.png").convert()
nebo=pygame.transform.scale(nebo,ekran.get_size())
slikaSmrt = pygame.image.load("slike/smrt1.png").convert()
slikaZmaga = pygame.image.load("slike/zmaga1.png").convert()
slikaZmagaZac = pygame.image.load("slike/zmagaZac.png").convert()
slikaStojiDesno = pygame.image.load("slike/igralci/mainStandT.png").convert_alpha()
slikaStojiLevo = pygame.image.load("slike/igralci/mainStandLT.png").convert_alpha()
slikeDesno=[pygame.image.load("slike/igralci/stickR1T.png").convert_alpha(),pygame.image.load("slike/igralci/stickR2T.png").convert_alpha(),pygame.image.load("slike/igralci/stickR3T.png").convert_alpha()]
slikeLevo=[pygame.image.load("slike/igralci/stickL1T.png").convert_alpha(),pygame.image.load("slike/igralci/stickL2T.png").convert_alpha(),pygame.image.load("slike/igralci/stickL3T.png").convert_alpha()]
slikeSkok=[pygame.image.load("slike/igralci/jump1T.png").convert_alpha(),pygame.image.load("slike/igralci/jump2T.png").convert_alpha()]
slikaMec = pygame.image.load("slike/igralci/D2.png").convert_alpha()
slikaZoga = pygame.image.load("slike/igralci/zoga2.png").convert_alpha()
slikeObjekti = [pygame.image.load("slike/opeka2.png").convert(),pygame.image.load("slike/lava.png").convert()]
slikeIgralciMeni = [pygame.image.load("slike/menuIgralci/menuIgralciStick.png").convert_alpha(),pygame.image.load("slike/menuIgralci/menuIgralciMec.png").convert_alpha(),pygame.image.load("slike/menuIgralci/menuIgralciZoga.png").convert_alpha()]
slikeIgralciMeniZbran = [pygame.image.load("slike/menuIgralci/menuIgralciStick1.png").convert_alpha(),pygame.image.load("slike/menuIgralci/menuIgralciMec1.png").convert_alpha(),pygame.image.load("slike/menuIgralci/menuIgralciZoga1.png").convert_alpha()]
slikaSrce=pygame.image.load("slike/srce7.png").convert_alpha()
slikaSrceNasp=pygame.image.load("slike/srceNasp.png").convert_alpha()

#TIPI OVIR: 1 bolec 0 navadni -1 zmaga -2 tocka za shranjevanje napredka
objects=[] #ovre (platforme)
nasprotniki=[]
maxLevel=4 #stevilo levelov
level = 1  #level, ki ga na zacetku nalozi

#NALOZI OBJEKTE in NASPROTNIKE za LEVEL
def nalozi_level():
    #izbrisemo prejsne shranjene ovire in nasprotnike
    objects.clear()
    nasprotniki.clear()
    with open(f'level/level{level}ovire.csv') as datoteka:
        branjeDatoteke = csv.DictReader(datoteka)
        for vrstica in branjeDatoteke:
            #tabeli se doda ti. tuplet v katerem je pravokotnik ovire in njen tip
            objects.append((pygame.Rect((int(vrstica["x"]),int(vrstica["y"])),(int(vrstica["sirina"]),int(vrstica["visina"]))),int(vrstica["tip"])))
    with open(f'level/level{level}nasprotniki.csv') as datoteka:
        branjeDatoteke = csv.DictReader(datoteka)
        for vrstica in branjeDatoteke:
            #tabeli se doda objekt tipa Nasprotnik
            nasprotniki.append(nasprotnik.Nasprotnik(int(vrstica["tip"]),
            int(vrstica["sredinax"]),int(vrstica["spodaj"]),int(vrstica["maxPremik"])))

#priprava pisave
pisava = pygame.font.SysFont(None, 48)


#pripravi se in predvaja se glasba, ki se ponavlja v neskoncnost
pygame.mixer.music.load("music/Risk.mp3")
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play(-1)#loop