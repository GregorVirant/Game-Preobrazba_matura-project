from priprava import * 
import gumb
import barve
escSpuscen=False
#nalozi slike
menuOkvir = pygame.image.load("slike/menu/menuOkvir.png").convert_alpha()
menuOkvirMali = pygame.image.load("slike/menu/menuOkvirMali2.png").convert_alpha()
igraj_slika = pygame.image.load("slike/menu/igraj.png").convert()
zapri_slika = pygame.image.load("slike/menu/zapri.png").convert()
ponovi_slika = pygame.image.load("slike/menu/ponovi.png").convert()
plus_slika = pygame.image.load("slike/menu/plus.png").convert()
minus_slika = pygame.image.load("slike/menu/minus.png").convert()
meni_slika = pygame.image.load("slike/menu/meni.png").convert()
zvok_slika = pygame.image.load("slike/menu/zvok2.png").convert_alpha()
navodilaZaIgro_slika = pygame.image.load("slike/menu/navodilaZaIgro5.png").convert_alpha()
naslovnica1 = pygame.image.load("slike/naslovnica1.png").convert()
#pripravi zvok za klik na gumb
zvokKlik = pygame.mixer.Sound("music/menu/select-sound-121244.mp3")
zvokKlik.set_volume(pygame.mixer.music.get_volume())


def glavniMeni():
    #pripravi novo povrsino na kiro se bo risal glavni meni
    ekranMeni=pygame.Surface(ekranVelikost)
    #narise ozadje
    n1=pygame.transform.scale(naslovnica1,ekran.get_size())
    ekranMeni.blit(n1,(0,0))
    #pripravi okvir, ki narisan okoli gumbov
    okvir  = menuOkvirMali.get_rect(x=ekranVelikost[0]/2-150,y=400)
    #pripravi gumbe
    igraj = gumb.Gumb(okvir.centerx,okvir.top+80,igraj_slika)
    zapri = gumb.Gumb(okvir.centerx,okvir.top+180,zapri_slika)

    #narise gumbe in okvir
    ekranMeni.blit(menuOkvirMali,okvir)    
    igraj.draw(ekranMeni)
    zapri.draw(ekranMeni)

    #na zaslon narise to povrsine na katero so bile prej narisane stvari in zaslon osvezi
    ekranGlavni.blit(pygame.transform.scale(ekranMeni,ekranGlavni.get_size()),(0,0))
    pygame.display.update()
    #pripravi novo zanko, ki bo gledala ce kak gumb pritisnjen
    run = True
    #uporabniku pokaze misko
    pygame.mouse.set_visible(True)
    #dovolji spreminjanje tega parametra zunaj metode
    global escSpuscen
    zePritisnjen = True
    while(run):
        zvokKlik.set_volume(pygame.mixer.music.get_volume())
        #to mora bit da zanka v PyGame sploh deluje
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        #ce pritisnemo zapri in se vrne True, kar nato v glavni zanki igro zapre
        if zapri.pritisnjen():
            #ne dovoljimo to ko ce je ze bil prej pritisnjen, ko ce pritisnemo gumb
            #meni v tiste meniju v igri in je pozicija miska iste kot je ta gumb zdaj
            #se se nekaj casa (dokler ne spustimo) steje, kot da drzimo ta gumb
            if not zePritisnjen:
                zvokKlik.play()
                return True
        #ce pritisnemo gumb pritisnjen se vrnemo v Igro
        elif igraj.pritisnjen():
            if not zePritisnjen:
                pygame.mouse.set_visible(False)
                zvokKlik.play()
                return False


            
        else:
            zePritisnjen = False

def meni():
    #priprava okvira in gumbov
    okvir  = menuOkvir.get_rect(x=ekranVelikost[0]/2-150,y=200)
    igraj = gumb.Gumb(okvir.centerx,okvir.top+100,igraj_slika)
    meni = gumb.Gumb(okvir.centerx,okvir.top+300,meni_slika)
    ponovi = gumb.Gumb(okvir.centerx,okvir.top+200,ponovi_slika)
    okvirZvok = pygame.rect.Rect(0,0,160,60)
    okvirZvok.center = (okvir.centerx,okvir.top+420)
    plus = gumb.Gumb(okvirZvok.left+30,okvirZvok.top+30,plus_slika)
    plus_pritisnjen=False
    minus = gumb.Gumb(okvirZvok.right-30,okvirZvok.top+30,minus_slika)
    minus_pritisnjen=False

    #nova povrsina ekranVelikost jo naredeimo skoraj prozorno 
    #narisemo na zaslon iz je igra v ozdju malce zatemnjena
    ozadje=pygame.Surface(ekranVelikost)
    ozadje.fill((0,40,60))
    ozadje.set_alpha(128)
    ekran.blit(ozadje,(0,0))

    
    #narisemo na povrsino ekran okvir, druge slike in gumbe
    ekran.blit(menuOkvir,okvir)
    ekran.blit(navodilaZaIgro_slika,(1100,500))
    ekran.blit(zvok_slika,(okvir.centerx-zvok_slika.get_width()/2,okvir.top+330))
    igraj.draw(ekran)
    meni.draw(ekran)
    ponovi.draw(ekran)
    plus.draw(ekran)
    minus.draw(ekran)
    #to nato narisemo na zaslon in osvezimo sliko
    ekranGlavni.blit(pygame.transform.scale(ekran,ekranGlavni.get_size()),(0,0))
    pygame.display.update()
    
    run = True
    pygame.mouse.set_visible(True)
    global escSpuscen
    #zanka, ki preverja ce gumbi pritisnjeni
    while(run):
        zvokKlik.set_volume(pygame.mixer.music.get_volume())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys=pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            if escSpuscen:
                escSpuscen=False
                pygame.mouse.set_visible(False)
                #vrne (False,False) se vrnemo v igro
                return (False,False)
        else:
            escSpuscen=True
        if igraj.pritisnjen():
            zvokKlik.play()
            pygame.mouse.set_visible(False)
            #vrne (False,False) se vrnemo v igro
            return (False,False)

        if meni.pritisnjen():
            zvokKlik.play()

            gM = glavniMeni()
            pygame.mouse.set_visible(False)
            #nas da na glavni meni
            return (gM,False)

        if ponovi.pritisnjen():
            zvokKlik.play()
            pygame.mouse.set_visible(False)
            #nas vrne na igro sam resetira stopnjo
            return (False,True)
        if plus.pritisnjen() and plus_pritisnjen == False:
            zvokKlik.play()
            plus_pritisnjen = True
            #poveca glsanost
            pygame.mixer.music.set_volume(pygame.mixer.music.get_volume()+0.05)
        if not plus.pritisnjen():
            plus_pritisnjen = False
        if minus.pritisnjen() and minus_pritisnjen == False:
            zvokKlik.play()
            minus_pritisnjen = True
            #zmanjsa glasnost
            glasnost = pygame.mixer.music.get_volume()
            if glasnost < 0.05:
                pygame.mixer.music.set_volume(0)
            else:
                pygame.mixer.music.set_volume(glasnost-0.05)
        if not minus.pritisnjen():
            minus_pritisnjen = False