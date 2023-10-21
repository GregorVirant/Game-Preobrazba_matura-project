from priprava import *
hitrost = 5
visinaSkoka = -20
zamudaSkokaMax=0
sirinaPolovic=ekranSirina/2  #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
rect=slikaStojiDesno.get_rect(centerx=sirinaPolovic,bottom=objects[0][0].top-1)
lahkoNapada = False
napadZaostanekMax = 0
#OSNOVNI IGRALEC
#narise
def draw(lahkoSkoci,vertikalnaHitrost,stevecHoje,usmerjenost):
    #animacije ce skace
    if lahkoSkoci == False:
        if vertikalnaHitrost<0:
            ekran.blit(slikeSkok[0],rect)
        else:
            ekran.blit(slikeSkok[1],rect)
    #animacije ce hodi
    else:
        #ce stoji na mesti
        if stevecHoje==-1:
            #loci ce hodi desn al levo
            if usmerjenost==1:
                ekran.blit(slikaStojiDesno,rect)
            else:
                ekran.blit(slikaStojiLevo,rect)
        #to sped loci ce desn al levo
        elif usmerjenost==1:
            #zbere pravood treh slik ker gre od 1 do 60 pac pogledamo
            #kolk dobimo pri deljenji z 20 in potem pravega od treh
            #slik zberemo to pomen da je vsaka slika igralca gore za
            #20 slik (angl. frame-ov) to pa je približno tretina sekunde
            ekran.blit(slikeDesno[stevecHoje//20],rect)
        else:
            ekran.blit(slikeLevo[stevecHoje//20],rect) 