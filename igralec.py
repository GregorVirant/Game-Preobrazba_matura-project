from priprava import *
import priprava
#poklice tudi datoteke za igralce iz mape igralci
import igralci.stick as st
import igralci.mec as m
import igralci.zoga as zo
import random

#pripravi spremenljivke za igralca
igralec = 1
x=0
y=0
vertikalnaHitrost=0
lahkoSkoci = True
usmerjenost = 1 
stevecHoje=-1 
zamudaSkoka=0
zivljenje=100
checkpointX=0
checkpointY=0
rot = 0
napadZaostanek = 0
napad = 0

igralci_za_uporabo = [1,2,3]

#stvari ki se razlikujejo glede na igralce se 
#nastavijo na vrednosti za osnovnega igralca
rect=st.rect
hitrost = st.hitrost
visinaSkoka = st.visinaSkoka
zamudaSkokaMax=st.zamudaSkokaMax
lahkoNapada = st.lahkoNapada
napadZaostanekMax = st.napadZaostanekMax

def draw():
    #poklice metodo za risanje ustreznega igralca
    global rect
    if igralec == 1:
        st.draw(lahkoSkoci,vertikalnaHitrost,stevecHoje,usmerjenost)
    if igralec == 2:
        rect = m.draw(slikaMec,rot)    
    if igralec == 3:
        zo.draw(rot)
def hodiDesno():
    #premaknemo se v desno 
    global x #tu global pomeni to da lahko spreminjamo vrednost te spremenljivke
    #x zunaj te metode
    global usmerjenost #1 desno   -1 levo
    global stevecHoje
    global slikaMec
    x=x+hitrost
    if usmerjenost <0:
        #slika za mec se obrne ce zamenjamo smer
        slikaMec =pygame.transform.flip(slikaMec,True,False)
    #ta stevec hoje je za animacije pa nocemo da gre v neskoncost
    #zato se nastavi na nic ce se smer obrne gremo tud na prvo animacijo
    if usmerjenost < 0 or stevecHoje>=59:
        usmerjenost=1
        stevecHoje=0
    stevecHoje+=1
def hodiLevo():
    #premaknemo se v levo
    global x
    global usmerjenost
    global stevecHoje
    global slikaMec
    x=x-hitrost
    #podobno kot pri hoji v desno
    if usmerjenost >0:
        slikaMec =pygame.transform.flip(slikaMec,True,False)
    if usmerjenost > 0 or stevecHoje>=59:
        usmerjenost=-1
        stevecHoje=0
    stevecHoje+=1
def gravitacija():
    #pristeje se vertikalna hitrost
    #ce pozitivna gre navzdol negativna pa navzgor
    global y
    y=y+vertikalnaHitrost
    #ce pade prenizko umre
    if y > 1500:
        smrt()
