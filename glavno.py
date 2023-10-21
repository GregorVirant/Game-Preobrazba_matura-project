from priprava import *
#takoj ob zagonu nalozi 1. level
nalozi_level()
import igralec, meni, math,sys

#metoda za risanje na ekran v kateri se rise skoraj vse
def narisiEkran():
    #narise ozadje
    ekran.blit(nebo,(0,0))
    #narise igralca
    igralec.draw()
    #narisejo se ovire
    for object,tip in objects:
        if tip ==-1:
            pygame.draw.rect(ekran,zelena,(object.left-igralec.x,object.top-igralec.y,object.width,object.height))
        elif tip ==-2:
            pygame.draw.rect(ekran,zlata,(object.left-igralec.x,object.top-igralec.y,object.width,object.height))
        else:
            #pri ovirah tipa 0 in 1 se vec manjsih slik 
            #sestavi tako da zapolnijo vecjo polje
            steviloSirina = math.ceil(object.width / slikeObjekti[tip].get_width())
            steviloVisina = math.ceil(object.height / slikeObjekti[tip].get_height())
            #gre tak da pac vse te manjse slike drugo zram druge narisem, da zgledajo kot ena vecja
            for i in range(0,steviloSirina):
                sub = slikeObjekti[tip].subsurface((0,0), (min(object.width,slikeObjekti[tip].get_width()),min(object.height,slikeObjekti[tip].get_height())))#object.size)

                for j in range(0,steviloVisina):
                    if i==steviloSirina-1 and j==steviloVisina-1:
                        sub = slikeObjekti[tip].subsurface((0,0),(object.width-slikeObjekti[tip].get_width()*i,object.height-slikeObjekti[tip].get_height()*j))
                    elif i == steviloSirina-1:
                        sub = slikeObjekti[tip].subsurface((0,0),(object.width-slikeObjekti[tip].get_width()*i,min(object.height,slikeObjekti[tip].get_height())))
                    elif j == steviloVisina-1:
                        sub = slikeObjekti[tip].subsurface((0,0),(min(object.width,slikeObjekti[tip].get_width()),object.height-slikeObjekti[tip].get_height()*j))
                    ekran.blit(sub,(object.left-igralec.x+slikeObjekti[tip].get_width()*i,object.top-igralec.y+slikeObjekti[tip].get_height()*j))
            #barva roba
            barveObjekti = [crna,temnoRdeca]
            #narise rob
            pygame.draw.rect(ekran,barveObjekti[tip],((object.left-igralec.x,object.top-igralec.y),object.size),7)          
    #narisejo se nasprotniki
    for i in range(len(nasprotniki)):
        nasprotniki[i].draw(ekran,igralec.x,igralec.y)
        #prikaz zivljenja nasprotnika
        dolzina = nasprotniki[i].rect.width #dolzina tega prikaza
        visina=25 #visina
        #ce nimajo max zivljenjas se prikaze
        if nasprotniki[i].zivljenje<nasprotniki[i].maxZivljenje:
            prikazZivljenja(nasprotniki[i].rect.centerx-igralec.x-dolzina/2,nasprotniki[i].rect.top-igralec.y-visina-10,dolzina,nasprotniki[i].maxZivljenje,nasprotniki[i].zivljenje,25)
    #meni igralcev nareto za splosno stevilo igralcev
    if len(igralec.igralci_za_uporabo)%2!=0: #pac loci na sodo pa liho tot pogoj je za liho
        #da pozicijo levega tja ko more bit
        x_meni_igralcev = ekranSirina//2 - 40-(len(igralec.igralci_za_uporabo)-1)//2*80
    else: #ce sodo 
        #pozicijo levega tja ko more bit ce sodo
        x_meni_igralcev = ekranSirina//2 - 80 - (len(igralec.igralci_za_uporabo)-1)//2*80
    #narise vse tote igralce za uporabo
    for i in range(len(igralec.igralci_za_uporabo)):
        textIgralec = pisava.render(f"{i+1}",True,rdeca) #pripravi stevilke ta tekst zram
        if igralec.igralci_za_uporabo[i] == igralec.igralec: #loci ce je izbran al ne
            ekran.blit(slikeIgralciMeniZbran[igralec.igralci_za_uporabo[i]-1],(x_meni_igralcev+i*80,ekranVisina-100))
        else:
            ekran.blit(slikeIgralciMeni[igralec.igralci_za_uporabo[i]-1],(x_meni_igralcev+i*80,ekranVisina-100))
        ekran.blit(textIgralec,(x_meni_igralcev+i*80,ekranVisina-100)) #narise stevilke za tekst zram

    textFps = pisava.render(f"FPS: {round(frames.get_fps())}",True,rdeca)
    ekran.blit(textFps,(10,0))

    #za prikaz zivljena
    prikazZivljenja(600,660,250,100,igralec.zivljenje)

    #narise in posodobi
    ekranGlavni.blit(pygame.transform.scale(ekran,ekranGlavni.get_size()),(0,0))
    pygame.display.update()