def interakcije():
    #interakcije igralca z ovirami (platformami)
    global y    
    global vertikalnaHitrost
    global lahkoSkoci
    global x
    global zamudaSkoka
    climb = False
    #gre cez vse ovire
    for objekt,tip in objects:
        dotik=False
        dotikZgoraj=False
        dotikLeva=False
        dotikDesna=False
        #preveri ce pada cez vrh ovire, pac je je od vzgori in ga postavi nazaj na vrh ovire preveri tud za dotike, da vemo pol ce igralec vzame kako skodo al pa ka takega
        if rect.bottom >= objekt.top-y and rect.bottom < objekt.top-y+vertikalnaHitrost and rect.right>=objekt.left-x and rect.left<=objekt.right-x:
            y = objekt.top-rect.bottom-1
            vertikalnaHitrost=0
            dotikZgoraj=True
            if lahkoSkoci == False:
                zamudaSkoka=zamudaSkokaMax
            lahkoSkoci=True
            dotik=True
        #preveri ce gre cez lev rob ovire ce gre ga nastavi nazaj na levo
        if usmerjenost==1 and stevecHoje>=0 and rect.right >= objekt.left-x and rect.right < objekt.left-x+hitrost and rect.bottom>=objekt.top-y and rect.top<objekt.bottom-y:
            x=objekt.left - rect.right-1
            dotik=True
            dotikDesna = True
        #preveri ce gre cez desn rob ovire in ce gre ga postavi nazaj na desno
        if usmerjenost==-1 and stevecHoje>=0 and rect.left <= objekt.right-x and rect.left > objekt.right - x - hitrost and rect.bottom>=objekt.top-y and rect.top<=objekt.bottom-y:
            x=objekt.right-rect.left+1
            dotik=True
            dotikLeva=True
        #ce skace in se v oviro zaletava od spodi (gre skoz njo) in postavi nazaj pod oviro
        if rect.top<=objekt.bottom-y and rect.top>objekt.bottom-y+vertikalnaHitrost and rect.right>=objekt.left-x and rect.left<=objekt.right-x:# and not rect.bottom > objekt.top-y and rect.bottom <= objekt.top-y+vertikalnaHitrost:
            y=objekt.bottom-rect.top+1
            vertikalnaHitrost=0
            dotik=True
        
        if dotik:
            if tip==1:
                #ce bil dotik in ovira je bla to ovira ki napada igralec vzame skodo
                skoda(0.7)
            if tip==-1 and dotikZgoraj:
                #ce ovira za zamgo in se dotaknil od zgoraj je igralec zmagal nivo
                zmaga()
            if tip==-2 and dotikZgoraj:
                #ce ovira za shranjevanje napredka in dotik zgoraj se mu ta napredek zdaj shrani
                global checkpointY
                global checkpointX
                global zivljenje
                zivljenje = 100
                checkpointX=objekt.centerx-rect.x-rect.width/2
                checkpointY=y
        #ce ma zogo lahko pleza tu bi lahk prisl do problema ce strop nad to oviro po kiri pleza
        if igralec ==3 and (dotikLeva or dotikDesna):
            climb = True
    if climb == True:
        vertikalnaHitrost=0
        y-=zo.hitrost
def skoda(skoda):
    #od igralca vzame zivljenske tocke in preveri ce umre
    global zivljenje
    zivljenje-=skoda
    if zivljenje<=0:
        smrt()
def skok():
    #ce skoci se mu vertikalna hitrost nastavi na visino skoka tak da bo neka casa se lgor
    global vertikalnaHitrost
    global lahkoSkoci
    if lahkoSkoci == True and vertikalnaHitrost<=0 and zamudaSkoka<=0:
        vertikalnaHitrost = visinaSkoka
        lahkoSkoci=False
def smrt():
    #ce umre se mu narise slika za smrt
    ekran.blit(slikaSmrt,(0,0))
    ekranGlavni.blit(pygame.transform.scale(ekran,ekranGlavni.get_size()),(0,0))
    #izklopi se glasba in predvaja se zvok za smrt
    pygame.display.update()
    pygame.mixer.music.pause()
    glasbaSmrt = pygame.mixer.Sound("music/Death.mp3")
    glasbaSmrt.set_volume(0.8)
    glasbaSmrt.play()
    time.sleep(3)
    #ponovi se nivo razen, ce ma tocko shranjevanja napredka te ga da nazaj nanjo
    restart(checkpointX,checkpointY)
def zmaga():
    #ce zmaga se preveri ce je to samo zmaga nivoja al nasplosna 
    #ce nivoja se pokaze ustreztna slika in gre na nasledno stopnjo 
    #ce pa dokoncna mu da koncno sliko pol pa ga da nazaj na 1. nivo
    global level
    priprava.level+=1
    ekran.blit(slikaZmagaZac,(0,0))
    if priprava.level>maxLevel:
        priprava.level=1
        ekran.blit(slikaZmaga,(0,0))
        
    ekranGlavni.blit(pygame.transform.scale(ekran,ekranGlavni.get_size()),(0,0))
    pygame.display.update()
    pygame.mixer.music.pause()
    time.sleep(3)
    restart()