#ko na glavnem meniji kliknemo preveri ce je bil da zapremo igre ce ne nadaljuje
if meni.glavniMeni():
    pygame.quit()
    sys.exit()

def prikazZivljenja(x,y,dolzinaZivljenje,maxZivljenje,zivljenje,visina=30):
    #prikaztuje tisto vrstico za zivljenje
    slika_za_srce = slikaSrce
    naLevo=33
    if visina<30:
        slika_za_srce=slikaSrceNasp
        naLevo=26
    razmerjeZivljenje = dolzinaZivljenje/maxZivljenje
    #narise sivo ozadje to ka predstavla max zivljenje
    pygame.draw.rect(ekran,(67, 67, 61),(x,y,dolzinaZivljenje,visina))
    #prek z rdeco to ka predstavlja trenutno zivljernje
    pygame.draw.rect(ekran,(254,54,68),(x,y,zivljenje*razmerjeZivljenje,visina))
    #rob
    pygame.draw.rect(ekran,crna,(x,y,dolzinaZivljenje,visina),6)
    #zram narise srcek
    ekran.blit(slika_za_srce,(x-naLevo,y-8))

pygame.mouse.set_visible(False)
frames = pygame.time.Clock()
#GLAVNA ZANKA
while teci:
    #omejen na 60 slik na sekundo
    frames.tick(60)
    #to pac more bit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           teci = False        
    #tu v keys shrani kiri gumbi pritisnjeni
    keys=pygame.key.get_pressed()
    #ce drzimo enter napademo ce lahka pa nimamo zaostzanka pac damo  napad na 20
    if (keys[pygame.K_RETURN] or keys[pygame.K_KP_ENTER]) and igralec.napad == 0 and igralec.lahkoNapada and igralec.napadZaostanek==0:
        igralec.napad = 20
        igralec.vertikalnaHitrost=0
    if igralec.napadZaostanek != 0:
        igralec.napadZaostanek-=1
    #ce napad vec od se mec vrti in se steje kot da napadamo
    if igralec.napad != 0:
        igralec.napad-=1
        igralec.rotiraj(9)
        if igralec.napad == 0:
            igralec.napadZaostanek = igralec.napadZaostanekMax
            igralec.rot = 0
            narisiEkran()
            continue
    #preveri ce zelimo menjat igralca in ce to lahko
    if keys[pygame.K_1] and igralec.igralec != 1 and not keys[pygame.K_2] and not keys[pygame.K_3]:
        #ga pac zamenja in narise
        igralec.spremeniIgralca(1)
        igralec.napad = 0
        igralec.rot = 0
        narisiEkran()
    #podobn ko za prejsnega
    elif keys[pygame.K_2] and igralec.igralec != 2 and not keys[pygame.K_3] and not keys[pygame.K_1]:
        igralec.spremeniIgralca(2)
        igralec.napad = 0
        igralec.rot = 0
        narisiEkran()
    #podobn ko za prejsnega
    elif keys[pygame.K_3] and igralec.igralec != 3 and not keys[pygame.K_1] and not keys[pygame.K_2]:
        igralec.spremeniIgralca(3)
        igralec.napad = 0
        igralec.rot = 0
        narisiEkran()
    #ce je kliknjena tipka Esc se odpre meni
    if keys[pygame.K_ESCAPE]:
        if meni.escSpuscen:
            meni.escSpuscen=False
            zapri, ponvoi = meni.meni()
            #prevermo ka je meni zelel
            if zapri:
                #ce smo hotl zaprt gremo vec iz glavne zanke
                break
            if ponvoi:
                #drugac nadaljujemo
                pygame.mixer.music.pause()
                igralec.restart()
    else:
        meni.escSpuscen = True
    #ce drcimo d in lahka gremo  se premaknemo desn
    if keys[pygame.K_d] and igralec.napad==0:
        igralec.hodiDesno()
    #ce drzan a in lahka gre levo se igralec premakne levo
    elif keys[pygame.K_a]and igralec.napad==0:
        igralec.hodiLevo()
    else:
        igralec.stevecHoje=-1
    #zmanjsa cas ko cakamo da lahka spet skocimo
    if igralec.zamudaSkoka>0:
        igralec.zamudaSkoka-=1
    #co drzimo skok in lahka skocimo skocimo
    if keys[pygame.K_SPACE] and igralec.napad == 0:
        igralec.skok()
    #ce mamo zogo in hodimo se vrti
    if igralec.igralec==3 and igralec.stevecHoje>0:
        igralec.rotiraj(4)
    #ce ne napadamo
    if igralec.napad==0:
        #poveca vertikalna hitrost
        igralec.vertikalnaHitrost+=1
        #metoda gravitacija v kiri ya kooridnati pristeje vertikalna hitrost
        igralec.gravitacija()
        #interakcije z ovirami
        igralec.interakcije()
    #interakcije z nasprotniki
    igralec.interkcijeNasprotniki()
    #ko nasprotniki hodijo
    for nasprotnik in nasprotniki:
        nasprotnik.premik()    
    #metoda za risanje na ekran
    narisiEkran()


pygame.quit()