def restart(valX=0,valY=0):
    #nalozi ustrezno stopnjo resetira vrednostti spremenljivk za igralca
    #ce ma checkpoint pa ga postavi nazaj na checkpoint
    #ta checkpoint izvemo iz parametrov, ki so dani v to metodo pa da igralca na zacetek
    global x,y,vertikalnaHitrost,zivljenje,lahkoSkoci,usmerjenost,stevecHoje,checkpointX,checkpointY,zamudaSkoka,zivljenje
    lahkoSkoci = True
    #usmerjenost = 1 # 1desna -1leva
    pygame.mixer.music.play()
    stevecHoje=-1 #za vsakih 20 nova animacija
    x=valX
    y=valY
    vertikalnaHitrost=0
    zivljenje=100
    checkpointX=0
    checkpointY=0
    zamudaSkoka=2 #da ne more skocit iz cekpointa takoj pa si ga zbrisat
    nalozi_level()
def spremeniIgralca(stIgralca):
    #nalozi pravega igralca
    global igralec,rect,hitrost,visinaSkoka,zamudaSkokaMax,lahkoNapada,checkpointX,checkpointY, napadZaostanekMax
    if stIgralca == 1 and seLahkoSpremeni(st.rect):
        igralec = 1
        rect=st.rect
        hitrost = st.hitrost
        visinaSkoka = st.visinaSkoka
        zamudaSkokaMax=st.zamudaSkokaMax
        lahkoNapada = st.lahkoNapada
        napadZaostanekMax = st.napadZaostanekMax
    if stIgralca == 2 and seLahkoSpremeni(m.rect):
        igralec = 2
        rect=m.rect
        hitrost = m.hitrost
        visinaSkoka = m.visinaSkoka
        zamudaSkokaMax=m.zamudaSkokaMax
        lahkoNapada = m.lahkoNapada
        napadZaostanekMax = m.napadZaostanekMax
    if stIgralca == 3 and seLahkoSpremeni(zo.rect):
        igralec = 3
        rect=zo.rect
        hitrost = zo.hitrost
        visinaSkoka = zo.visinaSkoka
        zamudaSkokaMax=zo.zamudaSkokaMax
        lahkoNapada = zo.lahkoNapada
        napadZaostanekMax = zo.napadZaostanekMax
def seLahkoSpremeni(taRect):
    #preveri ce se lahka spremni v zelenega igralca ker drgac lahka da bi ce gremo iz zoge v
    #osnovno obliko meli glavo v stropu ker smo v osnovni obliki visji
    for objekt,tip in objects:
        if taRect.colliderect(pygame.Rect((objekt.left-x,objekt.top-y),objekt.size)):
            return False
    return True
def rotiraj(koliko):
    #spremeni rotacijo igralca
    global rot
    rot-=koliko*usmerjenost
def interkcijeNasprotniki():
    global nasprotniki
    #gremo cez vse nasprotnike
    for i in reversed(range(len(nasprotniki))):
        #preveri ce se stikamo z nasprotniki
        if not rect.colliderect((nasprotniki[i].rect.left-x,nasprotniki[i].rect.top-y),nasprotniki[i].rect.size):
            continue
        #ce ne napadamo vzame skodo igralec ce mamo bodicasto zogo lahka da vzame skodo tud nasprotnik
        if napad == 0:
            if igralec==3:
                nasprotniki[i].skoda(random.randint(0,1))
                if nasprotniki[i].zivljenje<=0:
                    nasprotniki.pop(i)
            skoda(1)
            continue
        #ce pa napadamo pa je nasprotnik tisti ki vzame skodo
        nasprotniki[i].skoda(1)
        #ce ma zivljenje manj od nic ga  odstranimo
        if nasprotniki[i].zivljenje<=0:
            nasprotniki.pop(i)
